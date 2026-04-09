# proM7 — rôles, orchestration et agents (méthode de travail)

**Guide opérationnel pas à pas (tableaux par tâche, phrases pour Cursor) :**  
[`PROMIND7_GUIDE_TRAVAIL_RAPIDE.md`](./PROMIND7_GUIDE_TRAVAIL_RAPIDE.md)

**Phrase unique (l’assistant guide les étapes) :** **« Guide-moi proM7. »** (ou *prom7*) — si le **parcours** n’est pas dans le message, l’assistant **demande d’abord** sur quel parcours travailler ; détail dans ce guide.

---

Ce document **matérialise** la vision « plusieurs niveaux d’agents » : en pratique sous Cursor, on parle surtout de **rôles** + **skills** (consignes chargées à la demande ou via règles), pas de sept programmes autonomes séparés. Une **même conversation** peut enchaîner des **sections** (Pilote → Architecte → Rédaction) si tu le demandes explicitement.

---

## 1. Faut-il « splitter » en plein d’agents Cursor ?

**Non comme défaut.** Ce qui se fait de plus sain à ton échelle :

- **Peu de rôles bien définis** (4 à 6), chacun avec un **livrable** et des **sources de vérité** claires.
- **Un fil conducteur** : soit tu ouvres une session avec une **intention** (« console », « architecture parcours X », « leçon M3 L20 »), soit tu demandes un **tour orchestré** (« commence en mode Pilote puis propose le dispatch »).
- **Éviter** 7 agents permanents qui se répondent : perte de contexte, doublons, contradictions. Les **fiches par parcours** + **tableaux dans `app/reports/`** font office de « mémoire » partagée.

Ta hiérarchie (gérant → spécialistes) reste **la bonne carte mentale** ; on la traduit en **skills + docs**, et en **branchements** dans le chat.

---

## 2. Carte des rôles (ta vision, formalisée)

### Niveau A — Pilote / vision plateforme (« bras droit »)

**Mission** : vue d’ensemble produit & ops — ce qui est **dans le dépôt**, la **console** Streamlit, les **données** disponibles (SQLite, export Tutor), les **risques** (cache Cloud, réimport), et des **analyses** sur demande (lecture code + requêtes si tu exposes un export ou un extrait).

**Limites honnêtes** : l’assistant ne « voit » pas magiquement tous les **onglets** du navigateur en direct. Il s’appuie sur : fichiers du repo, sorties de commandes que tu autorises, captures ou exports que tu fournis, et **`app/data/promind7.db`** / **`tutor_lms/`** quand c’est pertinent.

**Mails, rappels, prospection** : pas dans ce dépôt aujourd’hui comme produit fini ; le rôle peut **rédiger** brouillons, relire, structurer des séquences — **branchement** futur (Make, CRM, API mail) = hors scope sauf implémentation dédiée (voir TODO intégrations dans le code).

**Skill** : `.cursor/skills/promind7-pilote-plateforme/SKILL.md`  
**Référence ops** : `AGENTS.md` (section console Tutor / Streamlit).

---

### Niveau B — Architecte parcours (multi-parcours)

**Mission** : cohérence **entre** parcours et **structure** (modules, leçons, taille, futurs tests), **dispatch** des idées (vidéos, Sources, veille) vers **la bonne leçon** ou « à créer », **sans** rédiger tout le script darija sauf demande suivante.

**Artefacts** : tableaux sous `app/reports/` (ex. `ARCHITECTURE_IDEES_<parcours>.md`, dispatch), éventuellement une **fiche par pack** sous `app/docs/` (objectifs, public, périmètre).

**Skills** : **promind7-parcours-objectifs** (cadre) + **promind7-pipeline-lecon-4phases** en mode **arrêt après Phase 3** si tu valides cette règle de travail.

---

### Niveau C — Expert d’un parcours (une « personnalité » par pack)

**Mission** : connaître les **spécificités** du pack (étudiants vs salariés, niveau, ton, contraintes légales / RH, vocabulaire cible). Contenu de référence : scripts existants, `000-Initiation`, `Sources/README.md`, synthèses `app/docs/`.

**Organisation** : pas besoin d’un agent Cursor **séparé par parcours** au départ — **une fiche** `app/docs/PARCOURS_<NOM>_BRIEF.md` (ou équivalent) que l’architecte et la rédaction **lisent en premier**. Quand un pack grossit, tu peux extraire un skill dédié (ex. `promind7-parcours-salarie`) si ça évite la dérive.

---

### Niveau D — Rédaction plateforme (darija, style proM7)

**Mission** : **stades A/B/C**, `moduleNN` / Word, lexique, pipeline 4 phases, Sources — **service transversal** : les autres rôles **s’arrêtent** sur un tableau validé ; la rédaction **exécute** Phase 4 + intégration technique.

**Règle** : `.cursor/rules/promind7-ecrivain-plateforme.mdc` + skills **promind7-ecrivain-plateforme**, **promind7-pipeline-lecon-4phases**, **promind7-veille-youtube-transcription** (transcript).

---

### Niveau E — Production supports (vidéo, visuel, scripts d’accompagnement)

**Mission** : storyboards, checklists tournage, accessibilité, cohérence graphique, **best practices** vidéo court format — **sans** remplacer la rédaction darija des leçons sauf demande.

**Organisation** : **skill à créer** quand tu as 2–3 besoins récurrents (ex. `promind7-production-supports`) ; en attendant, **brief dans le chat** + sortie dans `app/reports/` ou `Input/Script/.../Sources/`.

---

### Niveau F — Marketing & image de marque

**Mission** : posts, tunnels, messages **alignés** promind7-parcours-objectifs (pas de sur-promesse), calendriers éditoriaux, angles **terrain Maroc**.

**Organisation** : **skill à créer** plus tard (`promind7-marketing-proM7`) ; croiser **promind7-parcours-objectifs** pour ne jamais contredire le discours pédagogique.

---

## 3. Comment travailler au quotidien

| Situation | Rôle dominant | Action |
|-----------|----------------|--------|
| « Où on en est sur la console / Tutor ? » | Pilote | Lire `AGENTS.md`, code `app/ui/`, `db/` ; requêtes / export si besoin. |
| « Où ranger cette idée / cette vidéo ? » | Architecte | Mettre à jour un tableau `app/reports/…` ; valider **leçon cible** avant rédaction. |
| « Rédige la leçon 32 M5 » | Rédaction | Règle écrivain + pipeline ; transcript dans `Sources/videos/transcripts/` si vidéo. |
| « Texte LinkedIn + mail relance » | Pilote + Marketing (brouillon) | Pas de vérité unique dans le repo sans fichier dédié — créer un `.md` brouillon si tu veux versionner. |

**Règle d’or** : **une intention par message** ou une phrase du type : *« Tour complet : Pilote (résumé) puis Architecte (dispatch seulement) »*.

---

## 4. Évolution

- Quand un rôle **se répète** avec les mêmes 20 consignes → en faire un **skill** `.cursor/skills/…`.
- Quand une **API** (mail, analytics, paiement) existe → documenter le **connecteur** dans `AGENTS.md` ou ici, plutôt que de promettre un « agent » omniscient sans données.

---

*Dernière mise à jour : alignée sur la vision « gérant + spécialistes » — implémentation par skills et fichiers de vérité dans le dépôt.*
