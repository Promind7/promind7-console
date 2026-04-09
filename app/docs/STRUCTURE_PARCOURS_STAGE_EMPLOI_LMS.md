# Parcours « Stage & emploi » — LMS (Tutor) & dépôt V2

> **Schéma global unique** (toutes les étapes : phases, sujets Tutor **#1–#20**, leçons **L1…**, intitulés) :  
> **`D:\01-ProM7-consulting\01-Promind7\ARCHITECTURE_PLATEFORME_PROMIND7.md`** — section **§5.2** (bloc ASCII).  
> **Ne pas dupliquer** ce schéma ici : en cas de changement, **modifier le fichier consulting en premier**, puis ajuster **uniquement** les renvois ou détails techniques ci-dessous si nécessaire.

**Rôle de ce fichier** : compléments **techniques** pour le dépôt `IA\V2` (Tutor, chemins `Input/Script/`, règles pédagogiques) **sans** second arbre ni table « liste plate » parallèle.

---

## 0. Ce qu’il faut aligner

- Dans Tutor, reproduire l’**ordre** et les **libellés** des **20** unités indiquées par **(#n)** dans le schéma consulting §5.2 (parcours du haut vers le bas du bloc).
- Les **jalons** (ex. #2, #8, #14) sont des **sujets** de structuration, pas des modules.
- **Initiation** : scripts sous `000-…` (voir §3) ; ne pas utiliser le vocable « vidéos gratuites » côté public.

---

## 1. Accès large (optionnel — hors les 20 sujets du schéma)

| Élément | Rôle | Technique dépôt |
|--------|------|-----------------|
| **Contenus d’accroche initiale** (pack découverte) | Séquence trailer → questions → orientation → méthode → résultat | `Input/Script/Parcours stage & emploi/000-Initiation/` + `app/tools/format_parcours_video_scripts.py` |
| **Test de connaissance** (accès ouvert) | Diagnostic hors cursus complet — ≠ test — Phase finale (#19) | Quiz Tutor dédié |
| **Live d’ouverture** | Session ouverte à tous | Événement Tutor ou lien externe |

---

## 2. Rappels pédagogiques (détail hors schéma)

### 2.1 Tests de phase (3)

| Test | Portée |
|------|--------|
| **Test — Phase 1 — Le Contexte** | Modules **0, 1 et 2** — après dernière leçon M2, **avant** live phase 1 |
| **Test — Phase 2 — La Préparation** | Modules **3, 4 et 5** — idem |
| **Test — Phase 3 — Langues et outils numériques** | Modules **6 et 7** — idem |

**Distinction** : tests **par module** (fin de M1…M7) = leçons dans les dossiers pack ; **tests de phase** = synthèse inter-modules, **un sujet Tutor** par phase ; **test initiation** (phase 0) et **test accès large** (§1) = autres instances.

### 2.2 Lives de phase (3) + différenciation

| Live | Rôle |
|------|------|
| **Live — Phase 1 — Le Contexte** | Après test phase 1 — Q&R, cas, M0–M2 |
| **Live — Phase 2 — La Préparation** | Après test phase 2 — M3–M5 |
| **Live — Phase 3 — Langues et outils numériques** | Après test phase 3 — M6–M7 |

**Différenciation** : **live d’ouverture** (§1) = accès large ; **live — Phase finale** (#20, §2.3) = clôture du parcours, **après** le test #19 — distinct des trois lives de phase.

### 2.3 Clôture (Phase finale)

| Élément | Rôle |
|--------|------|
| **Test — Phase finale — Parcours Stage & emploi** (#19) | Après live phase 3 (#18) — synthèse **M0–M7** (± initiation si produit le prévoit) |
| **Live — Phase finale — Parcours Stage & emploi** (#20) | Bilan, Q&R, suite / communauté — **après** #19 ; **ne remplace pas** l’évaluation |

---

## 3. Chemins pack (`Input/Script/Parcours stage & emploi/`)

**Titres et ordre des leçons affichés dans Tutor** : **uniquement** le schéma consulting §5.2.  
Ci-dessous : **dossiers racine** par module (noms tels que dans le dépôt).

| Module | Dossier pack |
|--------|----------------|
| *(accroche)* | `000-Initiation` *(réf. technique)* |
| **0** | `00-Module 0 - les études et le mindest` |
| **1** | `01-Module 1 -  l'économie et le marché du travail` |
| **2** | `02-Module 2- L'entreprise` |
| **3** | `03-Module 3 - Les attentes Comportementales` |
| **4** | `04-Module 4 - comment trouver un stage` |
| **5** | `05-Module 5 - comment trouver un emploi` |
| **6** | `06-Module 6 - les outils numériques` |
| **7** | `07-Module 7 - les langues` |

Les sous-dossiers leçon portent des préfixes numériques (ex. `09-…`, `27-…`) : voir l’arborescence Git ; l’alignement **sémantique** avec le schéma §5.2 est fait lors de la production (`moduleNN_rich_content.py`, Word).

**Initiation (phase 0)** : génération scripts vidéo — `app/tools/format_parcours_video_scripts.py` (cf. schéma §5.2 pour les **titres** Tutor des 5 leçons + test).

---

## 4. Règles de cohérence

- **Ordre Tutor** : **20 sujets** — **schéma unique** consulting §5.2 ; **aucune** liste parallèle à maintenir dans ce fichier.
- **Vocabulaire** : ne pas utiliser « vidéos gratuites » en communication ; `000-Initiation` = chemin dépôt seulement.
- **Outils** : cartographie `moduleNN` / Word : `app/docs/PARCOURS_STAGE_EMPLOI_SYNTHESE_AGENT.md` §3.

---

*Dernière mise à jour : 2026-04-05 — consolidation : schéma déporté consulting §5.2, fichier V2 allégé.*
