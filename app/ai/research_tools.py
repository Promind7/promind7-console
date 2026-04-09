"""
Recherche web / vidéos pour l'agent rédacteur (sources indicatives).

Utilise DuckDuckGo (sans clé API). Peut échouer selon réseau / rate limits.
"""
from __future__ import annotations

import re
from typing import List, Tuple

import requests

DEFAULT_TIMEOUT = 12
MAX_URL_BYTES = 120_000
TEXT_CONTEXT_CHARS = 12_000


def _strip_html(html: str) -> str:
    html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>", " ", html)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"\s+", " ", html)
    return html.strip()


def fetch_url_text(url: str) -> Tuple[str, str | None]:
    """
    Télécharge une page et extrait du texte brut (aperçu).
    Retourne (texte, erreur).
    """
    try:
        r = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT,
            headers={
                "User-Agent": "ProMind7-WriterBot/1.0 (formation; +https://promind7.com)"
            },
        )
        r.raise_for_status()
        raw = r.content[:MAX_URL_BYTES]
        charset = r.encoding or "utf-8"
        try:
            html = raw.decode(charset, errors="replace")
        except LookupError:
            html = raw.decode("utf-8", errors="replace")
        text = _strip_html(html)
        if len(text) > TEXT_CONTEXT_CHARS:
            text = text[:TEXT_CONTEXT_CHARS] + "\n\n[…tronqué…]"
        return text, None
    except Exception as exc:  # noqa: BLE001
        return "", str(exc)


def search_web(query: str, max_results: int = 6) -> List[dict]:
    """Résultats texte DuckDuckGo."""
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=max_results))
    except Exception:  # noqa: BLE001
        return []


def search_videos(query: str, max_results: int = 5) -> List[dict]:
    """Résultats vidéo (liens YouTube / autres selon DDG)."""
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            return list(ddgs.videos(query, max_results=max_results))
    except Exception:  # noqa: BLE001
        return []


def format_sources_for_prompt(
    text_hits: List[dict], video_hits: List[dict], fetch_first_n: int = 2
) -> str:
    """Construit un bloc markdown pour le contexte LLM."""
    lines: List[str] = ["## Sources trouvées (à citer ; ne pas inventer au-delà)"]

    for i, h in enumerate(text_hits, 1):
        title = h.get("title") or "Sans titre"
        href = h.get("href") or ""
        body = (h.get("body") or "")[:500]
        lines.append(f"### Web {i}: {title}\n- URL: {href}\n- Snippet: {body}\n")

    for i, h in enumerate(video_hits, 1):
        title = h.get("title") or "Vidéo"
        href = h.get("content") or h.get("embed_html") or ""
        lines.append(f"### Vidéo {i}: {title}\n- Lien: {href}\n")

    # Enrichir les 1–2 premiers liens web avec extrait page
    for idx, h in enumerate(text_hits[:fetch_first_n]):
        href = h.get("href")
        if not href or not str(href).startswith("http"):
            continue
        txt, err = fetch_url_text(str(href))
        if txt and not err:
            lines.append(
                f"### Extrait page ({idx + 1})\nURL: {href}\n\n{txt[:4000]}\n"
            )
        elif err:
            lines.append(f"### Page non lisible ({href}): {err}\n")

    return "\n".join(lines) if len(lines) > 1 else ""
