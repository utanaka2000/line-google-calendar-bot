import os

from dotenv import load_dotenv
from google.cloud import secretmanager

load_dotenv()
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

def get_secret(secret_name):
    """Retrieve credentials JSON from Google Cloud Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    # Replace 'your-project-id' with your actual GCP project ID
    secret_path = f"projects/{GCP_PROJECT_ID}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": secret_path})
    return response.payload.data.decode("UTF-8")