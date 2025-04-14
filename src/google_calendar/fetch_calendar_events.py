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

def fetch_upcoming_events(num_events=10):
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  secret = get_secret(os.environ["GCP_PROJECT_ID"], os.environ["GCP_SECRET_ID"])
  creds = Credentials.from_authorized_user_info(secret, SCOPES)
  creds.refresh(Request())

  service = build("calendar", "v3", credentials=creds)

  # Call the Calendar API
  # 日本時間（JST）
  jst = pytz.timezone('Asia/Tokyo')
  now_jst = datetime.datetime.now(jst)
  now_utc = now_jst.astimezone(pytz.utc)
  now = now_utc.isoformat()
  events_result = (
      service.events()
      .list(
          calendarId="primary",
          timeMin=now,
          maxResults=num_events,
          singleEvents=True,
          orderBy="startTime",
      )
      .execute()
  )
  events = events_result.get("items", [])
  return events

def fetch_tomorrow_events():
  events = fetch_upcoming_events()
  tomorrow = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).date() + datetime.timedelta(days=1)
  return [
      event["summary"] for event in events
      if datetime.datetime.fromisoformat(event["start"].get("date")).date() == tomorrow
  ]
  

if __name__ == "__main__":
  print(fetch_upcoming_events())
  print(fetch_tomorrow_events())