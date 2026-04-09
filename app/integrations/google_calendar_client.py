"""
Google Calendar integration client for ProMind7 sessions.

Uses google_token.json (OAuth user token) to create/delete events with Meet links.
Returns None on errors to let callers handle gracefully.
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from services.log_service import log_error, log_info

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except Exception:  # noqa: BLE001
    Credentials = None  # type: ignore
    Request = None  # type: ignore
    build = None  # type: ignore
    HttpError = Exception  # type: ignore

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]
DEFAULT_CALENDAR_ID = "primary"
DEFAULT_TIMEZONE = (
    os.getenv("PROMIND7_GOOGLE_TIMEZONE", "Africa/Casablanca") or "Africa/Casablanca"
)
_APP = Path(__file__).resolve().parent.parent
_DATA = _APP / "data"
_DATA.mkdir(parents=True, exist_ok=True)
TOKEN_PATH = _DATA / "google_token.json"


def load_credentials() -> Optional[Credentials]:
    if not all([Credentials, Request, build]):
        log_error("[GoogleCalendar] google-api-python-client not installed.")
        return None

    if not TOKEN_PATH.exists():
        log_error(f"[GoogleCalendar] Token file missing at {TOKEN_PATH}.")
        return None

    try:
        creds: Credentials = Credentials.from_authorized_user_file(
            str(TOKEN_PATH), SCOPES
        )
    except Exception as exc:  # noqa: BLE001
        log_error(f"[GoogleCalendar] Failed to load token: {exc}")
        return None

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            with open(TOKEN_PATH, "w", encoding="utf-8") as f:
                f.write(creds.to_json())
        except Exception as exc:  # noqa: BLE001
            log_error(f"[GoogleCalendar] Token refresh failed: {exc}")
            return None

    if not creds or not creds.valid:
        log_error("[GoogleCalendar] Invalid credentials; skipping Calendar call.")
        return None

    return creds


def _build_service():
    creds = load_credentials()
    if not creds:
        return None
    try:
        return build("calendar", "v3", credentials=creds)
    except Exception as exc:  # noqa: BLE001
        log_error(f"[GoogleCalendar] Failed to build service: {exc}")
        return None


def _extract_meet_url(event: Dict) -> Optional[str]:
    if not event:
        return None
    if event.get("hangoutLink"):
        return event.get("hangoutLink")
    conference = event.get("conferenceData") or {}
    entry_points = conference.get("entryPoints") or []
    for ep in entry_points:
        if ep.get("entryPointType") and ep.get("entryPointType").lower() != "video":
            continue
        uri = ep.get("uri")
        if uri:
            return uri
    return None


def create_session_event(
    title: str,
    description: Optional[str],
    start_at: str,
    end_at: str,
    attendees_emails: Optional[List[str]] = None,
) -> Optional[Dict[str, str]]:
    try:
        start_dt = datetime.fromisoformat(start_at)
        end_dt = datetime.fromisoformat(end_at)
        service = _build_service()
        if not service:
            return None

        attendee_list = []
        seen = set()
        for email in attendees_emails or []:
            if email and email.lower() not in seen:
                attendee_list.append({"email": email})
                seen.add(email.lower())

        body = {
            "summary": title,
            "description": description or "",
            "start": {"dateTime": start_dt.isoformat(), "timeZone": DEFAULT_TIMEZONE},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": DEFAULT_TIMEZONE},
        }
        if attendee_list:
            body["attendees"] = attendee_list
        body["conferenceData"] = {
            "createRequest": {
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
                "requestId": f"pm7-{uuid.uuid4()}",
            }
        }

        event = (
            service.events()
            .insert(
                calendarId=DEFAULT_CALENDAR_ID,
                body=body,
                conferenceDataVersion=1,
            )
            .execute()
        )
        event_id = event.get("id")
        meet_url = event.get("hangoutLink") or _extract_meet_url(event)
        log_info(f"[GoogleCalendar] Created event {event_id} with Meet {meet_url}")
        return {"event_id": event_id, "meet_url": meet_url}
    except HttpError as http_exc:  # type: ignore
        log_error(f"[GoogleCalendar] Failed to create event: {http_exc}")
        return None
    except Exception as exc:  # noqa: BLE001
        log_error(f"[GoogleCalendar] Failed to create event: {exc}")
        return None


def delete_event(event_id: str) -> None:
    if not event_id:
        return
    service = _build_service()
    if not service:
        return
    try:
        service.events().delete(calendarId=DEFAULT_CALENDAR_ID, eventId=event_id).execute()
        log_info(f"[GoogleCalendar] Deleted event {event_id}")
    except HttpError as http_exc:  # type: ignore
        status = getattr(http_exc, "resp", None)
        status_code = getattr(status, "status", None)
        if status_code == 404:
            log_info(f"[GoogleCalendar] Event {event_id} already deleted (404).")
            return
        log_error(f"[GoogleCalendar] Failed to delete event {event_id}: {http_exc}")
    except Exception as exc:  # noqa: BLE001
        log_error(f"[GoogleCalendar] Failed to delete event {event_id}: {exc}")


def update_session_event(
    event_id: str,
    title: str,
    description: Optional[str],
    start_at: str,
    end_at: str,
    attendees_emails: Optional[List[str]] = None,
) -> Optional[Dict[str, str]]:
    try:
        start_dt = datetime.fromisoformat(start_at)
        end_dt = datetime.fromisoformat(end_at)
    except Exception as exc:  # noqa: BLE001
        log_error(f"[GoogleCalendar] Failed to update event: {exc}")
        return None

    service = _build_service()
    if not service:
        return None

    attendee_list = []
    seen = set()
    for email in attendees_emails or []:
        if email and email.lower() not in seen:
            attendee_list.append({"email": email})
            seen.add(email.lower())

    body = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": DEFAULT_TIMEZONE},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": DEFAULT_TIMEZONE},
        "attendees": attendee_list,
    }

    try:
        event = (
            service.events()
            .patch(
                calendarId=DEFAULT_CALENDAR_ID,
                eventId=event_id,
                body=body,
                conferenceDataVersion=1,
            )
            .execute()
        )
    except HttpError as http_exc:  # type: ignore
        log_error(f"[GoogleCalendar] Failed to update event: {http_exc}")
        return None
    except Exception as exc:  # noqa: BLE001
        log_error(f"[GoogleCalendar] Failed to update event: {exc}")
        return None

    meet_url = _extract_meet_url(event)
    log_info(f"[GoogleCalendar] Updated event {event_id} with Meet {meet_url}")
    return {"event_id": event_id, "meet_url": meet_url}
