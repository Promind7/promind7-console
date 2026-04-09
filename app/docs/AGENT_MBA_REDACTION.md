# Agent de rédaction — brief MBA technicien

## Fichiers

| Fichier | Rôle |
|--------|------|
| `content/writer_mba_agent_consignes.md` | Mission, architecture parcours (tests, lives), entrées audio/sources, exemples + web, focus M0–M2. |
| `content/writer_editing_instructions.md` | Style d’édition (clair, pas de tour du pot, concepts simples). |
| `ai/lesson_corpus.py` | Assemble les textes `.docx` du pack selon préfixes de dossiers. |

L’agent charge **`writer_mba_agent_consignes.md`** dans le **system prompt** (comme le guide de style).

## Corpus des leçons (cohérence)

- **Interface** : case **« Corpus leçons M0–M2 (cohérence MBA) »** dans l’onglet Assistant IA.
- **Ou** variable d’environnement **`PROMIND7_WRITER_INJECT_LESSON_CORPUS=1`**.
- **Racine du pack** : par défaut le parcours Stage & emploi (`PROMIND7_STAGE_EMPLOI_SCRIPT_ROOT` ou `Input/Script/Parcours stage & emploi`), sinon **`PROMIND7_MBA_CORPUS_PACK_ROOT`**.
- **Préfixes de chemins** : défaut `00-,01-,02-` → **`PROMIND7_MBA_CORPUS_PREFIXES`** (liste séparée par virgules).
- **Taille max** : **`PROMIND7_MBA_CORPUS_MAX_CHARS`** (défaut 70000).

## Audio

L’app ne transcrit pas l’audio seule : coller la **transcription** ou un **résumé** dans le chat ou en fichier téléversé ; le brief MBA indique à l’IA de reformuler à partir de ce type d’entrée.

## Fil conducteur

Pour analyser le fil conducteur sur **vos** fichiers, les `.docx` doivent être présents sur la machine où tourne Streamlit, avec la case corpus cochée (ou la variable d’env). Le dépôt Git peut ne pas contenir `Input/Script/`.

---

## Rédaction « écrivain plateforme » (Cursor, scripts Module 0)

Agent **autonome** : prompt minimal **`L3`**, **`M0 L5`**, etc. — voir **`AGENTS.md`** et la règle **`.cursor/rules/promind7-ecrivain-plateforme.mdc`** (`alwaysApply`).

Détails : `docs/PROMIND7_ECRIVAIN_PLATEFORME.md` · transcripts : `docs/veille/` · test optionnel : `docs/PROMPT_TEST_LECON_MODULE00_L1.md`
