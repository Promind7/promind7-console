"""
Helper script to generate google_token.json via OAuth.

Regeneration procedure:
1) Run: python create_google_token.py
2) A browser window (or console URL) opens; sign in with the Google account that owns the target calendar.
3) Accept the requested scopes (Calendar + Calendar Events).
4) If prompted in console, paste the authorization code and press Enter.
5) Confirm that google_token.json is created/updated under app/data/.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]
_REPO = Path(__file__).resolve().parent.parent.parent
_DATA = _REPO / "app" / "data"
_DATA.mkdir(parents=True, exist_ok=True)
CREDENTIALS_PATH = str(_DATA / "google_credentials.json")
TOKEN_PATH = str(_DATA / "google_token.json")


def main() -> None:
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"ERROR: {CREDENTIALS_PATH} not found in current directory.")
        sys.exit(1)

    print("Opening browser for Google OAuth... If no browser opens, use the URL shown in the console.")
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_PATH,
            scopes=SCOPES,
        )
        creds = flow.run_local_server(port=0)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: OAuth flow failed: {exc}")
        sys.exit(1)

    try:
        with open(TOKEN_PATH, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: Failed to write {TOKEN_PATH}: {exc}")
        sys.exit(1)

    print(f"{TOKEN_PATH} generated successfully with scopes: {', '.join(SCOPES)}")


if __name__ == "__main__":
    main()
