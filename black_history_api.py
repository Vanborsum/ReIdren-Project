import requests
import argparse
import json

# API key, GitHub safe!
with open("../bha-api-key.txt", "r") as f:
    key = f.read()

BASE_URL = "https://rest.blackhistoryapi.io"

def health_check(api_key, verbose):
    """Check if the API is up and running."""
    url = f"{BASE_URL}/health"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    print_response(response, verbose)

def get_fact(api_key, tags, people, verbose):
    """Fetch a fact based on tags and people."""
    url = f"{BASE_URL}/fact"
    params = {}
    if tags:
        params["tags"] = tags
    if people:
        params["people"] = people
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers, params=params)
    print_response(response, verbose)

def get_random_fact(api_key, verbose):
    """Fetch a random fact."""
    url = f"{BASE_URL}/fact/random"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    print_response(response, verbose)

def get_all_tags(api_key, verbose):
    """Fetch all available tags."""
    url = f"{BASE_URL}/template/tags"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    print_response(response, verbose, "get all")

def get_all_people(api_key, verbose):
    """Fetch all available people in the database."""
    url = f"{BASE_URL}/template/people"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    print_response(response, verbose, "get all")

def print_response(response, verbose, action="other"):
    """Print the API response in a readable format."""
    if response.status_code == 200:
        if verbose:
            pretty_json = json.dumps(response.json(), indent=4)
            print(pretty_json)  # Print formatted JSON response
        else:
            if action == "get all":
                things = []
                for item in response.json():
                    things.append(item.get("name"))
                for thing in set(things):
                    print(thing)
            else:
                facts = []
                for fact in response.json().get("Results"):
                    facts.append(fact["text"])
                for fact in set(facts):
                    print(fact)
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Black History facts.")
    parser.add_argument("--action", required=True, choices=["health", "fact", "random", "tags", "people"], help="Action to perform")
    parser.add_argument("--tags", help="Comma-separated list of tags (e.g., 'baseball,sports')", default=None)
    parser.add_argument("--people", help="Person's name (e.g., 'Rube Foster')", default=None)
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    if args.action == "health":
        health_check(key, args.verbose)
    elif args.action == "fact":
        get_fact(key, args.tags, args.people, args.verbose)
    elif args.action == "random":
        get_random_fact(key, args.verbose)
    elif args.action == "tags":
        get_all_tags(key, args.verbose)
    elif args.action == "people":
        get_all_people(key, args.verbose)
