import os
import tempfile
import subprocess
import openai
from openai import OpenAI
from google.cloud import storage, speech
import logging
import functions_framework

# Initialize Google Cloud clients
storage_client = storage.Client()
speech_client = speech.SpeechClient()

# Set your OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

@functions_framework.cloud_event
def process_video(cloud_event):
    logging.info(f"Event: {cloud_event}")
    print(cloud_event)
    print("stop")
    """
    Cloud Function entry point triggered by a new video upload to GCS.
    Transcribes the video and generates social media posts.
    """
    event = cloud_event.data

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

        duration = get_video_duration(video_path)
        if duration > 1860:  # 1860 seconds = 31 minutes
            print(f"Video is longer than 31 minutes ({duration} seconds). Splitting into 30 min chunks...")
            chunk_paths = split_video_into_chunks(video_path, tmpdirname, 1800, bucket_name, video_file_name)  # Split into 30-minute chunks            
            return

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

def get_video_duration(video_path):
    """
    Get the duration of the video using ffprobe.
    """
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    duration = float(result.stdout.strip())
    print(f"Video duration: {duration} seconds")
    return duration


def split_video_into_chunks(video_path, output_dir, chunk_duration, bucket_name, video_file_name):
    """
    Split the video into chunks of the specified duration (in seconds) and upload each chunk to the bucket.
    """
    chunk_paths = []
    chunk_template = os.path.join(output_dir, "chunk_%03d.mp4")  # Unique naming template
    subprocess.run(
        ["ffmpeg", "-i", video_path, "-c", "copy", "-map", "0", "-segment_time", str(chunk_duration), "-f", "segment", "-reset_timestamps", "1", chunk_template],
        check=True
    )
    # Collect the paths of the generated chunks
    for chunk_file in sorted(os.listdir(output_dir)):
        if chunk_file.startswith("chunk_") and chunk_file.endswith(".mp4"):
            chunk_paths.append(os.path.join(output_dir, chunk_file))
    print(f"Split video into {len(chunk_paths)} chunks")

    # Upload each chunk to the bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    for i, chunk_path in enumerate(chunk_paths):
        chunk_blob_name = f"{os.path.splitext(video_file_name)[0]}_chunk{i+1}.mp4"
        chunk_blob = bucket.blob(chunk_blob_name)
        chunk_blob.upload_from_filename(chunk_path)
        print(f"Uploaded chunk {i+1} to {chunk_blob_name}")

    return chunk_paths

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
            "Based on the following transcript, create as many engaging social media posts as you can "
            "that highlight the key points of the video. Each post should be brief and suitable for platforms like Facebook or LinkedIn:\n\n"
            f"{transcript}"
        )}
    ]

    ai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


    gpt_response = ai_client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )

    return gpt_response.choices[0].message.content
