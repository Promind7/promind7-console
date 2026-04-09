# Vidéos → idées (Phase 1 parcours)

Dossier **dédié aux contenus issus de vidéos** (veille YouTube) pour alimenter les scripts **Stage & emploi**, sous la responsabilité de l’**agent rédaction** (Phase 1 du skill **promind7-pipeline-lecon-4phases**).

## Structure

| Élément | Rôle |
|--------|------|
| **`transcripts/`** | Fichiers `.md` générés par `app/tools/fetch_youtube_transcript.py` : **transcript brut** + section **`## Idées clés (proM7)`** à remplir par l’assistant (puces après lecture). |
| **`syntheses/`** | Notes courtes, synthèses d’agent ou humain par vidéo (optionnel) — à lier au nom du fichier transcript ou à l’ID YouTube. |
| **`_cache_audio/`**, **`_cache_whisper_openai/`** | Caches techniques (ignorés par Git) — ne pas versionner. |

## Commande

Depuis la racine du dépôt `V2` :

```bash
python app/tools/fetch_youtube_transcript.py "URL_VIDEO_OU_PLAYLIST"
```

- **Playlist** : les vidéos sont traitées **une par une** dans l’ordre.
- **`--no-playlist`** : si l’URL contient `list=`, ne traiter que la vidéo courante.
- **`--max-videos N`** : limite (tests ou extraits de playlist).

Détails : skill **`.cursor/skills/promind7-veille-youtube-transcription/SKILL.md`**.

## Registre sources

Après exploitation dans les leçons, suivre **`../used_sources_registry.md`** (comme pour le reste de `Sources/`).
