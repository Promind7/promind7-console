# Console Streamlit — développement Promind7

Dossier de travail **autonome** pour l’application console (Promind7).  
Les documents produit / architecture validés sont sous `01-Promind7/01-Architecture/` ; **aucun renvoi** à un autre dépôt n’est requis pour faire tourner cette console.

## Lancer l’application

Depuis **ce dossier** :

```bash
pip install -r requirements.txt
streamlit run promind7_console.py
```

## Données attendues à la racine de ce projet

| Élément | Rôle |
|--------|------|
| `tutor_lms/` | Export Tutor LMS décompressé (`courses/` …) — import depuis **Admin** |
| `Input/Script/` | Scripts pédagogiques (autres parcours). Variables : `PROMIND7_SCRIPT_LIBRARY_ROOT`, `PROMIND7_STAGE_EMPLOI_SCRIPT_ROOT` si besoin. **Stage & emploi** : si le dossier `01-Promind7/02-Contenus/01-Scripts/Parcours stage & emploi` existe, il est utilisé **automatiquement** (sans variable). |
| `app/data/promind7.db` | Base SQLite (créée au premier lancement). Variable optionnelle : `PROMIND7_DB_PATH` |

## Copie des scripts Stage & emploi (contenu V2, noms sans `-V2` ni `-darija`)

Depuis la racine de ce projet, avec `PYTHONPATH` pointant vers `app` (ou `pip install -e` équivalent) :

```bash
python app/tools/sync_stage_emploi_scripts_strip_v2.py
```

Source par défaut : `D:\Promind7\IA\V2\Input\Script\Parcours stage & emploi` (surcharge : `PROMIND7_SYNC_SCRIPT_SOURCE`).  
Cible par défaut : `D:\01-ProM7-consulting\01-Promind7\02-Contenus\01-Scripts\Parcours stage & emploi`.

`Lancer_Promind7_Console.vbs` définit `PROMIND7_STAGE_EMPLOI_SCRIPT_ROOT` vers ce dossier cible.

## Rédaction (onglet dédié)

- **Script** : lecture et export des Word ; libellés et nom de fichier téléchargé **sans** `-V2` ni `-darija` (fichiers sources peuvent encore les porter).
- **Architecture** (Stage & emploi uniquement) : arborescence par **phases** (modules en sous-blocs).
- **Vidéos veille** : consolidé Markdown sous `Sources/videos/` du parcours concerné.
- **Sommaire structuré** : retiré pour l’instant ; à reconstruire plus tard.

## CSS

Styles globaux injectés **une seule fois** au démarrage dans `app/promind7_console.py` (`inject_global_styles()`), pas par onglet.
