# Drive, local, Git et déploiement Streamlit — ProMind7

## Principe

- **Git / GitHub** : code Python (`ui/`, `services/`, `ai/`, `db/`, etc.), `requirements.txt`, `PROMIND7_GUIDE.md`, `content/style_guide.md`, `content/writer_style_overrides.md`.
- **Local** : base SQLite (`promind7.db` ou `PROMIND7_DB_PATH`), gros dossiers `Input/`, exports Tutor ZIP, **clés** (`google_token.json`, `.streamlit/secrets.toml`).
- **Google Drive (ou équivalent)** : sauvegardes collaboratives, brouillons, scripts Word, business plan — ce qui est **lourd** ou **non versionné**.

## Quoi mettre sur le Drive (recommandé)

| Sur le Drive | Pourquoi |
|--------------|----------|
| Dossier `Input/` (scripts .docx, bibliographie, statuts PDF) | Partage équipe, sauvegarde, trop lourd pour Git |
| Exports / sauvegardes `promind7.db` (chiffré si sensible) | Backup |
| Copie de `content/redaction_drafts/` | Brouillons générés par l’onglet Rédaction |
| Documents juridiques, factures | Hors application |

## Quoi garder en local (ou secrets cloud uniquement)

| Ne pas commiter sur GitHub | Raison |
|----------------------------|--------|
| `OPENAI_API_KEY` | Secret (`.streamlit/secrets.toml` ou variables d’environnement) |
| `google_credentials.json`, `google_token.json` | OAuth Google |
| `promind7.db` | Données personnelles apprenants |
| `.env` avec secrets | Fuite accidentelle |

Ajoutez un **`.gitignore`** contenant au minimum :  
`.venv/`, `__pycache__/`, `*.db`, `google_token.json`, `google_credentials.json`, `.streamlit/secrets.toml`, `.env`

## Synchroniser `content/` vers le Drive sans API

1. Installez **Google Drive pour ordinateur** (ou équivalent).
2. Notez le chemin du dossier synchronisé (ex. `G:\Mon Drive\`).
3. Lancez :

```powershell
cd D:\Promind7\IA\V2
.\.venv\Scripts\python.exe scripts\sync_to_folder.py --dest "G:\Mon Drive\Promind7_sync"
```

Option pour inclure les scripts source (lourd) :

```powershell
.\.venv\Scripts\python.exe scripts\sync_to_folder.py --dest "G:\Mon Drive\Promind7_sync" --with-input-script
```

Le script recopie `content/` en miroir dans le dossier cible ; Drive propage vers le cloud.

## Déploiement Streamlit (collaborateurs) — prochaine étape

1. Repo **privé** sur GitHub (sans secrets).
2. **Streamlit Community Cloud** : connecter le repo, point d’entrée `promind7_console.py`, secrets `OPENAI_API_KEY`, etc.
3. Base **SQLite** sur le cloud est **éphémère** : pour de la vraie prod multi-utilisateurs, prévoir **PostgreSQL** + stockage fichiers (S3 / Drive API) — à planifier après la V1.

## Clé OpenAI — onglet Rédaction

- **Local** : variable système `OPENAI_API_KEY` ou fichier `.streamlit/secrets.toml` :

```toml
OPENAI_API_KEY = "sk-..."
```

- **Streamlit Cloud** : *Settings → Secrets* (même clé).

Modèle optionnel : variable `PROMIND7_WRITER_MODEL` (défaut `gpt-4o-mini`).
