import datetime
import json
import os

import pytz
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.cloud import secretmanager
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_secret(project_id, secret_name):
    """Retrieve credentials JSON from Google Cloud Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    # Replace 'your-project-id' with your actual GCP project ID
    secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": secret_path})
    secret_payload = response.payload.data.decode("UTF-8")
    return json.loads(secret_payload)

def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  secret = get_secret(os.environ["GCP_PROJECT_ID"], os.environ["GCP_SECRET_ID"])
  creds = Credentials.from_authorized_user_info(secret, SCOPES)
  creds.refresh(Request())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    # 日本時間（JST）
    jst = pytz.timezone('Asia/Tokyo')
    now_jst = datetime.datetime.now(jst)
    now_utc = now_jst.astimezone(pytz.utc)
    now = now_utc.isoformat()
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()