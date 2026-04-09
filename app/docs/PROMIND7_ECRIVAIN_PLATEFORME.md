# Écrivain plateforme proM7 — mode autonome

## Ce que l’humain dit (minimum)

Exemples suffisants pour l’agent :

- `M0 L3` ou `Module 0 leçon 3` ou `leçon 5` (M0 par défaut dans ce repo pour `module00_rich_content.py`).

Optionnel : URL vidéo/podcast, fichier transcript, « priorité séquence 2 », « alléger le ton ».

**L’humain ne doit pas** préciser quel skill ouvrir : la **règle Cursor**  
`.cursor/rules/promind7-ecrivain-plateforme.mdc` (`alwaysApply: true`) + **`AGENTS.md`** décrivent l’agent rédaction pour tout le projet.

---

## Ce que l’agent fait tout seul (ordre)

1. **Cadrage** : lire la leçon dans `tools/module00_rich_content.py`, objectifs dans `.cursor/skills/promind7-parcours-objectifs/SKILL.md`, cohérence avec leçons voisines.
2. **Veille** : docs du repo (`MODULE_00_SOURCES_*`, `SOURCE_VERITE_*`, `docs/veille/`) + **recherche web** si pertinent (méthodes, pas chiffres inventés).
3. **Propositions** : **≥ 3 idées** neuves (pas une paraphrase du message humain).
4. **Rédaction** : **brouillon FR ou EN autorisé** (section séparée), puis **script oral en darija** intégré au Python.
5. **Transcription** : si URL seule → extraire ce qui est fiable ; pour citation précise, **transcript humain ou fichier** dans `docs/veille/` — **pas** de réinvention du contenu vidéo.
6. **Livrable** : modification de `module00_rich_content.py` + rappel `python tools/format_module00_scripts.py`.
7. **Pour relecture** : résumé des ajouts et points à commenter pour l’humain.

---

## Inspiration — biographies membres

- **`Input/Bibliographie/Zaq/`** : biographie et documents de **Zaq** pour caler ton, exemples et posture dans les scripts (autres membres : `Input/Bibliographie/<Nom>/`).
- L’agent doit **consulter** ce dossier quand il rédige ou enrichit du contenu lié à ce profil. Voir aussi `Input/Bibliographie/README.md`.

---

## Fichiers projet

| Fichier | Rôle |
|--------|------|
| `AGENTS.md` | Identité « agent rédaction » + rappel prompt minimal. |
| `.cursor/rules/promind7-ecrivain-plateforme.mdc` | Règle **always on** (sauf pur technique sans contenu). |
| `.cursor/skills/promind7-parcours-objectifs/SKILL.md` | Brief objectifs modules / promesse. |
| `.cursor/skills/promind7-ecrivain-plateforme/SKILL.md` | Référence étendue (optionnelle). |
| `docs/veille/README.md` | Où déposer transcripts / notes. |
| `docs/PARCOURS_STAGE_EMPLOI_SYNTHESE_AGENT.md` | Synthèse **parcours Stage & emploi** : 4 phases, outillage M0–M7, dossier **Sources**, YouTube vs transcript. |
| `Input/Script/Parcours stage & emploi/Sources/README.md` | Dépôt documents FR/EN + registre **sources déjà utilisées** ; enrichissement additif des scripts. |

---

## Checklist qualité (humain après coup)

- [ ] ≥ 3 idées **nouvelles** identifiables.
- [ ] Cohérence fil parcours ; pas de sur-promesse ; **proM7** ; pas de méta-IA dans le script.
- [ ] Darija oral en corps de script ; FR/EN pour termes pro.
- [ ] Sources ou prudence sur les faits chiffrés.

---

## Tests détaillés (optionnel)

`docs/PROMPT_TEST_LECON_MODULE00_L1.md` — utile pour calibration ; **pas** requis au quotidien si tu utilises seulement « L1 ».

---

## Désactiver / réduire la règle

Si une conversation est **uniquement** technique : le modèle doit s’en tenir au **§ Portée** de la règle (ne pas lancer veille).  
Pour désactiver complètement : dans Cursor, désactiver la règle **promind7-ecrivain-plateforme** ou passer `alwaysApply` à `false` dans le `.mdc`.
