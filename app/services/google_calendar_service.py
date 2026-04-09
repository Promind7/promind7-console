import datetime as dt
import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

_APP = Path(__file__).resolve().parent.parent
_DATA = _APP / "data"
_DATA.mkdir(parents=True, exist_ok=True)
GOOGLE_CREDENTIALS_FILE = str(_DATA / "google_credentials.json")
GOOGLE_TOKEN_FILE = str(_DATA / "google_token.json")

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events"
]

def load_google_credentials():
    """Charge les credentials OAuth depuis le token Google."""
    if not Path(GOOGLE_TOKEN_FILE).exists():
        raise FileNotFoundError("google_token.json introuvable. Lance create_google_token.py")

    creds = Credentials.from_authorized_user_file(GOOGLE_TOKEN_FILE, SCOPES)
    return creds


def create_event(title, description, start_dt, end_dt, attendees_emails=None):
    """Crée un événement Google Calendar avec lien Google Meet."""
    creds = load_google_credentials()
    service = build("calendar", "v3", credentials=creds)

    event_body = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": "Europe/Paris"},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": "Europe/Paris"},
        "conferenceData": {
            "createRequest": {
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
                "requestId": f"promind7-{int(dt.datetime.utcnow().timestamp())}"
            }
        }
    }

    if attendees_emails:
        event_body["attendees"] = [{"email": e} for e in attendees_emails]

    event = service.events().insert(
        calendarId="primary",
        body=event_body,
        conferenceDataVersion=1
    ).execute()

    meet_url = None
    try:
        meet_url = event["conferenceData"]["entryPoints"][0]["uri"]
    except:
        pass

    return {
        "event_id": event.get("id"),
        "meet_url": meet_url
    }
