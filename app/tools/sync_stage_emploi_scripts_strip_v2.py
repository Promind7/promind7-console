#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copie le parcours **Stage & emploi** vers ``02-Contenus/01-Scripts`` (ou ``--dest``) :

- Contenu **V2** : chaque ``*-V2.docx`` est copié vers un nom **sans** ``-V2`` ni suffixe ``-darija`` (même arborescence).
- Les autres ``.docx`` hors ``Sources/`` sont copiés **seulement** s’il n’y a pas déjà une
  version ``-V2`` pour le même stem cible (évite d’écraser avec un V1 obsolète).
- Le dossier ``Sources/`` est recopié en entier (vidéos / transcripts / consolidé, etc.).

Exemple :

  python app/tools/sync_stage_emploi_scripts_strip_v2.py

Variables optionnelles : ``PROMIND7_SYNC_SCRIPT_SOURCE``, ``PROMIND7_SYNC_SCRIPT_DEST``.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

# Racine projet console (dossier contenant ``app/``)
_ROOT = Path(__file__).resolve().parents[2]
_APP = _ROOT / "app"
if str(_APP) not in sys.path:
    sys.path.insert(0, str(_APP))

from services.stage_emploi_service import (  # noqa: E402
    WORD_DOCX_V2_FILE_SUFFIX,
    get_stage_emploi_root,
    normalize_script_display_stem,
)

_SUFFIX = WORD_DOCX_V2_FILE_SUFFIX  # "-V2"

_DEFAULT_SOURCE = Path(
    os.getenv("PROMIND7_SYNC_SCRIPT_SOURCE", r"D:\Promind7\IA\V2\Input\Script\Parcours stage & emploi")
)
_DEFAULT_DEST_PARENT = Path(
    os.getenv(
        "PROMIND7_SYNC_SCRIPT_DEST",
        r"D:\01-ProM7-consulting\01-Promind7\02-Contenus\01-Scripts\Parcours stage & emploi",
    )
)


def _is_under_sources(rel: Path) -> bool:
    parts = rel.parts
    return len(parts) > 0 and parts[0].casefold() == "sources"


def _gather_docx_choices(src: Path) -> dict[Path, Path]:
    """relatif → chemin source absolu (fichier à copier)."""
    choices: dict[Path, Path] = {}

    all_docx = sorted(src.rglob("*.docx"), key=lambda p: str(p).lower())
    for p in all_docx:
        try:
            rel = p.relative_to(src)
        except ValueError:
            continue
        if _is_under_sources(rel):
            continue
        stem = p.stem
        parent = rel.parent
        if stem.endswith(_SUFFIX):
            base = stem[: -len(_SUFFIX)]
            norm = normalize_script_display_stem(base)
            key = parent / f"{norm}.docx"
            choices[key] = p

    for p in all_docx:
        try:
            rel = p.relative_to(src)
        except ValueError:
            continue
        if _is_under_sources(rel):
            continue
        if p.stem.endswith(_SUFFIX):
            continue
        stem = p.stem
        parent = rel.parent
        key = parent / f"{normalize_script_display_stem(stem)}.docx"
        if key not in choices:
            choices[key] = p

    return choices


def sync_pack(*, src: Path, dest: Path, dry_run: bool) -> tuple[int, list[str]]:
    log: list[str] = []
    if not src.is_dir():
        raise SystemExit(f"Source introuvable : {src}")

    choices = _gather_docx_choices(src)
    n = 0
    for rel_key, src_file in sorted(choices.items(), key=lambda x: str(x[0]).lower()):
        out = dest / rel_key
        msg = f"{src_file.relative_to(src)}  ->  {out.relative_to(dest)}"
        log.append(msg)
        if not dry_run:
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, out)
        n += 1

    src_sources = src / "Sources"
    if src_sources.is_dir():
        dst_sources = dest / "Sources"
        log.append(f"[Sources]  {src_sources}  ->  {dst_sources}")
        if not dry_run:
            shutil.copytree(src_sources, dst_sources, dirs_exist_ok=True)

    return n, log


def main() -> None:
    ap = argparse.ArgumentParser(description="Copie Stage & emploi, noms .docx sans -V2.")
    ap.add_argument(
        "--source",
        type=Path,
        default=_DEFAULT_SOURCE,
        help="Dossier source « Parcours stage & emploi » (défaut : variable ou chemin V2 connu).",
    )
    ap.add_argument(
        "--dest",
        type=Path,
        default=_DEFAULT_DEST_PARENT,
        help="Dossier cible (défaut : 02-Contenus/01-Scripts/Parcours stage & emploi).",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Affiche les opérations sans écrire.",
    )
    args = ap.parse_args()

    # get_stage_emploi_root() utile si l’utilisateur a déjà PROMIND7_STAGE_EMPLOI_SCRIPT_ROOT
    src = args.source.resolve()
    if not src.is_dir() and os.getenv("PROMIND7_STAGE_EMPLOI_SCRIPT_ROOT", "").strip():
        alt = get_stage_emploi_root()
        if alt.is_dir():
            src = alt
            print(f"Source (via PROMIND7_STAGE_EMPLOI_SCRIPT_ROOT) : {src}", file=sys.stderr)

    dest = args.dest.resolve()
    n, lines = sync_pack(src=src, dest=dest, dry_run=args.dry_run)
    print(f"{'[dry-run] ' if args.dry_run else ''}{n} fichier(s) .docx (hors Sources).")
    for line in lines:
        print(line)
    if args.dry_run:
        print("(Aucun fichier écrit — retirez --dry-run pour copier.)")


if __name__ == "__main__":
    main()
