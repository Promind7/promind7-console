# -*- coding: utf-8 -*-
"""Utilitaires partagés : audio YouTube (yt-dlp) + Whisper ; expansion playlist."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def sanitize_filename(s: str, max_len: int = 80) -> str:
    s = re.sub(r'[<>:"/\\|?*]', "", s)
    s = re.sub(r"\s+", "_", s.strip())
    # Évite emojis / pictogrammes (chemins + print console Windows cp1252)
    s = re.sub(r"[\ufe0e\ufe0f]", "", s)
    s = re.sub(r"[\u2600-\u26FF\u2700-\u27BF]", "", s)
    s = re.sub(r"[\U00010000-\U0010FFFF]", "", s)
    return s[:max_len] if len(s) > max_len else s


def yt_extract_info(url: str, *, no_playlist: bool = False) -> dict:
    from yt_dlp import YoutubeDL

    opts: dict = {"quiet": True, "no_warnings": True, "skip_download": True}
    if no_playlist:
        opts["noplaylist"] = True
    with YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)


def expand_youtube_watch_urls(
    url: str,
    *,
    no_playlist: bool = False,
    max_videos: int | None = None,
) -> list[str]:
    """
    Retourne une liste d’URLs `watch?v=` (une entrée par vidéo).
    Pour une playlist, utilise extract_flat (rapide, sans télécharger).
    """
    from yt_dlp import YoutubeDL

    opts: dict = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": "in_playlist",
    }
    if no_playlist:
        opts["noplaylist"] = True
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

    out: list[str] = []
    entries = info.get("entries")
    if entries:
        for e in entries:
            if not e:
                continue
            vid = e.get("id")
            if isinstance(vid, str) and len(vid) == 11:
                out.append(f"https://www.youtube.com/watch?v={vid}")
            else:
                u = e.get("url")
                if isinstance(u, str) and u.startswith("http"):
                    out.append(u)
        if max_videos is not None and max_videos > 0:
            out = out[:max_videos]
        return out

    vid = info.get("id")
    if isinstance(vid, str) and vid:
        u = info.get("webpage_url")
        if isinstance(u, str) and u.startswith("http"):
            return [u]
        return [f"https://www.youtube.com/watch?v={vid}"]
    return []


def resolve_transcription_cache_dirs(transcripts_dir: Path) -> tuple[Path, Path]:
    """
    Si sortie = .../Sources/videos/transcripts, caches au niveau .../videos/.
    Sinon caches dans le même dossier que les .md (comportement historique docs/veille).
    """
    transcripts_dir = transcripts_dir.resolve()
    if transcripts_dir.name == "transcripts":
        root = transcripts_dir.parent
        return root / "_cache_audio", root / "_cache_whisper_openai"
    return transcripts_dir / "_cache_audio", transcripts_dir / "_cache_whisper_openai"


def list_available_subs(url: str) -> dict:
    info = yt_extract_info(url)
    video_id = info.get("id") or "unknown"
    title = info.get("title") or "video"
    subs = info.get("subtitles") or {}
    auto = info.get("automatic_captions") or {}
    print(f"Titre : {title}\nID    : {video_id}\n")
    print("Sous-titres (manuel) :", ", ".join(subs.keys()) or "(aucun)")
    print("Sous-titres (auto)   :", ", ".join(auto.keys()) or "(aucun)")
    return info


def download_audio_mp3(url: str, cache_dir: Path, video_id: str) -> Path:
    """Télécharge l’audio et extrait en MP3 (ffmpeg requis sur le PATH)."""
    from yt_dlp import YoutubeDL

    cache_dir.mkdir(parents=True, exist_ok=True)
    out_base = str(cache_dir / video_id)
    ydl_opts: dict = {
        "format": "bestaudio/best",
        "outtmpl": out_base + ".%(ext)s",
        "quiet": False,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    mp3 = cache_dir / f"{video_id}.mp3"
    if not mp3.is_file():
        raise FileNotFoundError(
            f"MP3 introuvable après extraction : {mp3}. "
            "Installez ffmpeg et vérifiez qu’il est dans le PATH."
        )
    return mp3


def _pick_whisper_device() -> str:
    """
    Par défaut : CPU (évite les GPU « détectés » mais sans libs CUDA complètes sous Windows).
    Pour forcer le GPU : variable d'environnement YT_VEILLE_USE_CUDA=1
    """
    import os

    if os.environ.get("YT_VEILLE_USE_CUDA", "").strip().lower() in ("1", "true", "yes"):
        try:
            import ctranslate2

            if ctranslate2.get_cuda_device_count() > 0:
                return "cuda"
        except Exception:
            pass
    return "cpu"


def transcribe_faster_whisper(
    mp3_path: Path,
    *,
    model_size: str,
    language: str | None,
    device: str = "auto",
) -> tuple[str, str]:
    """Transcription via faster-whisper. Retourne (texte, langue)."""
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise RuntimeError(
            "Installez faster-whisper : pip install faster-whisper\n" f"Détail : {e}"
        ) from e

    if device == "auto":
        device = _pick_whisper_device()

    compute_type = "float16" if device == "cuda" else "int8"
    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
    except Exception:
        if device == "cuda":
            model = WhisperModel(model_size, device="cpu", compute_type="int8")
        else:
            raise
    lang_kw = language if language else None
    segments, info = model.transcribe(
        str(mp3_path),
        language=lang_kw,
        beam_size=5,
    )
    parts: list[str] = []
    for seg in segments:
        t = seg.text.strip()
        if t:
            parts.append(t)
    text = "\n\n".join(parts)
    lang_out = info.language or language or "auto"
    return text, lang_out


def transcribe_openai_whisper_module(
    mp3_path: Path,
    *,
    model_size: str,
    language: str | None,
    workdir: Path,
) -> tuple[str, str]:
    """Repli : python -m whisper (package openai-whisper)."""
    workdir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "-m",
        "whisper",
        str(mp3_path),
        "--model",
        model_size,
        "--output_dir",
        str(workdir),
        "--output_format",
        "txt",
        "--verbose",
        "False",
    ]
    if language:
        cmd.extend(["--language", language])
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            "openai-whisper a échoué. Installez : pip install openai-whisper "
            "et ffmpeg (PATH).\n"
            f"Code retour : {e.returncode}"
        ) from e
    txts = sorted(workdir.glob("*.txt"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not txts:
        raise RuntimeError("Aucun .txt produit par whisper.")
    content = txts[0].read_text(encoding="utf-8", errors="replace")
    return content.strip(), language or "auto"


def transcribe_audio(
    mp3_path: Path,
    *,
    model_size: str,
    language: str | None,
    workdir: Path,
    engine: str,
) -> tuple[str, str, str]:
    """
    engine: faster | openai
    Retourne (texte, langue, moteur_utilisé).
    """
    if engine == "faster":
        text, lang = transcribe_faster_whisper(
            mp3_path, model_size=model_size, language=language
        )
        return text, lang, "faster-whisper"
    if engine == "openai":
        text, lang = transcribe_openai_whisper_module(
            mp3_path,
            model_size=model_size,
            language=language,
            workdir=workdir,
        )
        return text, lang, "openai-whisper (python -m whisper)"
    raise ValueError(f"Moteur inconnu : {engine}")


def write_markdown_transcript(
    *,
    out_path: Path,
    url: str,
    title: str,
    video_id: str,
    lang_label: str,
    plain_text: str,
    source_detail: str,
) -> None:
    when = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = f"""# Transcript YouTube — {sanitize_filename(title, 120)}

