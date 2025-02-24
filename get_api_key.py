import os
from dotenv import load_dotenv
from google.cloud import secretmanager

class APIKeyRetrievalError(Exception):
    """Custom exception for API key retrieval failures."""
    pass


def get_api_key():
    """Retrieves the OpenAI API key from either Secret Manager or a .env file."""

    # Check if running in Google Cloud environment.  This is a rudimentary check;
    # more robust checks might be needed depending on your deployment strategy.
    is_gcp_environment = os.environ.get("GAE_APPLICATION", "") != ""

    if is_gcp_environment:
        try:
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/the-secret-ai-edition/secrets/API_KEY/versions/latest" # Replace with your secret path
            response = client.access_secret_version(request={"name": name})
            api_key = response.payload.data.decode("UTF-8")
            print("API key retrieved from Secret Manager.")
            return api_key
        except Exception as e:
            raise APIKeyRetrievalError(f"Error retrieving API key from Secret Manager: {e}")

    else:  # Assume local development environment
        load_dotenv()
        api_key = os.getenv("API_KEY")
        if api_key:
            print("API key retrieved from .env file.")
            return api_key
        else:
            raise APIKeyRetrievalError("API key not found in .env file. Please set the API_KEY environment variable.")


# Example usage:
#api_key = get_api_key()
#if api_key:
#    import openai
#    openai.api_key = api_key
#    # Proceed with OpenAI API calls
#else:
#    print("Failed to retrieve API key. Exiting.")
#    exit(1)
