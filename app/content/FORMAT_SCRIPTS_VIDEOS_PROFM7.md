# Format standard — scripts vidéo (pack Parcours stage & emploi)

**Entreprise** : écrire **proM7** (plus *PM7*, *P7* ni *ProMind7* dans les textes latins).

## Structure obligatoire (fichier Word)

1. **Titre du script**  
   - Un paragraphe, **tout en gras**, police **Calibri 11 pt**.

2. **Objectif**  
   - Titre de section : **`الهدف`** en **gras** + **couleur** (vert dans le gabarit généré).  
   - **Un seul paragraphe** en texte **normal** (Calibri 11 pt), **en arabe uniquement** (intention de la vidéo pour la prod).

3. **Séquences**  
   - Chaque idée = une **séquence**.  
   - **Titre de séquence** : paragraphe **tout en gras** + **couleur distinctive** (bleu dans le gabarit) pour le distinguer du corps du texte.  
   - **Contenu** : paragraphes en **texte normal** noir (citations, listes, dialogues darija, etc.).

4. **Uniformité**  
   - Même police (**Calibri**) et même taille (**11 pt**) pour **tous** les paragraphes (titres = gras, pas une autre taille).  
   - Pas de styles mélangés (éviter titres en « Titre 1 » Word si cela change police/taille) : privilégier **Normal + gras** pour les titres.

5. **Lecture droite → gauche (RTL)**  
   - Pour l’arabe / darija, chaque paragraphe doit avoir la direction **RTL** dans Word (propriétés OOXML `w:bidi` + `w:rtl` sur les runs).  
   - Les scripts générés par `tools/format_parcours_video_scripts.py` l’appliquent automatiquement ; pour les autres `.docx` du pack : `python tools/apply_rtl_all_parcours_docx.py`.

## Application

- Dossier concerné : `Input/Script/Parcours stage & emploi/000-Initiation/`.  
- Pour régénérer les `.docx` à partir des données maintenues dans le dépôt :  
  `python tools/format_parcours_video_scripts.py`
