# Scripts pédagogiques (Streamlit)

## Onglet **Rédaction & scripts**

- **Assistant IA** : sous-onglet dédié.
- **Un sous-onglet par pack** sous `Input/Script/`.

### Navigateur de leçons (interface allégée)

- Liste des fichiers **`.docx`** uniquement (hors `Sources/`, `V2/`, `_exports/`, ancien `Textes_ameliores/`).
- Choix : **Module**, puis **Leçon**.
- **V1** : pour un **`.docx`**, aperçu **HTML** reprenant **gras, couleurs et ordre des paragraphes/tableaux** comme dans Word ; **RTL** appliqué automatiquement (comme le document). Si la conversion échoue, retour au texte brut. Les **`.md` / `.txt`** restent en texte formaté simple (également RTL pour cohérence avec les scripts arabe/darija).
- **V2** : zone d’édition ; le contenu est enregistré dans **`V2/<même chemin relatif que le .docx>.md`** (UTF-8). Le Word **V1** n’est pas modifié. Bouton **Enregistrer V2**.
- Sous V2, repliable **« Proposition IA → fichier V2 »** : génère une V2 avec l’agent (clés API), option corpus M0–M2 du **pack courant** et recherche web, puis **écrit directement** le `.md` V2 sur le disque.

Exemple : `00-Module 0/Lecon.docx` → fichier V2 : `V2/00-Module 0/Lecon.md`.

### Sources (hors interface)

- Vous pouvez toujours ranger les documents de référence sous **`Sources/`** à la racine du pack ; ils ne sont plus listés dans cette vue.

## Variables d’environnement (optionnelles)

- `PROMIND7_SCRIPT_LIBRARY_ROOT`, `PROMIND7_STAGE_EMPLOI_SCRIPT_ROOT`.

## Ancien dossier `Textes_ameliores/`

- N’est plus utilisé par l’UI ; vous pouvez recopier les `.md` vers **`V2/`** en gardant la même arborescence.
