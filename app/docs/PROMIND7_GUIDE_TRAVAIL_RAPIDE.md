# proM7 — guide de travail rapide (sans mémoriser tous les fichiers)

**À retenir par cœur :** une phrase (ci-dessous) + ce fichier en pièce jointe ou chemin copié si besoin + **`AGENTS.md`** pour la console.

---

## Une phrase pour tout enchaîner (mode guidé)

Tu peux dire **uniquement** :

> **« Guide-moi proM7. »**  
> (Variantes acceptées : *Guide-moi prom7*, *guide moi pro m7*, etc.)

**Si le parcours est déjà dans le message**, enchaîner directement (ex. *« Guide-moi proM7 pour le parcours Stage & emploi »*).  
**Sinon** — l’assistant **doit d’abord demander** : *« Sur quel parcours veux-tu travailler ? »* (nom exact ou dossier sous `Input/Script/`), et proposer l’option **GLOBAL** / **vague multi-parcours** si l’humain préfère une idée transversale avant de scinder. **Ne pas** lancer E/A/B/C ni créer de fichiers `BRAINSTORM_…` **avant** cette réponse, sauf si l’humain a déjà nommé le parcours.

Optionnel dans la même phrase : *« … pour une vague d’idées multi-parcours »* → dans ce cas, préciser avec l’humain s’il veut **`BRAINSTORM_IDEES_GLOBAL.md`** ou plusieurs parcours à la suite.

**Comportement attendu de l’assistant** (à respecter quand l’humain utilise cette phrase) :

0. **Parcours** : si non précisé, **poser la question** (quel parcours ? ou GLOBAL / multi-parcours ?) et **attendre** la réponse.  
1. **Lire** ce fichier (`PROMIND7_GUIDE_TRAVAIL_RAPIDE.md`) et rappeler **l’ordre des étapes** E → A → B → C → F → G (rappel court). **Pas d’étape D** de validation humaine sur le dispatch : après **C**, enchaînement direct **F** puis **G** (rédaction **V2** avec les idées issues des **vidéos** / **transcripts** et des **documents** `Sources/`).  
2. **Indiquer l’étape courante** et **une seule action concrète** à la fois (fichier à créer ou à ouvrir, commande, ou question de clarification).  
3. **Attendre** la réponse de l’humain avant de sauter à une étape suivante **sauf** si l’humain demande d’enchaîner tout seul.  
4. **Brainstorm (A)** : utiliser `BRAINSTORM_IDEES_<Parcours>.md` ou `BRAINSTORM_IDEES_GLOBAL.md` selon le choix ci-dessus ; proposer **d’abord** la collecte des **transcriptions vidéo** (URLs / playlist → `fetch_youtube_transcript.py` → fichiers sous `Sources/videos/transcripts/`) ; **dans le même fichier `.md`**, compléter la section **`## Idées clés (proM7)`** (puces reformulées, 3–12) après lecture du transcript ; enchaîner le tableau brainstorm en **citant** ces chemins ; compléter avec `Sources/` (hors vidéo) et veille web si utile.  
5. **Après le dispatch (C)** : enchaîner **F** (veille leçon / pipeline 4 phases) puis **G** (script darija + Word **V2**) en **injectant** les idées du tableau dispatch et des sources ci-dessus — sauf demande explicite de l’humain de s’arrêter entre deux étapes.

Si tu préfères **une étape précise** sans repartir de zéro :

*« Suis `app/docs/PROMIND7_GUIDE_TRAVAIL_RAPIDE.md` — on est à l’étape [E/A/B/C/F/G/…]. »*

---

## Tableau par type de tâche

*Ordre d’exécution typique : **E → A → B → C → F → G** (pas d’étape **D** ; après le dispatch, rédaction **V2** = **F** puis **G** avec les idées extraites des vidéos / documents).*

