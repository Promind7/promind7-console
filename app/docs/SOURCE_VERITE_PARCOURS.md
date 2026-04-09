# Source de vérité — parcours et données Tutor LMS

> Document vivant : à fusionner dans une **refonte du PROMIND7_GUIDE** une fois le contenu stabilisé avec l’équipe.

## Structure des parcours (référence officielle)

La **structure des parcours** à suivre pour le produit et la production de contenu est celle définie dans :

**`Input/Architecture cours/Architecture cours.xlsx`**

- Feuille **Parcours** : liste des parcours et publics visés.
- Feuille **Stage & emploi** : détail des modules, leçons, tests, lives, etc.

Toute autre description de parcours (ex. ancien business plan, anciens packs Tutor) est **historique** tant qu’elle n’est pas réalignée sur ce fichier.

## Scripts pédagogiques (rédaction)

- **Seul emplacement** des scripts / brouillons de leçons (Word, etc.) : **`Input/Script/`**.
- Aucun **code** (`.py`, outils) ne doit y être placé : l’arborescence sert au **suivi des parcours** et au contenu, pas aux utilitaires du projet (ceux-ci restent à la racine, ex. dossier `scripts/`).
- Les **versions retravaillées** et fichiers annexes (YouTube, notes) produits depuis l’onglet Streamlit **Stage & emploi** vont sous **`Parcours stage & emploi/_exports/`** (sans modifier les originaux).

## Export ZIP Tutor LMS dans la plateforme (état actuel)

L’export **ZIP Tutor LMS** actuellement importé / visible dans la console **ne reflète pas** encore cette architecture : il contient des **anciens packs**.

**Conséquences :**

- L’arborescence **Packs** dans Streamlit et le miroir `tutor_*` en base peuvent être **décalés** par rapport à la cible pédagogique.
- Les dossiers sous `content/packs/` synchronisés depuis ce ZIP peuvent correspondre à l’**ancienne** offre.

**Action attendue (quand vous serez prêt) :**

1. Mettre à jour le catalogue côté **WordPress / Tutor LMS** selon `Architecture cours.xlsx`.
2. Générer un **nouvel export ZIP** (ou activer la synchro API une fois opérationnelle).
3. Réimporter depuis l’onglet **Admin** et resynchroniser le contenu local.

En attendant, traiter les données « packs » dans l’UI comme **indicatives**, pas comme la vérité finale des parcours.

## Refonte du guide

Une **refonte du `PROMIND7_GUIDE.md`** est prévue pour intégrer :

- cette source de vérité (Excel + lien `content/`),
- l’architecture agents / rédaction,
- le workflow Drive / déploiement,

en cohérence avec ce qui sera rédigé **ensemble** au fil du projet.
