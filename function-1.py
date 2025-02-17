import os
import tempfile
import subprocess
import openai
from openai import OpenAI
from google.cloud import storage, speech
import logging

# Initialize Google Cloud clients
storage_client = storage.Client()
speech_client = speech.SpeechClient()

# Set your OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

def process_video(event, context):
    logging.info(f"Event: {event}")
    logging.info(f"Context: {context}")
    """
    Cloud Function entry point triggered by a new video upload to GCS.
    Transcribes the video and generates social media posts.
    """
    bucket_name = event['bucket']
    video_file_name = event['name']
    storage_client = storage.Client()
    #speech_client = speech.SpeechClient()

    if video_file_name.startswith('post_uploads/') or video_file_name.startswith('audio/'):
        print(f"Skipping file {video_file_name}, not in correct folder.")
        return

    # Temporary directories for processing
    with tempfile.TemporaryDirectory() as tmpdirname:
        video_path = os.path.join(tmpdirname, video_file_name)
        audio_path = os.path.join(tmpdirname, "audio.wav")

        # Download video from Cloud Storage
        bucket = storage_client.bucket(bucket_name)
        print(bucket_name)
        blob = bucket.blob(video_file_name)
        print(blob)
        blob.download_to_filename(video_path)
        print(f"Downloaded {video_file_name} to {video_path}")

        # Step 1: Extract audio from video using FFmpeg
        subprocess.run(["ffmpeg", "-y", "-i", video_path, "-ar", "16000", "-ac", "1", audio_path], check=True)
        print(f"Extracted audio to {audio_path}")

        # Step 2: Transcribe the audio using Google Cloud Speech-to-Text (asynchronous)
        gcs_audio_uri = upload_audio_to_gcs(bucket_name, audio_path, video_file_name)
        transcript = transcribe_audio_async(gcs_audio_uri)
        print(f"Transcript: {transcript}")

        # Step 3: Generate social media posts using GPT-4
        social_media_posts = generate_social_media_posts(transcript)
        print(f"Generated Posts: {social_media_posts}")

        # Step 4: Save generated posts back to Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        output_blob = bucket.blob(f'post_uploads/{os.path.basename(video_file_name)}.txt')
        output_blob.upload_from_string(social_media_posts, content_type='text/plain; charset=utf-8')

        print(f"Generated posts uploaded to 'post_uploads/{os.path.basename(video_file_name)}.txt'")


def upload_audio_to_gcs(bucket_name, audio_path, video_file_name):
    """
    Upload the extracted audio to GCS for asynchronous transcription.
    """
    audio_blob_name = f"audio/{video_file_name}.wav"
    bucket = storage_client.bucket(bucket_name)
    audio_blob = bucket.blob(audio_blob_name)
    audio_blob.upload_from_filename(audio_path)
    gcs_audio_uri = f"gs://{bucket_name}/{audio_blob_name}"
    print(f"Uploaded audio to {gcs_audio_uri}")
    return gcs_audio_uri


def transcribe_audio_async(gcs_uri):
    """
    Asynchronous transcription for longer audio files.
    """
    #storage_client = storage.Client()
    speech_client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    operation = speech_client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=600)

    transcript = " ".join(result.alternatives[0].transcript for result in response.results)
    return transcript


def generate_social_media_posts(transcript):
    """
    Use GPT-4 to generate social media posts from the transcript.
    """
    messages = [
        {"role": "system", "content": "You are an assistant that summarizes video content for social media."},
        {"role": "user", "content": (
            "Based on the following transcript, create three engaging and concise social media posts "
            "that highlight the key points of the video. Each post should be brief and suitable for platforms like Twitter:\n\n"
            f"{transcript}"
        )}
    ]

    ai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


    gpt_response = ai_client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=300
    )

    return gpt_response.choices[0].message.content
