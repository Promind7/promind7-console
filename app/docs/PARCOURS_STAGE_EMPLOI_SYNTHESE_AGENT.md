# Parcours « Stage & emploi » — synthèse pour l’agent (état du dépôt + pipeline + étape Sources)

Document de référence pour un **agent de rédaction proM7** : ce qui a été construit, **les 4 phases** de veille/rédaction, l’**outillage** technique, puis la **phase suivante** (dossier `Sources/` : enrichissement **sans effacement** du contenu existant).

---

## 1. Objectif du pack

- **Public** : étudiant·e marocain·e, post-bac (Bac+1 → Bac+5), ton terrain Maroc.
- **proM7** : méthode, lucidité, posture — **pas** de promesse de stage/emploi garanti ; nom d’entreprise **proM7** (pas ProMind7 / PM7 dans le neuf).
- **Lexique scripts** : diplôme → **الديبلوم** / **التأهيل الرسمي** (éviter **ورقة** pour le titre) ; grille 2 axes → **جدول** plutôt que **مصفوفة** (voir skill **promind7-parcours-objectifs**).

---

## 2. Les 4 étapes (pipeline stade A — promind7-pipeline-lecon-4phases)

Pour une **leçon** ou un **lot** en rédaction de fond, l’agent enchaîne :

| Phase | Contenu | Contrainte clé |
|-------|---------|----------------|
| **1 — YouTube** | Requêtes **FR + EN** ; tableau d’URLs + pertinence ; idées exploitables depuis titre/description/chapitres | **Ne pas** inventer l’oral fidèle d’une vidéo sans **transcript** (voir § YouTube ci-dessous). |
| **2 — Web** | Articles, guides, références institutionnelles ; idem **FR + EN** pour l’exploration | Pas de chiffres/études inventés ; prudence Maroc vs générique international. |
| **3 — Idées catégorisées** | Fusion YouTube + web + docs internes ; étiquettes (concept, méthode, exemple Maroc, risque, formulation…) | Servir de base à la rédaction ou au **dispatch** vers plusieurs leçons (voir § Sources). |
| **4 — Rédaction** | Darija oral pour les paragraphes ; termes **FR/EN** pro entre parenthèses si besoin | Intégration dans `moduleNN_rich_content.py` et/ou `.docx` selon le module ; respect structure séquences (souvent **Synthèse / pièges / pont** avant **الخاتمة**). |

**Veille déjà consignée par module** : `docs/veille/MODULE_00_PIPELINE_4PHASES.md` … `MODULE_07_PIPELINE_4PHASES.md` (phases 1–3 + rappel phase 4 / commande de format).

**Docs internes récurrents** : `docs/SOURCE_VERITE_PARCOURS.md`, `docs/veille/`, `docs/PROMIND7_ECRIVAIN_PLATEFORME.md`, biographies `Input/Bibliographie/<Membre>/`.

---

## 3. Cartographie technique du parcours (scripts riches → Word)

Chaque module migré a un fichier **`tools/moduleNN_rich_content.py`** avec un dictionnaire **`LESSONS[numéro]`** (`cadre_lignes`, `objectif_ar`, `sequences`).

| Module | Dossier pack | Fichier contenu | Régénération `.docx` | Clés `LESSONS` (numéros de dossier sous le module) |
|--------|----------------|-----------------|----------------------|---------------------------------------------------|
| 0 | `00-…` | `module00_rich_content.py` | `python tools/format_module00_scripts.py` | 1–6 |
| 1 | `01-…` | `module01_rich_content.py` | `python tools/format_modules_01_02_scripts.py` | 9–18 |
| 2 | `02-…` | `module02_rich_content.py` | idem | 20–28 |
| 3 | `03-…` | `module03_rich_content.py` | `python tools/format_module03_scripts.py` | 27–32 |
| 4 | `04-…` | `module04_rich_content.py` | `python tools/format_module04_scripts.py` | 33–43 |
| 5 | `05-…` | `module05_rich_content.py` | `python tools/format_module05_scripts.py` | 44–51 |
| 6 | `06-…` | `module06_rich_content.py` | `python tools/format_module06_scripts.py` | 52–56 |
| 7 | `07-…` | `module07_rich_content.py` | `python tools/format_module07_scripts.py` | 57–63 |

