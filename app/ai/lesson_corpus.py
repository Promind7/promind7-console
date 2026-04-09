"""
Assemblage du texte des leçons .docx d’un pack (pour cohérence agent rédaction).

Préfixes de dossiers typiques : ``00-``, ``01-``, ``02-`` (modules 0 à 2).
Configurable via ``PROMIND7_MBA_CORPUS_PREFIXES`` (virgules).
"""
from __future__ import annotations

import os
from pathlib import Path

from services.stage_emploi_service import list_lesson_docx_files, load_script_text


def _default_prefixes() -> tuple[str, ...]:
    raw = (os.getenv("PROMIND7_MBA_CORPUS_PREFIXES") or "00-,01-,02-").strip()
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    return tuple(parts) if parts else ("00-", "01-", "02-")


def build_module_corpus_text(
    pack_root: Path | str,
    *,
    module_prefixes: tuple[str, ...] | None = None,
    max_total_chars: int = 70_000,
) -> str:
    """
    Concatène le texte extrait des .docx dont le chemin relatif commence
    par l’un des préfixes (ex. ``00-Module 0/...``).
    """
    root = Path(pack_root)
    if not root.is_dir():
        return ""

    prefixes = module_prefixes if module_prefixes is not None else _default_prefixes()
    items = list_lesson_docx_files(root)
    chunks: list[str] = []

    def sort_key(d: dict) -> str:
        return d["rel_posix"].lower()

    for it in sorted(items, key=sort_key):
        rel = it["rel_posix"].replace("\\", "/")
        if not any(rel.startswith(p) for p in prefixes):
            continue
        text, err = load_script_text(it["path"])
        if err or not (text or "").strip():
            continue
        chunks.append(f"### Fichier : `{rel}`\n\n{text.strip()}\n")

    full = "\n\n---\n\n".join(chunks)
    if len(full) > max_total_chars:
        full = full[:max_total_chars] + "\n\n[… corpus tronqué — augmenter PROMIND7_MBA_CORPUS_MAX_CHARS si besoin …]"
    return full


def mba_corpus_pack_root() -> Path | None:
    """Racine du pack pour le corpus MBA (variable d’env ou parcours Stage & emploi par défaut)."""
    env = (os.getenv("PROMIND7_MBA_CORPUS_PACK_ROOT") or "").strip()
    if env:
        p = Path(env)
        return p if p.is_dir() else None
    from services.stage_emploi_service import get_stage_emploi_root

    r = get_stage_emploi_root()
    return r if r.is_dir() else None
