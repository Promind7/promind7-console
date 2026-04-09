# Sources — enrichissement des scripts (Parcours stage & emploi)

Ce dossier sert de **dépôt de travail** pour l’humain : documents **FR** ou **EN** à exploiter pour **enrichir** les leçons sans supprimer le contenu déjà rédigé dans `tools/moduleNN_rich_content.py` (et les `.docx` régénérés).

## Fichiers de référence globale

- Synthèse agent + pipeline 4 phases + tableau modules : **`docs/PARCOURS_STAGE_EMPLOI_SYNTHESE_AGENT.md`**
- Registre des sources **déjà utilisées** (à tenir à jour après chaque lot) : **`used_sources_registry.md`**

## Où mettre les brouillons agent (dispatch, analyses)

- **Ne pas** créer dans ce dossier les fichiers de travail de l’agent (tableaux de dispatch, analyses de lot, etc.).
- Les placer sous **`reports/`** — ex. `reports/Sources_dispatch_en_attente.md`, `reports/Sources_concepts_analyse_agent.md`.
- Ici : uniquement **documents déposés par l’humain** à exploiter (FR/EN, citations brutes, transcripts) + les **fichiers de référence** listés ci-dessous.

### Sous-dossier `videos/`

- **Transcripts Whisper** (outil `app/tools/fetch_youtube_transcript.py`) : `videos/transcripts/*.md` ; notes / synthèses optionnelles : `videos/syntheses/`. Voir **`videos/README.md`** et le skill **promind7-veille-youtube-transcription** (Phase 1, sous contrôle de l’agent rédaction).

### Sous-dossier `concepts/`

- **Réservé à tes dépôts** (docx, sous-dossiers type `english quotes/`, etc.). L’agent **ne doit pas** supprimer ce dossier ni y écrire ses brouillons ; voir `concepts/README.md`.

## Règles pour l’agent de rédaction

1. **Lire d’abord** `used_sources_registry.md` : ne **retraiter** que les fichiers **absents** de ce registre (ou explicitement marqués « à réutiliser » par l’humain).
2. **Analyser** chaque nouveau fichier : thèses, exemples, définitions, citations, angles Maroc ou transférables avec prudence.
3. **Proposer un dispatch** : pour chaque idée, indiquer **module + numéro de leçon** (clé `LESSONS` / dossier `NN-…` sous le bon `NN-Module*`) et **où** insérer (nouvelle séquence, nouveau paragraphe dans une séquence existante) — **sans retirer** le texte existant sauf demande explicite de l’humain.
4. **Vue globale** : éviter la redondance lourde entre leçons ; respecter les objectifs par module (skill **promind7-parcours-objectifs**). Penser à la **future banque de tests** (où l’idée pourrait être évaluée).
5. **Citations** : utiliser le fichier **`citations_modele.md`** comme gabarit ; dans le script darija, garder **l’original** (courte) + **version darija** ; citer la source si nécessaire.
6. Après validation humaine des patches : **ajouter** les noms de fichiers sources traités dans `used_sources_registry.md`.

## Formats conseillés pour les dépôts humains

- `.md`, `.txt`, `.pdf` (si extractible), `.docx` dans ce dossier ou sous-dossiers thématiques (`Sources/concepts/`, `Sources/economie/`, `Sources/soft_skills/`, etc.).
- **Vidéos** : transcription automatique **Whisper** → `videos/transcripts/` (commande dans `videos/README.md`) ; à défaut, transcript ou notes en `.md` ; le lien seul = veille **générale** seulement (voir synthèse doc § YouTube).

## Fichier citations

Voir **`citations_modele.md`** : une entrée = source + citation originale + darija + usage suggéré (leçon / type d’accroche).
