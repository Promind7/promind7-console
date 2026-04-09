# Veille — transcripts & notes pour l’agent rédaction

Ce dossier reste utile pour **notes**, **exports manuels** ou **archives** de transcripts.

**Transcription YouTube automatisée (Whisper)** : sortie **par défaut** sous  
`Input/Script/Parcours stage & emploi/Sources/videos/transcripts/`  
(voir **`Sources/videos/README.md`** et le skill **promind7-veille-youtube-transcription**).

**Convention suggérée** (fichiers déposés ici à la main) : `YYYY-MM-sujet-source.md`  
Contenu : lien vers la vidéo/podcast + **transcript** ou **notes détaillées** (timestamps optionnels).

L’agent est instruit de **ne pas inventer** le contenu exact d’un média non fourni.

## Outil : `app/tools/fetch_youtube_transcript.py`

**Pipeline détaillé** : **`WORKFLOW_VIDEOS_WHISPER.md`** dans ce dossier.

Commande typique à la racine du projet (`V2`) :

```bash
python app/tools/fetch_youtube_transcript.py "URL_YOUTUBE_OU_PLAYLIST"
```

- **Playlist** : les vidéos sont traitées **l’une après l’autre**.
- **`--no-playlist`** : une seule vidéo si l’URL contient `list=`.
- **`--output-dir app/docs/veille`** : écrire les `.md` ici au lieu de `Sources/videos/transcripts/`.

Sous Windows : `powershell -File app/tools/youtube_to_veille.ps1 "URL"`.

### Prérequis

- **Python** : `pip install -r requirements.txt` et `requirements-extra.txt` si besoin (`yt-dlp`, `faster-whisper`).
- **ffmpeg** dans le **PATH** (obligatoire pour l’audio).  
  Ex. Windows : `winget install ffmpeg`

### Whisper

- **`--whisper-model`** : `tiny` → `base` (défaut) → `small` / `medium` / `large-v3`.
- **`--whisper-lang fr`** : forcer la langue ; vide = détection auto.
- **`--whisper-engine`** : `auto` | `faster` | `openai`
- **`--list-subs`** : affiche les langues de sous-titres sur la **1re vidéo** (debug uniquement ; le transcript produit est **Whisper**, pas les sous-titres).

Caches : `docs/veille/_cache_*` si `--output-dir` pointe ici ; sinon sous `Sources/videos/_cache_*` (voir `.gitignore`). Sans `--keep-audio`, le MP3 est supprimé après transcription.

### Si tout échoue

Transcript **manuel** ou autre service ASR → fichier `.md` dans ce dossier ou dans `Sources/videos/transcripts/`.

Respecter les **conditions d’utilisation** de YouTube et les droits sur le contenu.

### Exemples historiques (générés avec d’anciennes options)

- `I8nwNcCfyig_en_Introduction_to_the_Business_Model_Canvas.md` — [Introduction to the Business Model Canvas](https://www.youtube.com/watch?v=I8nwNcCfyig)
- `QoAOzMTLP5s_en_Business_Model_Canvas_Explained.md` — [Business Model Canvas Explained](https://www.youtube.com/watch?v=QoAOzMTLP5s)
- `nZndv4HLVIg_en_Harvard_i-lab_Startup_Secrets_Part_3_Business_Model_-_Michael_Skok.md` — [Harvard i-lab — Business Model](https://www.youtube.com/watch?v=nZndv4HLVIg)