| Phase / tâche | Objectif concret | Où ça vit (fichiers) | Comment demander à l’assistant (exemple) |
|---------------|------------------|----------------------|-------------------------------------------|
| **E — Transcription vidéo** | Audio → Whisper → texte + section **Idées clés** dans le même `.md` | `Input/Script/…/Sources/videos/transcripts/*.md` | `python app/tools/fetch_youtube_transcript.py "URL_ou_PLAYLIST"` — skill **promind7-veille-youtube-transcription** |
| **A — Brainstorm idées** | Consolider idées à partir des **transcripts** + autres sources ; pas encore le script darija | `app/reports/BRAINSTORM_IDEES_<parcours_ou_GLOBAL>.md` + **`Sources/videos/transcripts/*.md`** | *« Phase A »* ou laisser l’assistant te guider après **« Guide-moi proM7. »** |
| **B — Architecture du parcours** | Modules, leçons, ordre, promesse par bloc ; « squelette » avant rédaction | `app/reports/ARCHITECTURE_PARCOURS_<nom>.md` **ou** fiche `app/docs/PARCOURS_<NOM>_BRIEF.md` | *« Phase B architecture : propose une grille module → leçons pour [parcours], cohérente avec promind7-parcours-objectifs ; livrable markdown dans reports/. »* |
| **C — Dispatch idées → leçons** | Chaque idée a une **leçon cible** (ou « à créer ») ; le dispatch est le **plan d’injection** pour **F** et **G**. Sans **F + G**, le tableau ne produit rien dans les scripts. | `app/reports/DISPATCH_IDEES_<parcours>.md` (tableau ID, leçon, source, suivi optionnel) | *« Phase C dispatch : à partir du brainstorm, remplis le tableau ; puis enchaîne F/G pour les leçons ciblées. »* |
| **F — Veille leçon (stade A)** | Phases 1–2–3 du **pipeline leçon** ; intégrer les idées du **dispatch** + **transcripts** + documents `Sources/` pour la leçon concernée. | Pipeline : `.cursor/skills/promind7-pipeline-lecon-4phases` ; trace : `app/docs/veille/MODULE_NN_PIPELINE_4PHASES.md` | *« Mx Ly, stade A ; stop après Phase 3 »* **ou** *« … pipeline complète + patch moduleNN »* |
| **G — Rédaction V2 / correction** | Script darija dans `moduleNN` + régénération Word. **Word V2** (`*-V2.docx`) = sortie **G** quand on distingue l’ancien Word (**V1**). Les **nouvelles idées** (vidéos, docs, dispatch) **entrent** ici dans le texte. | `app/tools/moduleNN_rich_content.py` + `format_moduleNN_scripts.py` | *« Mx Ly »* ou *« stade B restauration leçon … »* — règle **promind7-ecrivain-plateforme** |
| **H — Sources documentaires** | Déposer / suivre ce qui est consommé | `Input/Script/…/Sources/` + **`used_sources_registry.md`** | *« Sources : lire used_sources_registry ; nouveaux fichiers dans Sources/… »* |
| **I — Ops console / Tutor** | Import, apprenants, Cloud, Git | **`AGENTS.md`** (section console) ; code `app/ui/`, `db/` | *« Mode pilote plateforme : [question] »* + skill **promind7-pilote-plateforme** |

---

## Enchaînement recommandé (nouveau parcours ou grosse vague)

1. **E** (si tu as des URLs) : transcriptions → `Sources/videos/transcripts/`  
2. **A** Brainstorm : idées **à partir des transcripts** + autres sources → `reports/BRAINSTORM_…`  
3. **B** Architecture → `reports/ARCHITECTURE_…` ou `docs/PARCOURS_…_BRIEF.md`  
4. **C** Dispatch → `reports/DISPATCH_…`  
5. **F** puis **G** leçon par leçon (ou lot) : **rédaction V2** = intégrer les idées du **dispatch**, des **transcripts** vidéo et des **documents** `Sources/`.

### Dispatch → F → G → Word V2

- **Objectif du dispatch (C)** : **router** chaque idée vers une leçon ; **immédiatement après**, enchaîner **F** (veille / pipeline 4 phases pour la leçon) puis **G** (patch `moduleNN_rich_content.py` + `format_moduleNN_scripts.py`), **sans** étape de validation humaine sur le tableau.
- **Contenu de G** : le darija et le **Word V2** doivent **refléter** les extractions **vidéo** + **documents** + lignes du dispatch pertinentes pour la leçon.
- **Word V2** (`*-V2.docx`) : **sortie de G** dans le dossier leçon. Si les idées **ne sont pas** dans le texte régénéré, le flux **C → F → G** est incomplet.
- **Traçabilité** : colonne **« Remarque intégration »** du dispatch (optionnel) ; mise à jour `MODULE_NN_PIPELINE_4PHASES.md` si lot stade A.

---

## Rôles (rappel)

| Besoin | Rôle | Doc |
|--------|------|-----|
| Vue globale ops / console | Pilote | `PROMIND7_ROLES_ET_ORCHESTRATION.md` |
| Structure & dispatch multi-leçons | Architecte | idem + tableaux `reports/` |
| Texte darija / Word | Écrivain | règle `promind7-ecrivain-plateforme.mdc` |

---

*Les noms de fichiers `BRAINSTORM_…`, `ARCHITECTURE_…`, `DISPATCH_…` sont des conventions proposées ; tu peux les adapter tant qu’ils restent sous `app/reports/` ou `app/docs/` comme indiqué.*

---

## Brainstorm : un fichier par parcours ou un seul pour tout ?

| Approche | Quand l’utiliser | Fichier type |
|----------|------------------|--------------|
| **Par parcours (recommandé par défaut)** | Chaque pack a son public, ses modules et son dispatch ; tu veux éviter le mélange et t’aligner sur `ARCHITECTURE_…` / `DISPATCH_…` du même nom. | `app/reports/BRAINSTORM_IDEES_<NomParcours>.md` (ex. `BRAINSTORM_IDEES_Stage_emploi.md`) |
| **Global (transversal)** | Première passe « fourre-tout » : idées qui peuvent servir **plusieurs** parcours ; tu **dupliques** ou **déplaces** ensuite vers un fichier par parcours. | `app/reports/BRAINSTORM_IDEES_GLOBAL.md` + colonne **« Parcours cible(s) »** dans le tableau |

En pratique : **un brainstorm par parcours** pour le quotidien ; **GLOBAL** seulement si tu fais une séance unique avant de décider comment découper les parcours.
