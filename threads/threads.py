import requests
import os
from dotenv import load_dotenv



class Threads:
    def __init__(self):
        load_dotenv()
        self.id = os.getenv("THREADS_ID")
        self.access_token = os.getenv("THREADS_ACCESS_TOKEN")
        
        if not self.id or not self.access_token:
            raise ValueError("THREADS_ID or THREADS_ACCESS_TOKEN environment variables are not set")

    def create_thread(self, text):
        url = f"https://graph.threads.net/v1.0/{self.id}/threads"

        text_with_tag = f"{text}#generatedBygpt-4o-mini"

        params = {
            "media_type": "TEXT",
            "text": text_with_tag,
            "access_token": self.access_token
        }

        try:
            response = requests.post(url, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            creation_id = response.json().get("id")
            if not creation_id:
                raise ValueError("No creation ID returned from API")
            return creation_id
        except requests.RequestException as e:
            print(f"Error creating thread: {e}")
            return None

    def post_thread(self, text):
        creation_id = self.create_thread(text)
        if not creation_id:
            return None

        url = f"https://graph.threads.net/v1.0/{self.id}/threads_publish"
        params = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }

        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error posting thread: {e}")
            return None

    def main(self, text):
        result = self.post_thread(text)
        if result:
            print("Thread posted successfully:", result)
        else:
            print("Failed to post thread")

if __name__ == "__main__":
    threads = Threads()
    threads.main("Hello, Threads!")
