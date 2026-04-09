# Test « écrivain plateforme » — Module 0, Leçon 1

> **Usage courant** : tu peux simplement écrire **`L1`** ou **`M0 L1`** dans le chat — la règle `promind7-ecrivain-plateforme` (`alwaysApply`) enchaîne la pipeline **sans** copier-coller ce fichier.

**Objectif de ce document** : scénario **détaillé** pour vérifier que l’agent **analyse le fil**, **propose** des idées externes, puis **intègre** sans se limiter à reformuler ta consigne.

**Fichier cible** : `tools/module00_rich_content.py` → clé `1` (`LESSONS[1]`).

**Pré-requis Cursor** : ouvrir `module00_rich_content.py` **ou** demander explicitement le skill **promind7-ecrivain-plateforme** + **promind7-parcours-objectifs**.

---

## Partie 1 — Étape A (chat seul, pas de commit)

Coller :

```text
Rôle : écrivain plateforme proM7 — Étape A uniquement.

Cible : Module 0, Leçon 1 — Introduction au parcours, en particulier la séquence qui présente le sommaire des modules (logique des 3 phases + liste M0–M7 + LIVEs).

1) En 5 puces maximum : où se place cette leçon dans le parcours complet (00→07) et ce que l’étudiant doit déjà savoir / pas encore.
2) Propose 5 idées pédagogiques OU méthodes reconnues qui pourraient enrichir CETTE séquence (ex. « spirale révision », « advance organizer », ancrage mémoire, rappel espacé, lien avec une chaîne YouTube sur l’orientation pro — sans inventer de citation).
3) Choisis les 3 meilleures pour notre public Maroc post-bac ; pour chacune : une phrase « ce qu’on dit face caméra » en darija + une phrase en français si c’est un terme technique.

Contrainte : ne pas réécrire mon message ; ne pas encore modifier les fichiers.
```

**Validation humaine** : tu choisis 1–3 idées, ou tu demandes des variantes.

---

## Partie 2 — Étape B (modification code)

Coller (adapter les numéros d’idées) :

```text
Étape B : intègre les idées [précise 1, 2, 3] dans tools/module00_rich_content.py pour LESSONS[1],
dans la séquence du sommaire (3 phases / modules), sans casser les tuples ("phase1", …) ni le format liste un module par ligne.
Ajoute du texte darija court (paragraphes ou lignes) là où ça aide l’oral — pas de méta-IA.
À la fin de ta réponse, liste « Ajouts veille : … » en 3 bullets.

Je lancerai moi-même : python tools/format_module00_scripts.py
```

---

## Critères de succès du test

- La réponse **Étape A** contient bien une **mini-analyse de fil** + **5 propositions** dont **3 détaillées**.
- L’**Étape B** modifie le Python de façon **lisible** et tu peux **voir** dans le Word que ce n’est pas qu’un synonyme de ta consigne.
- Aucune **statistique** ou **promesse** non autorisée par le brief proM7.

---

## Variante : tester une autre séquence

Remplacer dans Partie 1 : « séquence … » par ex. **Séquence 4** (proM7 + vidéos gratuites) ou **Séquence 2** (pour qui).

Dupliquer ce fichier en `PROMPT_TEST_LECON_MODULE00_L3.md` en changeant `LESSONS[3]` et l’objectif (lacunes techniques).
