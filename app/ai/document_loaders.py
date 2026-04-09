"""Extraction de texte depuis fichiers locaux (référence de style / contenu)."""
from __future__ import annotations

from pathlib import Path


def read_text_file(path: Path, max_chars: int = 25_000) -> str:
    p = Path(path)
    if not p.is_file():
        return ""
    raw = p.read_text(encoding="utf-8", errors="replace")
    if len(raw) > max_chars:
        return raw[:max_chars] + "\n\n[…tronqué…]"
    return raw


def read_docx_file(path: Path, max_chars: int = 25_000) -> str:
    try:
        import docx  # python-docx
    except ImportError:
        return ""
    p = Path(path)
    if not p.is_file() or p.suffix.lower() != ".docx":
        return ""
    document = docx.Document(str(p))
    parts: list[str] = []
    for para in document.paragraphs:
        t = (para.text or "").strip()
        if t:
            parts.append(t)
    raw = "\n".join(parts)
    if len(raw) > max_chars:
        return raw[:max_chars] + "\n\n[…tronqué…]"
    return raw


def load_local_reference(path_str: str) -> tuple[str, str | None]:
    """Charge un fichier .md, .txt ou .docx ; retourne (texte, erreur)."""
    p = Path(path_str.strip().strip('"'))
    if not p.is_file():
        return "", "Fichier introuvable."
    suf = p.suffix.lower()
    try:
        if suf in {".md", ".txt"}:
            return read_text_file(p), None
        if suf == ".docx":
            t = read_docx_file(p)
            if not t:
                return "", "Lecture .docx vide ou python-docx absent."
            return t, None
        return "", f"Extension non supportée: {suf}"
    except Exception as exc:  # noqa: BLE001
        return "", str(exc)
