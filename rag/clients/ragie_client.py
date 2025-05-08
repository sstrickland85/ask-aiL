import requests
from typing import List, Dict, Any


class RagieClient:
    """Client for interacting with ragie.ai API"""

    def __init__(self, url: str, api_key: str):
        self.url = url.rstrip('/')  # Remove trailing slash if present
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def retrieve_chunks(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks based on user query."""

        payload = {
            'query': query,
            'top_k': top_k
        }

        try:
            response = requests.post(
                f"{self.url}/retrievals",
                headers=self.headers,
                json=payload,
                timeout=30  # Add a reasonable timeout
            )

            # Handle common error codes specifically
            if response.status_code == 401:
                raise Exception("Authentication failed. Please check your Ragie API key.")
            elif response.status_code == 404:
                raise Exception("Ragie API endpoint not found. Check your URL configuration.")
            elif response.status_code != 200:
                raise Exception(f"Ragie API error (HTTP {response.status_code}): {response.text}")

            # Return the scored chunks directly
            return response.json()["scored_chunks"]

        except requests.RequestException as e:
            # More specific error for network issues
            raise Exception(f"Network error connecting to Ragie API: {str(e)}")