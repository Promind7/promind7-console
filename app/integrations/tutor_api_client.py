# file created for Codex to fill
from __future__ import annotations

# NOTE ProMind7 :
# Client API Tutor LMS (non utilisé en production actuellement).
# Conservé pour de futures évolutions (ex : V3.1).

import os
from datetime import datetime
from typing import Dict, List, Optional

import requests

from services.log_service import log_error, log_info

# Configuration environment variable names
_BASE_URL_ENV_KEYS = ("TUTOR_API_BASE_URL", "TUTOR_LMS_API_BASE_URL")
_TOKEN_ENV_KEYS = ("TUTOR_API_TOKEN", "TUTOR_LMS_API_TOKEN", "TUTOR_API_KEY")
_ENDPOINT_ENV_KEYS = ("TUTOR_API_LEARNERS_ENDPOINT", "TUTOR_LMS_API_LEARNERS_ENDPOINT")
_BASIC_AUTH_KEY_ENV_KEYS = ("TUTOR_API_KEY", "TUTOR_LMS_API_KEY")
_BASIC_AUTH_SECRET_ENV_KEYS = ("TUTOR_API_SECRET", "TUTOR_LMS_API_SECRET")

# Endpoint par defaut cible les enrollments (meme logique que l'import ZIP)
DEFAULT_LEARNERS_ENDPOINT = "/wp-json/tutor/v1/enrollments"
DEFAULT_TIMEOUT = 15  # seconds


def _get_first_env(keys: tuple[str, ...]) -> Optional[str]:
    for key in keys:
        val = os.getenv(key)
        if val:
            return val
    return None


def _get_base_url() -> str:
    base_url = _get_first_env(_BASE_URL_ENV_KEYS)
    if not base_url:
        raise ValueError(
            "Tutor LMS API base URL not configured. "
            "Set TUTOR_API_BASE_URL (or TUTOR_LMS_API_BASE_URL)."
        )
    return base_url.rstrip("/")


def _get_token() -> Optional[str]:
    return _get_first_env(_TOKEN_ENV_KEYS)


def _get_basic_auth_credentials() -> Optional[tuple[str, str]]:
    key = _get_first_env(_BASIC_AUTH_KEY_ENV_KEYS)
    secret = _get_first_env(_BASIC_AUTH_SECRET_ENV_KEYS)
    if key and secret:
        return key, secret
    return None


def _get_learners_endpoint() -> str:
    endpoint = _get_first_env(_ENDPOINT_ENV_KEYS)
    if endpoint:
        return endpoint if endpoint.startswith("/") else f"/{endpoint}"
    return DEFAULT_LEARNERS_ENDPOINT


def _build_headers(token: Optional[str]) -> dict:
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_learners_since(
    since: datetime | None, page_size: int = 100
) -> List[Dict]:
    """
    Fetch learners created/updated since a given datetime.

    Args:
        since: datetime filter. If None, fetch all pages.
        page_size: page size for pagination.

    Returns:
        List of learner dicts as returned by Tutor LMS API (not transformed).
    """
    base_url = _get_base_url()
    token = _get_token()
    basic_auth = _get_basic_auth_credentials()
    endpoint = _get_learners_endpoint()
    headers = _build_headers(token if basic_auth is None else None)

    if basic_auth:
        log_info(f"[TutorAPI] Using Basic Auth (key length={len(basic_auth[0])}) from environment.")
    elif token:
        log_info(f"[TutorAPI] Using Bearer token from environment (len={len(token)})")
    else:
        log_info("[TutorAPI] No authentication credentials found in environment (request will likely fail with 401).")

    params: dict = {"per_page": page_size, "page": 1}
    if since:
        params["modified_after"] = since.isoformat()

    learners: List[Dict] = []
    page = 1

    while True:
        params["page"] = page
        url = f"{base_url}{endpoint}"
        try:
            if basic_auth:
                response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=DEFAULT_TIMEOUT,
                    auth=basic_auth,
                )
            else:
                response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=DEFAULT_TIMEOUT,
                )
        except requests.RequestException as exc:
            log_error(f"[TutorAPI] HTTP error on page {page}: {exc}")
            break

        if not response.ok:
            log_error(
                f"[TutorAPI] Non-2xx response on page {page}: "
                f"{response.status_code} {response.text}"
            )
            break

        try:
            payload = response.json()
        except ValueError:
            log_error(f"[TutorAPI] Invalid JSON on page {page}")
            break

        if isinstance(payload, list):
            page_learners = payload
        elif isinstance(payload, dict):
            page_learners = payload.get("data") or payload.get("results") or []
        else:
            page_learners = []

        if not isinstance(page_learners, list):
            log_error(f"[TutorAPI] Unexpected payload structure on page {page}")
            break

        learners.extend(page_learners)
        log_info(
            f"[TutorAPI] Fetched {len(page_learners)} learners on page {page} "
            f"(total {len(learners)})"
        )

        if len(page_learners) < page_size:
            break

        page += 1

    return learners


# Alias plus explicite pour les enrollments (V3 API)
def fetch_enrollments_since(
    since: datetime | None, page_size: int = 100
) -> List[Dict]:
    """
    Fetch enrollments created/updated since a given datetime.
    Maintient la compatibilite avec fetch_learners_since qui pointe
    par defaut sur le meme endpoint (enrollments).
    """
    return fetch_learners_since(since=since, page_size=page_size)
