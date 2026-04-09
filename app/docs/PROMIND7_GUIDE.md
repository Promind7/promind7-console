# PROMIND7_GUIDE – Guide Technique Officiel (Version V5)

Ce guide définit les règles **obligatoires** pour toutes les modifications du projet ProMind7, qu’elles soient réalisées par un développeur, GPT, ou Codex.

Il remplace toutes les anciennes versions (dont la V3 compacte `.md`).

---

# 1. Objectifs

- Définir la vision technique commune de ProMind7  
- Standardiser la manière dont GPT/Codex modifient le code  
- Garantir la cohérence entre **UI / Services / DB / AI / Integrations**  
- Préparer l’évolution de l’Agent IA (Étapes 2 → 4)  
- S’assurer que **promind7_console.py ne soit jamais modifié** sauf demande explicite  
- Assurer la continuité pour toutes les futures mises à jour

---

# 2. Architecture Générale

## 📁 ui/
- Uniquement logique **Streamlit**  
- Pas de logique métier  
- Pas d’accès DB direct  
- Affichage, formulaires, interactions utilisateur  

## 📁 services/
- Logique métier  
- Accès BD via `get_connection()`  
- Validations, regroupement de données  
- Aucun Streamlit ici

## 📁 db/
- Schémas SQL  
- Initialisation, migrations  
- Pas de logique métier

## 📁 ai/
- Appels OpenAI  
- Recherche IA (`run_agent_search`)  
- Builders de contexte  
- Profiling et mémoire locale future  
- Pas d’UI

## 📁 integrations/
- Connecteurs externes (Airtable, Make, Webhooks)  
- Synchronisation automatique ou manuelle

## 📄 promind7_console.py
- Point d’entrée Streamlit  
- Définit les onglets  
- **Ne jamais modifier ce fichier**, sauf demande explicite

---

# 3. Règles d'encodage

- UTF-8 obligatoire  
- Pas d’emojis dans le code  
- Labels simples (ASCII)  
- Noms clairs, cohérents  
- Respect strict du linter interne

---

# 4. Règles Codex (obligatoires)

1. Ne jamais modifier `promind7_console.py`  
2. Travailler fichier par fichier  
3. Lire ce guide avant toute modification  
4. Analyser le code existant avant d’écrire  
5. Respect strict de l’architecture (UI ≠ Services ≠ DB ≠ AI)  
6. Pas de modifications globales injustifiées  
7. Aucune logique métier en UI  
8. Tester mentalement les imports circulaires  
9. Proposer toujours ce que l’on va faire avant de le coder  
10. Si un service existe déjà → l’utiliser, ne pas recréer une fonction similaire  

---

# 5. Rôle des onglets Streamlit

### Dashboard
- KPIs  
- Répartition des apprenants  
- Résumé global ProMind7

### Agent IA
- Appels OpenAI  
- Historique des requêtes  
- Analyse d’apprenant (Étape 2 future)  
- Recherche contextualisée

### Team
- CRUD membres d’équipe  
- Champs profil (bio, rôle, etc.)  
- Sécurité sur les suppressions (tâches liées)

### Packs
- Lecture seule des données Tutor LMS synchronisées  
- Modules, leçons, détails du contenu

### Apprenants
- Fiche apprenant  
- Packs associés  
- Recherche / filtre  
- Informations Tutor LMS

### Tâches
- CRUD tâches  
- Assignations  
- Affichage par membre & par pack

### Admin
- Import ZIP Tutor LMS  
- Historique des imports  
- Taille DB  
- Synchronisation & nettoyage contenu

---

# 6. Stratégie IA (Roadmap Officielle)

### Étape 1 — **FAIT**
- run_agent_search()  
- Contexte dynamique  
- Historique inversé  
- Appels réels OpenAI  
- Profil simple

### Étape 2 — **À FAIRE**
- Profils IA persistants  
- Embeddings internes  
- Mémoire à long terme  
- Analyse d’apprenant enrichie

### Étape 3 — **FUTUR**
- Analyse IA du contenu (leçons / modules)  
- Résumés automatiques  
- Classification intelligente

### Étape 4 — **FUTUR**
- IA autonome capable d’agir sur l’interface  
- Suggestions automatisées  
- Actions proactives (ex : création de tâche intelligente)

---

# 7. Workflow Codex Officiel

- Lire le fichier avant modification  
- Modifier **uniquement** le fichier demandé  
- Respecter strictement l'architecture  
- Séparer systématiquement :
  - UI  
  - Services  
  - DB  
  - IA  
  - Integrations  
- Revenir vers l’utilisateur avant d’appliquer :
  - un refactor  
  - un changement impactant plusieurs fichiers  
  - une suppression  
  - une modification dans les services

---

# 8. Bonnes pratiques GPT / Codex

- Toujours proposer les modifications avant de coder  
- Toujours indiquer **où** sera intégré le code  
- Ne jamais inventer des fonctions si un service existe déjà  
- Maintenir un style cohérent  
- Pas de duplication de logique  
- Préférer des composants isolés / modulaires  
- Vérifier qu’un changement UI n’affecte pas d’autres onglets  
- Ne jamais faire d’hypothèse sur le contenu DB  
- Ne jamais utiliser le système de fichiers (sauf zip import)

---

# 9. Règles UX/UI (V5)

- UI minimaliste, lisible  
- Titres hiérarchisés (H1 > H2 > H3)  
- Boutons taille standard  
- Pas de style spécifique dans chaque fichier → utiliser `ui/styles.py`  
- Tous les onglets doivent appeler :  
  ```python
  from ui.styles import inject_global_styles
  inject_global_styles()
  ```

---

# 10. Architecture IA Multi-Agents

Cette section définit l'architecture multi-agents utilisant Gemini.

### Agent Stratège (SQL)
- Responsable de la génération et de l'exécution de requêtes SQL pour récupérer ou analyser des données structurées.
- Utilise la table `ai_style_reference` pour adapter son style de réponse.

### Rédacteur (Fichiers /content)
- Spécialisé dans la lecture et la génération de contenu markdown/texte.
- Opère principalement dans le dossier `/content`.
- **Template Maître** : Utilise une structure stricte (`# TITRE`, `## Objectif Pédagogique`, `## 📝 Contenu`, `## 🔗 Cohérence`) pour toute production.
- **Mode Création Intelligente** : 
    - Analyse automatique des métadonnées du fichier source (`TITRE`, `PACK`, `MODULE`).
    - Proposition d'**Enrichissement** si la leçon existe déjà (fusion intelligente).
- **Administration** :
    - Initialisation automatique de l'arborescence Packs (`content/packs/[slug]__[id]/MASTER_CONTENT_[slug].md`).
    - Archivage des anciens fichiers de brainstorming dans `_OLD_ARCHIVES_`.
- Les nouveaux fichiers sont sauvegardés directement dans l'arborescence du pack (`content/packs/...`).

### Dispatcher (Apprenants/Team)
- Gère l'attribution des tâches et l'interaction avec les profils Apprenants et Membres d'équipe.
- Coordonne les actions entre les différents agents et les services métiers.
