# Architecture — Parcours **Stage & emploi** (proM7)

**Étape guide** : **B — Architecture du parcours** (`PROMIND7_GUIDE_TRAVAIL_RAPIDE.md`).  
**Date** : 2026-03-24.  
**Statut** : **squelette validable** — à ajuster si le produit renomme des leçons ou ajoute des modules.

---

## 1. Promesse globale (rappel)

- **Public** : étudiant·e **marocain·e**, Bac+1 → Bac+5.
- **But** : cadre + méthode pour lier **formation** et **marché** (économie, entreprise, comportement pro, stage, emploi, numérique, langues) — **sans** promesse de stage/emploi garanti.
- **Référence discours / objectifs modules** : `.cursor/skills/promind7-parcours-objectifs/SKILL.md`.
- **Cartographie technique détaillée** (outillage, `LESSONS`, commandes de format) : `app/docs/PARCOURS_STAGE_EMPLOI_SYNTHESE_AGENT.md` §3.

---

## 2. Fil narratif (ordre pédagogique)

| Ordre | Module | Intention (résumé) |
|------:|--------|-------------------|
| 1 | **00** — Études & mindset | Études ↔ marché, posture, projection |
| 2 | **01** — Économie & marché | Lire le marché (macro, Maroc, positionnement) |
| 3 | **02** — L’entreprise | Fonctionnement, rôles, recrutement vu « futur salarié » |
| 4 | **03** — Attentes comportementales | Soft skills, stress pro, place dans l’orga |
| 5 | **04** — Trouver un stage | Méthodes, types de stage, tuteur, valorisation |
| 6 | **05** — Trouver un emploi | Canaux, CV, entretien, mobilité, contrats |
| 7 | **06** — Outils numériques | Digital, IA, culture data / performance |
| 8 | **07** — Langues | FR / ANG orientés pro et entretien |

**Hors cursus numéroté** : dossier **`000-Initiation`** (accroche / méthode / résultat produit).

---

## 3. Grille module → dossier pack → leçons (`LESSONS` / sous-dossiers)

L’identifiant **stable** d’une leçon = **`NN-Module*`** + **chemin du sous-dossier** (le numéro seul peut se répéter entre modules).

| Module | Dossier sous `Input/Script/Parcours stage & emploi/` | Clés `LESSONS` (numéros de leçon dans `moduleNN_rich_content.py`) | Nombre |
|--------|------------------------------------------------------|-------------------------------------------------------------------|--------|
| 0 | `00-Module 0 - …` | 1–6 | 6 |
| 1 | `01-Module 1 - …` | 9–18 | 10 |
| 2 | `02-Module 2- …` | 20–28 | 9 |
| 3 | `03-Module 3 - …` | 27–32 | 6 |
| 4 | `04-Module 4 - …` | 33–43 | 11 |
| 5 | `05-Module 5 - …` | 44–51 | 8 |
| 6 | `06-Module 6 - …` | 52–56 | 5 |
| 7 | `07-Module 7 - …` | 57–63 | 7 |

**Régénération `.docx`** : voir tableau dans `PARCOURS_STAGE_EMPLOI_SYNTHESE_AGENT.md` (M0 → `format_module00_scripts.py`, M1–M2 → `format_modules_01_02_scripts.py`, M3–M7 → `format_module03_scripts.py` … `format_module07_scripts.py`).

### 3.1 Distinction **M1 L17** vs **M5 L48** (intitulés alignés produit)

| Leçon | Question centrale | Périmètre |
|-------|-------------------|-----------|
| **M1 L17** — *Poursuivre ses études à l'étranger ou au Maroc* | Où **continuer sa formation** (Bac+X, ingénieur, master, spécialisation…) ? | Décision **académique** / parcours d’**études** (visa étudiant, coût, spécialisation, retour…) |
| **M5 L48** — *Travailler à l'étranger ou au Maroc* | Où **exercer** un **emploi** (premier poste, mobilité pro, offre à l’étranger) ? | Décision **emploi** / **contrat** / **vie active** (visa travail, salaire net, famille…) |

Les deux ne répondent pas à la même question ; les ponts dans les scripts **M1** et **M5** le rappellent.

### 3.2 Lettres et messages (sans nouvelle leçon)

Sujets type **lettre de motivation**, **e-mail de candidature**, **message LinkedIn** : traités **dans les leçons existantes**, en priorité **M5 L50** (*CV, lettre de motivation et entretien*), avec renvois lexicaux FR (**lettre de motivation**, **cover e-mail**) dans le corps du script.

---

## 4. Enchaînement avec les autres étapes du guide

| Étape | Livrable | Lien avec cette architecture |
|-------|-----------|------------------------------|
| **E** | Transcripts `Sources/videos/transcripts/` | Idées par thème ; voir colonne « module cible » au **dispatch** |
| **A** | `app/reports/BRAINSTORM_IDEES_Stage_emploi.md` | Tableau S-E-xxx ; croiser avec **§2–3** ci-dessus |
| **B** | **Ce fichier** | Référence pour **C** |
| **C** | `app/reports/DISPATCH_IDEES_Stage_emploi.md` *(créé 2026-03-24)* | Chaque idée → **M + leçon** + statut **proposé** |
| **D** | Validation humaine sur le dispatch | Puis **F/G** (rédaction) |
| **H** | `Sources/used_sources_registry.md` | Après intégration validée dans les scripts |

---

## 5. Nouvelle source documentaire : `Books & pdfs/CareerGuide_Web.pdf`

- **Fichier** : `Input/Script/Parcours stage & emploi/Sources/Books & pdfs/CareerGuide_Web.pdf` (44 p., **2024–2025**).
- **Nature** : guide **Career Development** de **Pittsburg State University** (PSU, Kansas, USA) — services bureau carrière, **Handshake**, checklist par année, auto-évaluation (forces, valeurs, intérêts), entretien (**STAR**), tenue, suivi post-entretien, offres.
- **Usage proM7** : matière **à filtrer** (géographie US, outils type Handshake, références salariales/légales US). **Transposition** Maroc : équivalences **plateformes** école / LinkedIn / salons ; **méthodes** (STAR, recherche entreprise, mock interview) réutilisables en **darija** avec prudence locale.
- **Modules cibles (brouillon pour étape C)** :
  - **M0** : introspection, forces / valeurs / intérêts, plan sur plusieurs années.
  - **M1** : tendances / attentes salariales → **ne pas** importer chiffres US sans source MA.
  - **M3** : compétences, préparation comportementale.
  - **M4–M5** : recherche stage/emploi, entretien, STAR, questions au recruteur, relances.
  - **M6** : profil en ligne, visibilité employeurs (parallèle limité avec Handshake).
  - **M7** : peu de matière directe ; éventuellement formulation **mail** pro en anglais si le guide en contient.

**Registre** : entrée « déposé / en attente de dispatch » dans `used_sources_registry.md` — **pas** marqué comme déjà intégré aux scripts.

---

## 6. Prochaine action recommandée

1. **Valider** ou commenter cette grille (§2–3).  
2. Enchaîner **étape C** : créer ou mettre à jour `app/reports/DISPATCH_IDEES_Stage_emploi.md` en rattachant les idées **S-E-xxx** du brainstorm + les thèmes du **CareerGuide_Web.pdf** aux **M + numéros de leçon** ci-dessus.  
3. Après **D**, rédaction ciblée (**F/G**) leçon par leçon ou par lot.

---

*Document généré pour clôturer l’étape **B** du parcours **Stage & emploi** ; cohérent avec `promind7-parcours-objectifs` et `PARCOURS_STAGE_EMPLOI_SYNTHESE_AGENT.md`.*
