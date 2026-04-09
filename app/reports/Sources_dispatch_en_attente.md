# Dispatch enrichissement — en attente d’autres sources (intégration groupée)

**Emplacement** : ce fichier est un **livrable agent / suivi de lot** — il vit sous `reports/`, pas sous `Input/.../Sources/` (réservé aux documents à exploiter).

**Statut** : propositions conservées ; une **partie** a déjà été reflétée dans les commentaires d’en-tête et le contenu de `tools/module00_rich_content.py`, `module01_rich_content.py`, `module02_rich_content.py` — le tableau ci-dessous reste une **réserve** pour les prochains lots.  
À fusionner avec les **futures sources** puis traiter **en un seul lot** (dispatch **C** → **F/G**) selon le calendrier du parcours.

**Sources déjà analysées pour ce fichier** :
- `Input/Script/Parcours stage & emploi/Sources/redaction_contenu_V5.md`
- `Input/Script/Parcours stage & emploi/Sources/Citations/citations_a_classer.txt`
- Analyse concepts (docx) : **`reports/Sources_concepts_analyse_agent.md`** (extraction brute : `reports/sources_concepts_extract.md`)

**Rappel** : avant merge final, relire `Input/Script/Parcours stage & emploi/Sources/used_sources_registry.md` ; après intégration validée, y inscrire tous les fichiers sources consommés.

---

## 1. Idées V5 (`redaction_contenu_V5.md`) — reformuler proM7 (pas ProMind7, pas « médicament », pas sur-promesse ; chiffres type 70 % / coût minute → prudents ou sourcés)

| ID | Idée | Leçon cible | Note insertion |
|----|------|-------------|----------------|
| A | Valeur perçue ≈ technique × posture | M0 L7 ou M1 L14 | 1 paragraphe + micro-exemple prudent |
| B | Benchmark LinkedIn international → un levier prioritaire | M1 L11 | Bloc outil / fin de séquence |
| C | Deux vitesses Maroc (PME vs zones exigeantes) sans chiffre minute inventé | M1 L12 | Terrain |
| D | Atelier 3 offres → mots de posture | M1 L12 ou M1 L18 | Micro-action |
| E | Commodité vs rareté ; remplaçabilité | M1 L15 | Réflexion, pas loi absolue |
| F | Recrutement = risque ; alignement visuel / vocal / verbal | M1 L16 + rappel M5 | Concept M1, appli M5 |
| G | Postes pourvus hors annonce — formulation prudente | M1 L16 | Éviter « 70 % » figé sans source |
| H | Vidéo 1 min sans son + feedback franc | M5 (entretien / image) | Encart entraînement |
| I | Friction d’équipe ; profil « fluide » | M3 L28 (`03-Module 3`) | + question feedback |
| J | SWOT perso ; miser sur forces | M0 L6 ou M3 L27 | Arbitrer répartition |
| K | 4 fondations (darija, terrain, pas par cœur aveugle, pas magie) sans jargon produit ancien | M0 L1 | Synthèse / pont M1 |

---

## 2. Citations prioritaires (`Citations/citations_a_classer.txt`)

| N° | Leçon cible (indicatif) |
|----|-------------------------|
| 21 Buffett | M3 L29 ou M2 L27 |
| 23 Strauss | M4 (stage / attentes) |
| 16 | M3 L31 ou M5 |
| 18 | M7 L60 ou L61 |
| 19 | M3 L28 |
| 20 | M5 ou M7 L56 |
| 24 | M7 L57 |
| 25 | M3 L28 |
| 240 | M7 L60–L62 |
| 242 | M3 L29 ou M1 L16 |
| 168 | M0 L4 |
| 176 | M0 L7 |
| 169 | M0 L6 ou M4 |
| 181 | M0 L5 |
| 218 | M3 L27 ou M5 |
| 234 | M0 L1 ou M1 L17 |
| 239 | M1 L18 ou M5 |
| 241 Bennett | M2 L28 ou M4 |

*Le reste de la liste : réserve tests / accroches ; éviter répétition entre leçons.*

---

## 3. Prochaine étape (quand tu ajoutes des sources)

1. Déposer les nouveaux fichiers sous `Input/Script/Parcours stage & emploi/Sources/` (ou sous-dossiers).  
2. Demander une **mise à jour de ce dispatch** dans `reports/` (fusion avec les nouvelles idées + résolution des doublons).  
3. Valider le tableau unifié → **une seule** vague de patches sur les `moduleNN_rich_content.py` + format + `Sources/used_sources_registry.md`.
