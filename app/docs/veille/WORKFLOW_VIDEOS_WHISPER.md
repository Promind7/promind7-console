# Réussir l’intégration des vidéos (YouTube + Whisper)

Objectif : produire un **fichier `.md`** avec un **transcript réel** (Whisper) que l’agent rédaction peut lire pour la **phase 1** puis la phase 4.

**Emplacement par défaut** :  
`Input/Script/Parcours stage & emploi/Sources/videos/transcripts/`  
(aligné sur le pack Stage & emploi ; voir `Sources/videos/README.md`).

---

## 1. Checklist avant la première utilisation

| Étape | Commande / action |
|--------|-------------------|
| Python | Racine du projet : `pip install -r requirements.txt` + si besoin `requirements-extra.txt` (`yt-dlp`, `faster-whisper`). |
| **ffmpeg** | Obligatoire. Vérifier : `ffmpeg -version`. Sinon Windows : `winget install ffmpeg`, puis **rouvrir le terminal**. |
| Espace disque | Le **premier** lancement Whisper télécharge le modèle (ex. `base`). |

---

## 2. Commande principale

À la racine du dépôt (`V2`) :

```text
python app/tools/fetch_youtube_transcript.py "https://www.youtube.com/watch?v=XXXX"
```

- **Une vidéo** ou **playlist** : traitement **séquentiel** (`[1/N] OK …`).
- **`--max-videos 5`** : limite (tests).
- **`--no-playlist`** : avec `watch?v=…&list=…`, ne traiter **que** la vidéo courante.

Variantes utiles :

```text
python app/tools/fetch_youtube_transcript.py "URL" --list-subs
python app/tools/fetch_youtube_transcript.py "URL" --whisper-lang fr --whisper-model small
python app/tools/fetch_youtube_transcript.py "URL" --output-dir app/docs/veille
```

- **`--whisper-model`** : `tiny` (test) → `base` (défaut) → `small` / `medium` (meilleure qualité).
- **`--whisper-lang fr`** : utile si la vidéo est surtout en français ; vide = **détection auto**.

---

## 3. GPU (optionnel, Windows)

Par défaut le script utilise le **CPU** (évite les erreurs CUDA incomplètes).

Pour tenter le **GPU** :

```text
set YT_VEILLE_USE_CUDA=1
python app/tools/fetch_youtube_transcript.py "URL"
```

---

## 4. Après le téléchargement : lier la vidéo à une leçon

1. Noter le chemin du `.md` affiché (`OK …/Sources/videos/transcripts/….md`).
2. Optionnel : synthèse sous **`Sources/videos/syntheses/`** ou section `## Synthèse` dans le `.md`.
3. Demander à l’agent : intégration leçon en citant ce fichier.

Sans ce fichier, l’agent **ne peut pas** citer fidèlement l’oral de la vidéo.

---

## 5. Dépannage

| Problème | Piste |
|----------|--------|
| `ffmpeg est introuvable` | Installer ffmpeg et vérifier le **PATH** (nouveau terminal). |
| `yt-dlp` / extraction YouTube | `pip install -U yt-dlp`. Notes yt-dlp (runtime JS) si besoin. |
| `Aucun moteur Whisper` | `pip install faster-whisper` ou `pip install openai-whisper` puis `--whisper-engine openai`. |
| Transcription vide / très courte | `--whisper-lang`, modèle plus grand, vérifier l’audio téléchargé. |
| Playlist partielle | Vérifier les entrées privées / supprimées ; consulter les lignes `FAIL` dans la console. |

---

## 6. Cadre légal

Respecter les **conditions d’utilisation** de YouTube et les **droits** sur le contenu.
