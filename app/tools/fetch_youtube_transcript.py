# -*- coding: utf-8 -*-
"""
YouTube → transcription Whisper (markdown).

- **Une vidéo** ou **playlist** : traitement **séquentiel** (une vidéo après l’autre).
- Sortie par défaut : `Input/Script/Parcours stage & emploi/Sources/videos/transcripts/`
  (transcript + section **Idées clés (proM7)** à remplir par l’assistant ; voir skill **promind7-veille-youtube-transcription**).

Prérequis :
  - pip install yt-dlp
  - ffmpeg sur le PATH (ex. winget install ffmpeg)
  - pip install faster-whisper  (recommandé) ou pip install openai-whisper

Usage :
  python app/tools/fetch_youtube_transcript.py "URL_VIDEO_OU_PLAYLIST"
  python app/tools/fetch_youtube_transcript.py "URL" --no-playlist
  python app/tools/fetch_youtube_transcript.py "URL" --max-videos 5
  python app/tools/fetch_youtube_transcript.py "URL" --output-dir app/docs/veille
  python app/tools/fetch_youtube_transcript.py "URL" --whisper-model small --whisper-lang fr
  python app/tools/fetch_youtube_transcript.py "URL" --list-subs   # métadonnées sous-titres (1re vidéo)

Respectez les conditions d’utilisation de YouTube et les droits sur le contenu.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from youtube_veille_lib import (
    download_audio_mp3,
    expand_youtube_watch_urls,
    ffmpeg_available,
    list_available_subs,
    resolve_transcription_cache_dirs,
    resolve_whisper_engine,
    sanitize_filename,
    transcribe_audio,
    write_markdown_transcript,
    yt_extract_info,
)

_APP_DIR = Path(__file__).resolve().parent.parent
_REPO_ROOT = _APP_DIR.parent
_DEFAULT_TRANSCRIPTS = (
    _REPO_ROOT
    / "Input"
    / "Script"
    / "Parcours stage & emploi"
    / "Sources"
    / "videos"
    / "transcripts"
)


def _run_whisper_path(
    *,
    url: str,
    info: dict,
    transcripts_dir: Path,
    cache_audio_dir: Path,
    cache_whisper_root: Path,
    model_size: str,
    whisper_lang: str | None,
    engine: str,
    keep_audio: bool,
) -> Path:
    if not ffmpeg_available():
        raise SystemExit(
            "ffmpeg est introuvable (PATH). Installez ffmpeg pour extraire l’audio.\n"
            "Ex. Windows : winget install ffmpeg"
        )

    transcripts_dir = transcripts_dir.resolve()
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    cache_audio_dir.mkdir(parents=True, exist_ok=True)
    cache_whisper_root.mkdir(parents=True, exist_ok=True)

    video_id = info.get("id") or "unknown"
    title = info.get("title") or "video"

    mp3_path = download_audio_mp3(url, cache_audio_dir, video_id)
    try:
        resolved_engine = resolve_whisper_engine(engine)
        wdir = cache_whisper_root / video_id
        wdir.mkdir(parents=True, exist_ok=True)
        text, lang_out, engine_used = transcribe_audio(
            mp3_path,
            model_size=model_size,
            language=whisper_lang,
            workdir=wdir,
            engine=resolved_engine,
        )
    finally:
        if not keep_audio and mp3_path.is_file():
            mp3_path.unlink(missing_ok=True)

    slug = sanitize_filename(f"{video_id}_whisper_{model_size}_{title}", 100)
    md_path = transcripts_dir / f"{slug}.md"
    detail = (
        f"Whisper ({engine_used}, modèle {model_size}). "
        "Audio extrait avec yt-dlp + ffmpeg."
    )
    write_markdown_transcript(
        out_path=md_path,
        url=url,
        title=title,
        video_id=video_id,
        lang_label=str(lang_out),
        plain_text=text,
        source_detail=detail,
    )
    return md_path


def main() -> None:
    p = argparse.ArgumentParser(
        description=(
            "YouTube : audio + Whisper → markdown (vidéo ou playlist en chaîne). "
            "Défaut : Sources/videos/transcripts/"
        )
    )
    p.add_argument("url", help="URL d’une vidéo ou d’une playlist YouTube")
    p.add_argument(
        "--output-dir",
        type=Path,
        default=_DEFAULT_TRANSCRIPTS,
        help="Dossier des .md (défaut : Sources/.../videos/transcripts)",
    )
    p.add_argument(
        "--no-playlist",
        action="store_true",
        help="Ne traiter que la vidéo courante (ignore la playlist si l’URL en contient une)",
    )
    p.add_argument(
        "--max-videos",
        type=int,
        default=0,
        help="Nombre max de vidéos pour une playlist (0 = toutes)",
    )
    p.add_argument(
        "--list-subs",
        action="store_true",
        help="Lister les langues de sous-titres (1re vidéo seulement ; debug)",
    )
    p.add_argument(
        "--whisper-model",
        default="base",
        help="Modèle Whisper : tiny, base, small, medium, large-v3, …",
    )
    p.add_argument(
        "--whisper-lang",
        default="",
        help="Code langue forcé pour Whisper (ex. fr). Vide = détection auto",
    )
    p.add_argument(
        "--whisper-engine",
        choices=("auto", "faster", "openai"),
        default="auto",
        help="Moteur : faster-whisper (défaut si installé), ou openai-whisper",
    )
    p.add_argument(
        "--keep-audio",
        action="store_true",
        help="Conserver les MP3 dans le dossier cache _cache_audio",
    )
    args = p.parse_args()

    transcripts_dir = args.output_dir.resolve()
    cache_audio_dir, cache_whisper_root = resolve_transcription_cache_dirs(transcripts_dir)
    whisper_lang = args.whisper_lang.strip() or None
    max_v = args.max_videos if args.max_videos > 0 else None

    if args.list_subs:
        first = expand_youtube_watch_urls(
            args.url, no_playlist=args.no_playlist, max_videos=1
        )
        if not first:
            print("Aucune URL vidéo résolue.", file=sys.stderr)
            sys.exit(1)
        list_available_subs(first[0])
        return

    watch_urls = expand_youtube_watch_urls(
        args.url, no_playlist=args.no_playlist, max_videos=max_v
    )
    if not watch_urls:
        print("Aucune vidéo à traiter (URL invalide ou playlist vide).", file=sys.stderr)
        sys.exit(1)

    failures = 0
    for i, watch_url in enumerate(watch_urls, start=1):
        prefix = f"[{i}/{len(watch_urls)}]"
        try:
            info = yt_extract_info(watch_url, no_playlist=True)
        except Exception as e:
            failures += 1
            print(f"{prefix} FAIL métadonnées {watch_url} : {e}", file=sys.stderr)
            continue
        try:
            md_path = _run_whisper_path(
                url=watch_url,
                info=info,
                transcripts_dir=transcripts_dir,
                cache_audio_dir=cache_audio_dir,
                cache_whisper_root=cache_whisper_root,
                model_size=args.whisper_model,
                whisper_lang=whisper_lang,
                engine=args.whisper_engine,
                keep_audio=args.keep_audio,
            )
        except RuntimeError as e:
            failures += 1
            print(f"{prefix} FAIL {watch_url} : {e}", file=sys.stderr)
            continue
        except SystemExit:
            raise
        except Exception as e:
            failures += 1
            print(f"{prefix} FAIL {watch_url} : {e}", file=sys.stderr)
            continue
        try:
            print(f"{prefix} OK", md_path)
        except UnicodeEncodeError:
            print(f"{prefix} OK", str(md_path).encode("ascii", "backslashreplace").decode("ascii"))

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
