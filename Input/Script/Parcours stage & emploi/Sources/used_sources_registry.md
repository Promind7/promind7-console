# Registre des sources déjà exploitées (Parcours stage & emploi)

**Rôle** : éviter que l’agent **repropose** le même enrichissement à partir d’un fichier déjà traité.  
**Mise à jour** : après chaque lot d’intégration validé, ajouter une ligne (fichier ou URL + date ou référence courte).

## Format des entrées

- `YYYY-MM-DD — chemin relatif depuis Sources/ ou URL — notes optionnelles`

## Entrées

- **2026-03-24** — `Books & pdfs/Code-du-Travail-Maroc.pdf` — **Analysé** pour **dispatch** (`app/reports/DISPATCH_IDEES_Stage_emploi.md`, IDs **CT-MA-001** à **CT-MA-012**) : repères **entrée vie pro** (définitions, essai, hiérarchie des normes, droits mini **formation-insertion** / apprentissage, prescription, travailleurs **étrangers** au MA). **Non intégré** aux scripts tant que **D** non validé ; **recouper** texte **officiel** pour chiffres & articles modifiés.

- **2026-03-24** — https://www.stagiaires.ma/stage-emploi-type-stage — Page d’information **Types de stages au Maroc** (libellés usuels sur la plateforme : **PFE**, **pré-embauche**, **observation**, etc.). **Non intégré** aux scripts : matière pour **M4** (lecture d’offre, attentes selon le **type** de stage) ; croiser **convention** / **école** et textes **locaux** ; chiffres « nombre d’offres » sur le site **non** repris sans date de capture.

- **2026-03-23** — `concepts/` (dossier *critical thinking* et pack associé : docx pensée critique, etc., déposés par l’humain) — **Déjà exploité** dans les scripts : **M0** (تفكير نقدي / critical thinking : source, biais, comparaison) ; **M1** (tendances / marché, rappel vérification de source) ; **M2** (rappels de cohérence avec le lot) ; **M3** L28 (تفكير نقدي خفيف, cadre hiérarchique). Idées reformulées en darija ; pas d’URL US du document source dans les scripts. Croiser **reports/Sources_concepts_analyse_agent.md** et **reports/sources_concepts_extract.md**.

---

## État des fichiers présents dans `Sources/` (hors registre daté)

Pour chaque fichier ou lot : une entrée datée ci-dessus = trace d’exploitation. Les fichiers **non** mentionnés restent à traiter ou à préciser (le registre fait foi).

| Fichier / dossier | Nature | Remarque |
|-------------------|--------|----------|
| `README.md` | Méta | Référence, pas une « source » à cocher |
| `used_sources_registry.md` | Méta | Ce fichier |
| `citations_modele.md` | Gabarit | Référence pour forme des citations |
| `redaction_contenu_V5.md` | Source humaine | Analysée ; dispatch / scripts = intégration **partielle** selon lots (voir `reports/Sources_dispatch_en_attente.md`) |
| `Citations/citations_a_classer.txt` | Source humaine | Idem ; liste encore exploitée comme réserve |
| `concepts/` | Dépôt humain | Docx, images, sous-dossiers (ex. critical thinking, `english quotes/`) — **ne pas supprimer**. Lot *critical thinking* : voir **entrée datée** ci-dessus + analyse `reports/Sources_concepts_analyse_agent.md` ; extract `reports/sources_concepts_extract.md`. |
| `Books & pdfs/CareerGuide_Web.pdf` | PDF (PSU, USA, 2024–2025) | **Déposé 2026-03-24** — **non intégré** aux scripts. Checklist carrière, Handshake, STAR, entretien, etc. Voir **`DISPATCH_IDEES_Stage_emploi.md`** (PSU-CG-001…008). Retirer de cette ligne « en attente » après intégration validée + **entrée datée** § Entrées. |
| `Books & pdfs/Code-du-Travail-Maroc.pdf` | PDF (Loi 65-99, texte structuré) | **Dispatch** **CT-MA-001…012** dans `app/reports/DISPATCH_IDEES_Stage_emploi.md` ; entrée datée § **Entrées**. **Intégration scripts** en **F/G** après dispatch (voir `app/docs/PROMIND7_GUIDE_TRAVAIL_RAPIDE.md`). |