**Note produit** : les préfixes numériques des dossiers (`27-`, `28-`, …) **se répètent entre modules distincts** (ex. M2 et M3 ont chacun un `27-…`). L’identifiant unique est **`NN-Module*` + chemin du sous-dossier**, pas le seul chiffre.

**M1/M2** : le script de format **n’interprète pas** les marqueurs `**…**` dans le texte (tout est écrit en style normal). Les modules **3 à 7** convertissent `**` en gras Word via leur script de format.

Le pack contient aussi **`000-Initiation`** (scripts d’accroche, hors cursus module 00–07).

**Structure LMS Tutor (ordre #1–#20, phases, leçons)** — **schéma unique** : fichier consulting **`ARCHITECTURE_PLATEFORME_PROMIND7.md` §5.2** (chemin local ProM7 consulting). Complément technique dépôt (chemins `Input/Script/`, règles) : **`app/docs/STRUCTURE_PARCOURS_STAGE_EMPLOI_LMS.md`** — **sans** dupliquer le schéma.

---

## 4. Étape suivante — dossier `Sources/` (enrichissement piloté)

**Emplacement** : `Input/Script/Parcours stage & emploi/Sources/`

**Objectif** : l’humain y dépose des **documents FR/EN** (+ éventuellement transcripts, exports). L’agent :

1. **Scanne** `Sources/` et lit **`used_sources_registry.md`** (ou équivalent) pour savoir ce qui est **déjà consommé**.
2. Ne travaille **que sur les sources nouvelles** (fichiers non listés comme utilisés).
3. **Analyse** le contenu (concepts, exemples, formulations, citations exploitables).
4. Propose un **dispatch** : quelle idée va dans **quelle leçon** (par module + numéro de dossier / clé `LESSONS`), sous forme de **patch incrémental**.
5. **N’efface pas** les idées déjà présentes dans les scripts : **ajout** de séquences ou de paragraphes dans le flux pédagogique, ou reformulation **additive** ; en cas de tension, signaler le choix dans « Pour relecture » plutôt que d’écraser.
6. **Citations** : si le pack inclut un fichier dédié (voir `Sources/README.md` et `citations_modele.md`), toute citation utilisée dans un script doit conserver la **formulation originale** et proposer une **traduction / adaptation en darija** (oral) pour l’accroche ou la leçon — sans déformer le sens ; crédit/source si requis.
7. **Vue globale du parcours** : garder la cohérence **M0→M7**, objectifs par module (skill objectifs), **éviter les doublons** massifs entre leçons ; cette vue servira plus tard pour l’**élaboration de tests** (l’agent doit pouvoir s’y référer).

**Après intégration validée** : mettre à jour **`used_sources_registry.md`** (liste des fichiers sources traités + date ou référence conversation) pour que les prochains tours ne **retraitent** pas les mêmes fichiers par erreur.

**Détail opérationnel** : `Input/Script/Parcours stage & emploi/Sources/README.md`.

---

## 5. YouTube : lien seul vs transcription

| Ce que fournit l’humain | Ce que l’agent peut faire en toute sécurité |
|-------------------------|---------------------------------------------|
| **Lien seul** | Métadonnées (titre, description, chaîne), orientation thématique, **reformulations générales** du type d’idée abordée — **sans** prétendre retranscrire la vidéo. |
| **Transcript / sous-titres** (fichier dans `docs/veille/` ou `Sources/`, ou collage) | Citations et idées **ancrées** sur des passages réels ; meilleur dispatch précis. |

**Recommandation** : pour un enrichissement **fin** (citations, nuances, exemples précis), fournir **transcription ou export de sous-titres**. Le lien seul reste **utile** pour la phase 1 (angles, comparatif de vidéos), insuffisant pour du contenu **détail à la phrase près**.

---

## 6. Rappel commandes utiles

- Formats : voir tableau §3.
- **Ne pas écraser** les dossiers de sauvegarde externes ; réimport M1/M2 documenté dans `AGENTS.md`.

---

*Dernière mise à jour conceptuelle : alignée sur l’outillage M0–M7 + workflow Sources incrémental.*
