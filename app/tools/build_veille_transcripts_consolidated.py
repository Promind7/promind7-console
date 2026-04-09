# -*- coding: utf-8 -*-
"""
Assemble tous les fichiers ``*.md`` de ``Sources/videos/transcripts/`` en **un seul**
document de travail : métadonnées, **transcription** (français si langue ``fr`` ; pistes **en**
: verbatim EN + note, ou traduction indicative si ``--translate-en`` + ``deep-translator``),
puis **Idées clés (proM7)**.

Sortie par défaut :
  Input/Script/Parcours stage & emploi/Sources/videos/CONSOLIDE_transcripts_idees_proM7.md

Chaque entrée commence par une ligne balise ``## VIDEO — NNN — …`` (parsing par l’UI Streamlit).

Usage (racine V2) ::
    python app/tools/build_veille_transcripts_consolidated.py
    python app/tools/build_veille_transcripts_consolidated.py --translate-en   # pip install deep-translator
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_DEFAULT_TRANSCRIPTS_DIR = (
    _REPO_ROOT
    / "Input"
    / "Script"
    / "Parcours stage & emploi"
    / "Sources"
    / "videos"
    / "transcripts"
)
_DEFAULT_OUT = (
    _REPO_ROOT
    / "Input"
    / "Script"
    / "Parcours stage & emploi"
    / "Sources"
    / "videos"
    / "CONSOLIDE_transcripts_idees_proM7.md"
)

_MARK_START = "## Transcript (texte)"
_MARK_IDEAS = "## Idées clés (proM7)"


def _extract_lang(text: str) -> str:
    m = re.search(r"^\-\s*\*\*Langue\*\*\s*:\s*(\S+)", text, re.MULTILINE)
    return (m.group(1) if m else "?").strip().lower()


def _extract_url(text: str) -> str:
    m = re.search(r"^\-\s*\*\*URL\*\*\s*:\s*(\S+)", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# Transcript YouTube —"):
            return line.replace("# Transcript YouTube —", "").strip()
    return fallback


def _extract_transcript_body(text: str) -> str:
    if _MARK_START not in text:
        return ""
    start = text.index(_MARK_START) + len(_MARK_START)
    rest = text[start:]
    end = len(rest)
    if _MARK_IDEAS in rest:
        end = min(end, rest.index(_MARK_IDEAS))
    chunk = rest[:end]
    # retirer un --- terminal avant Idées
    chunk = chunk.strip()
    if chunk.startswith("---"):
        chunk = chunk.lstrip("-").lstrip()
    return chunk.strip()


def _extract_ideas(text: str) -> str:
    if _MARK_IDEAS not in text:
        return ""
    return text[text.index(_MARK_IDEAS) :].strip()


def _translate_to_fr(text: str) -> str:
    try:
        from deep_translator import GoogleTranslator
    except ImportError as e:
        raise SystemExit(
            "Traduction : installez deep-translator : pip install deep-translator"
        ) from e
    if not text.strip():
        return ""
    tr = GoogleTranslator(source="en", target="fr")
    max_chunk = 4500
    parts: list[str] = []
    remain = text
    while remain:
        if len(remain) <= max_chunk:
            parts.append(tr.translate(remain))
            break
        cut = remain.rfind("\n\n", 0, max_chunk)
        if cut < max_chunk // 2:
            cut = max_chunk
        chunk = remain[:cut]
        remain = remain[cut:].lstrip()
        parts.append(tr.translate(chunk))
    return "\n\n".join(parts)


def parse_one(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8")
    return {
        "filename": path.name,
        "rel": f"Sources/videos/transcripts/{path.name}",
        "title": _extract_title(raw, path.stem),
        "url": _extract_url(raw),
        "lang": _extract_lang(raw),
        "transcript": _extract_transcript_body(raw),
        "ideas": _extract_ideas(raw),
    }


def build_markdown(paths: list[Path], *, translate_en: bool) -> str:
    iso = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        "# Consolidé — Transcripts & idées (veille YouTube, proM7)",
        "",
        f"- **Parcours** : Stage & emploi",
        f"- **Généré** : {iso}",
        "- **Source** : fichiers dans `Sources/videos/transcripts/*.md`",
        (
            "- **Transcriptions** : si **Langue** du fichier est `fr`, la section *Transcription (français)* "
            "reprend le verbatim Whisper. Si `en`, "
            + (
                "une **traduction indicative** (Google via `deep-translator`) est insérée — **à relire**."
                if translate_en
                else "le texte Whisper est en **anglais** ; la section **Idées clés (proM7)** reste la couche de travail **en français**."
            )
        ),
        "- **Mise à jour** : `python app/tools/build_veille_transcripts_consolidated.py` ; "
        "ajouter **`--translate-en`** pour une **traduction indicative** FR des pistes non-FR (dépendance `deep-translator`, résultat **à relire**).",
        "",
        "---",
        "",
    ]
    paths = sorted(paths, key=lambda p: p.name.lower())
    for i, p in enumerate(paths, start=1):
        d = parse_one(p)
        head = f"## VIDEO — {i:03d} — {d['title']}"
        lines.append(head)
        lines.append("")
        lines.append(f"- **Fichier source** : `{d['rel']}`")
        lines.append(f"- **URL** : {d['url'] or '—'}")
        lines.append(f"- **Langue Whisper** : `{d['lang']}`")
        lines.append("")
        lang = d["lang"].split("-")[0]
        trans = d["transcript"]
        lines.append("### Transcription (français)")
        lines.append("")
        if not trans.strip():
            lines.append("*(Transcription vide ou bloc non trouvé.)*")
        elif lang == "fr":
            lines.append(trans)
        else:
            if translate_en:
                try:
                    fr = _translate_to_fr(trans)
                    lines.append(fr)
                except SystemExit:
                    raise
                except Exception as exc:
                    lines.append(
                        f"*Échec traduction automatique ({exc!s}) — verbatim en langue source ci-dessous.*\n"
                    )
                    lines.append(trans)
            else:
                lines.append(
                    "*La piste Whisper n’est pas en français. Verbatim tel quel (souvent anglais) — "
                    "pour le script oral darija, s’appuyer sur les **Idées clés** ou régénérer / retraduire.*"
                )
                lines.append("")
                lines.append(trans)
        lines.append("")
        lines.append("### Idées clés (proM7)")
        lines.append("")
        if d["ideas"]:
            # sans re-dupliquer le titre ##
            body = d["ideas"]
            if body.startswith(_MARK_IDEAS):
                body = body[len(_MARK_IDEAS) :].lstrip()
            lines.append(body.strip() or "*(Section vide.)*")
        else:
            lines.append("*(Pas de section Idées clés dans le fichier source.)*")
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Consolide transcripts + idées proM7 en un .md")
    ap.add_argument(
        "--transcripts-dir",
        type=Path,
        default=_DEFAULT_TRANSCRIPTS_DIR,
        help="Dossier contenant les .md (défaut : …/Sources/videos/transcripts)",
    )
    ap.add_argument("--out", type=Path, default=_DEFAULT_OUT, help="Fichier Markdown sortie")
    ap.add_argument(
        "--translate-en",
        action="store_true",
        help="Traduire les transcripts non-FR vers le français (nécessite deep-translator)",
    )
    args = ap.parse_args()
    d = args.transcripts_dir
    if not d.is_dir():
        raise SystemExit(f"Dossier introuvable : {d}")
    paths = sorted(p for p in d.glob("*.md") if p.is_file())
    if not paths:
        raise SystemExit(f"Aucun .md dans {d}")
    text = build_markdown(paths, translate_en=args.translate_en)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(args.out.resolve(), len(paths), "vidéo(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