- **URL** : {url}
- **ID** : `{video_id}`
- **Langue** : {lang_label}
- **Récupéré le** : {when}
- **Source** : {source_detail}

---

## Transcript (texte)

"""
    footer = """

---

## Idées clés (proM7)

> **À compléter par l’assistant** après lecture du transcript : remplacer **tout ce bloc** (titre de section conservé) par **3 à 12 puces** — concepts, méthodes, angles pédagogiques, exemples transférables ; **reformulation** (pas copier-coller du verbatim) ; formulation utilisable pour le **brainstorm** / dispatch leçons.

"""
    out_path.write_text(header + plain_text.strip() + "\n" + footer, encoding="utf-8")


def resolve_whisper_engine(preferred: str) -> str:
    """preferred: auto | faster | openai"""
    if preferred == "faster":
        try:
            import faster_whisper  # noqa: F401
        except ImportError as e:
            raise RuntimeError(
                "Moteur « faster » demandé mais faster-whisper n’est pas installé."
            ) from e
        return "faster"
    if preferred == "openai":
        try:
            import whisper  # noqa: F401
        except ImportError as e:
            raise RuntimeError(
                "Moteur « openai » demandé mais openai-whisper n’est pas installé."
            ) from e
        return "openai"
    try:
        import faster_whisper  # noqa: F401

        return "faster"
    except ImportError:
        pass
    try:
        import whisper  # noqa: F401

        return "openai"
    except ImportError:
        raise RuntimeError(
            "Aucun moteur Whisper trouvé. Installez l’un des paquets :\n"
            "  pip install faster-whisper\n"
            "  pip install openai-whisper"
        )


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None
