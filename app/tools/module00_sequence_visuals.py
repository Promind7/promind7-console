# -*- coding: utf-8 -*-
"""
Support visuel proposé en **fin de chaque séquence** du Module 0 (tournage / slide).

- Clé : (numéro_leçon 1..7, index séquence 0..n-1) — même ordre que ``LESSONS[n]["sequences"]`` dans ``module00_rich_content.py``.
- Contenu : texte **production** (FR) — idée d’écran, éléments à dessiner ; l’orateur peut s’appuyer dessus pour alléger l’oral.
- Les diagrammes Mermaid restent hors Word ; indiqués quand utile pour Figma / Excalidraw / export image.

Si l’ordre des séquences change dans ``module00_rich_content.py``, mettre à jour les clés ici.
"""

from __future__ import annotations

VISUEL_FIN_SEQUENCE: dict[tuple[int, int], str] = {
    # ——— Leçon 1 ———
    (1, 0): (
        "**Écran** : « De la mentalité étudiant → employabilité ».\n"
        "**Schéma** : une flèche large **طالب** → **موظف واجد (Talent)** ; bandeau bas **Bac+1 → Bac+5**.\n"
        "**À dire** : une phrase — le reste sur le visuel."
    ),
    (1, 1): (
        "**Écran** : « Pour qui ? » — 3 colonnes ou 3 pictogrammes.\n"
        "**Contenu** : (1) début de parcours / tronc commun (2) spécialisation (3) recherche stage ou emploi.\n"
        "**But** : montrer l’hétérogénéité sans relire la liste à l’oral."
    ),
    (1, 2): (
        "**Écran** : carte des **3 phases** (cœur de la leçon 1).\n"
        "**Schéma** : 3 bandes ou escaliers empilés — **1. السياق** (M0–M2 + LIVE 1) → **2. الاستعداد** (M3–M5 + LIVE 2) → **3. الأدوات واللغات** (M6–M7).\n"
        "**Note** : garder les noms de modules lisibles ; le présentateur pointe du doigt au lieu de tout énumérer.\n"
        "*Mermaid (hors Word)* : trois nœuds horizontaux ou verticaux avec sous-listes modules."
    ),
    (1, 3): (
        "**Écran** : rappel **proM7** en 3 pictos.\n"
        "**Schéma** : Darija (oral) → FR/EN (clés pro) ; puis **✓ méthode** vs **✗ pas de promesse emploi/stage**.\n"
        "**Pont** : phrase courte « M0 suite → M1 = سياق » sur la même slide ou slide suivante."
    ),
    (1, 4): (
        "**Écran** : mini-récap **تلخيص / أغلاط / جسر**.\n"
        "**Schéma** : les 3 phases en une ligne ; **piège** : icône « lire les modules sans rattacher à une phase ».\n"
        "**J** : flèche vers **Leçon 2 — الدراسات**."
    ),
    (1, 5): (
        "**Écran** : consignes **micro-action** en pictos.\n"
        "**Schéma** : triangle **سياق / استعداد / أدوات** + case « quel module m’aide maintenant ? ».\n"
        "**But** : pas de texte long à lire ; l’oral se limite à l’intention."
    ),
    # ——— Leçon 2 ———
    (2, 0): (
        "**Écran** : « Pourquoi on se sent ‚tordu‘ après le bac ? »\n"
        "**Schéma** : petits facteurs autour d’un étudiant — **famille**, **pairs**, **notes**, **الديبلوم vu comme أمان** ; centre : **« عادي »**.\n"
        "**À dire** : une phrase rassurante ; le visuel porte le contexte marocain."
    ),
    (2, 1): (
        "**Écran** : **الديبلوم = بوابة** vs **السوق = يطلب دليل**.\n"
        "**Schéma** : deux colonnes — porte ouverte (titre diplôme) / loupe sur **preuves** (projets, TP, langue).\n"
        "**But** : éviter de répéter les définitions à l’oral."
    ),
    (2, 2): (
        "**Écran** : **صندوق أدوات** + **Pivot**.\n"
        "**Schéma** : boîte à outils (icônes visibles + invisibles) ; flèche latérale **Pivot** vers nouveau chemin + **portfolio**.\n"
        "*Mermaid* : Toolbox -- Pivot --> Nouvelle trajectoire."
    ),
    (2, 3): (
        "**Écran** : **Même diplôme — deux trajectoires**.\n"
        "**Schéma** : bifurcation — **en attente** vs **preuves** (projet, stage été, langue) → **جاهز** plus tôt.\n"
        "**But** : image forte, peu de mots au micro."
    ),
    (2, 4): (
        "**Écran** : rôle **proM7**.\n"
        "**Schéma** : pont / raccourci **méthode** ; pas de **baguette magique** (icône barrée).\n"
        "**Une ligne** : effort + apprentissage continu + marché incertain."
    ),
    (2, 5): (
        "**Écran** : synthèse **mindset** (plusieurs sous-idées).\n"
        "**Schéma** : 3 cartes **(1) حدود / صحة وعائلة (2) mindset = réglages (3) forces · intérêts · valeurs** avec icônes.\n"
        "**Rappel** : lien visuel depuis « ne pas se comparer aux réseaux » vers « rester lucide sur ses limites » (pont déjà dans le script).\n"
        "**Option** : 3 slides courtes au lieu d’une si la densité est trop forte."
    ),
    (2, 6): (
        "**Écran** : **جدول 2 axes** (اهتمام × واقع السوق).\n"
        "**Schéma** : grille vide modèle + exemple d’une cellule « force / manque / action ce mois ».\n"
        "**But** : le tableau remplace une explication longue du cadre."
    ),
    (2, 7): (
        "**Écran** : **synthèse + pièges + pont L3**.\n"
        "**Schéma** : **دبلوم + دليل** ; piège **Nom de filière ≠ preuve** ; flèche **L3 — النواقص**.\n"
        "**Une slide** ou trois blocs empilés."
    ),
    (2, 8): (
        "**Écran** : **14 jours — preuve** + une ligne **CV**.\n"
        "**Schéma** : deux cases à cocher ou mini checklist.\n"
        "**But** : fin de leçon dynamique sans relecture des consignes."
    ),
    # ——— Leçon 3 ———
    (3, 0): (
        "**Écran** : **zone de confort** — exemple **méca vs élec**.\n"
        "**Schéma** : matière « facile » en surbrillance vs **trou** (cours non travaillé) — trou grossit = risque.\n"
        "**Icon** : alerte sur le **trou**."
    ),
    (3, 1): (
        "**Écran** : **عقلية الليسي** vs **الحرفة** + **الساس والسوسة**.\n"
        "**Schéma** : bâtiment — **fondation** avec niche (petit animal) ; si la niche grossit, l’étage du haut s’effrite.\n"
        "**Exemple** : EN faible en info sur la même slide (annotation)."
    ),
    (3, 2): (
        "**Écran** : **نواقص شائعة**.\n"
        "**Schéma** : icônes en liste — **Langue**, **outil**, **norme/plan**, **automatisation**, **communication**.\n"
        "**But** : lecture silencieuse ; le speaker ajoute 1 phrase de principe."
    ),
    (3, 3): (
        "**Écran** : **traiter un gap**.\n"
        "**Schéma** : boucle **doc → essai → question intelligente** ; piège LinkedIn / accumulation de vidéos barré.\n"
        "**Mini** : **critical thinking** — 3 bulles (source ? biais ? autre source ?)."
    ),
    (3, 4): (
        "**Écran** : **protocole 4 étapes** + **Feynman** + **3× علاش**.\n"
        "**Schéma** : ligne 1→2→3→4 horizontale ; en dessous bulle « expliquer simple » ; en bas « علاش ×3 » en cascade.\n"
        "**But** : trois méthodes visibles d’un coup pour alléger l’oral."
    ),
    (3, 5): (
        "**Écran** : **semaine 1 terrain**.\n"
        "**Schéma** : 3 pictos — **délais**, **notes**, **signaler un blocage**.\n"
        "**Une phrase** à l’oral."
    ),
    (3, 6): (
        "**Écran** : **pont Module 2**.\n"
        "**Schéma** : entreprise ⇄ **productivité / résultat** — « le stress du terrain n’est pas personnel ».\n"
        "**Slide très courte**."
    ),
    (3, 7): (
        "**Écran** : synthèse L3 + **L4 stress**.\n"
        "**Schéma** : **zone de confort** + **protocole** + **جسر → ضغط / انضباط**.\n"
        "**Une slide** récap."
    ),
    (3, 8): (
        "**Écran** : **7 jours — une preuve**.\n"
        "**Schéma** : UNE case « gap choisi + source + date ».\n"
        "**Minimal** pour clôture."
    ),
    # ——— Leçon 4 ———
    (4, 0): (
        "**Écran** : attentes **post-bac** vs **douche froide**.\n"
        "**Schéma** : nuage « bac = tranquille » → pluie / tempête « préparation continue ».\n"
        "**Ton** : empathique, visuel humoristique léger possible."
    ),
    (4, 1): (
        "**Écran** : **empilement** des charges + citation EN (texte sur slide).\n"
        "**Schéma** : couches empilées — **métier**, **famille**, **projets**, **responsabilités** ; dessous **« demander de l’aide ≠ faiblesse »**.\n"
        "**Citation** : affichée telle quelle pour ne pas la répéter mot à mot."
    ),
    (4, 2): (
        "**Écran** : stress **signal** / **carburant**.\n"
        "**Schéma** : curseur ou **moteur** — zone verte « utile » vs zone rouge « débordement ».\n"
        "**3 courtes bulles** : intérêt, engagement, énergie."
    ),
    (4, 3): (
        "**Écran** : **levier** + **GPS** proM7.\n"
        "**Schéma** : charge lourde + **levier** ; carte compliquée + **itinéraire simplifié**.\n"
        "**But** : métaphores visibles = moins d’explication."
    ),
    (4, 4): (
        "**Écran** : **boîte à outils** anti-stress.\n"
        "**Schéma** : rangée d’icônes — **Pomodoro**, **sommeil/eau**, **good enough**, **échéance + message**, **respiration**, **aigu vs chronique**.\n"
        "**Note** : gratitudes / croyances en petit encadré secondaire si besoin."
    ),
    (4, 5): (
        "**Écran** : **quand** solliciter de l’aide.\n"
        "**Schéma** : trois portes **enseignant · service · santé/médical**.\n"
        "**Une phrase** : ce n’est pas un tabou."
    ),
    (4, 6): (
        "**Écran** : synthèse + **L5 temps**.\n"
        "**Schéma** : **كتل + good enough + aide** → **جسر — الوقت كيتخاد**.\n"
        "**Slide unique** idéalement."
    ),
    (4, 7): (
        "**Écran** : planning **semaine**.\n"
        "**Schéma** : grille avec **3 créneaux** + **1 tâche « acceptable »**.\n"
        "**But** : la consigne est sur l’écran."
    ),
    # ——— Leçon 5 ———
    (5, 0): (
        "**Écran** : le temps **ne se trouve pas** — il se **prend**.\n"
        "**Schéma** : sablier ou calendrier barré « j’attends » vs case cochée « je bloque un créneau ».\n"
        "**Phrase-clé** sur la slide."
    ),
    (5, 1): (
        "**Écran** : **Motivation** (feuille au vent) vs **Discipline** (ancre / contrat).\n"
        "**Schéma** : deux pictos opposés ; citation discipline en **texte sur slide**.\n"
        "**But** : image mémorable."
    ),
    (5, 2): (
        "**Écran** : **LIVE** = rendez-vous non négociable.\n"
        "**Schéma** : calendrier avec **LIVE** en rouge + **préparation avant** (checklist courte).\n"
        "**Ton** : exigeant bienveillant."
    ),
    (5, 3): (
        "**Écran** : **Triangles employeur** — 3 signaux.\n"
        "**Schéma** : **Technique · Impact · Collaboration** (sommet d’un triangle ou trois colonnes).\n"
        "**Note** : le speaker pointe les sommets au lieu de relire les paragraphes."
    ),
    (5, 4): (
        "**Écran** : **time blocking** + **Pomodoro** + **rituel 15 min offres** + **année par année** (contexte MA).\n"
        "**Schéma** : bande de créneaux colorés ; encart **15’** lecture offre ; carte **Maroc** ou mention « parcours locaux différents ».\n"
        "**Slide riche** : accepter de passer 20–30 s en silence sur le visuel."
    ),
    (5, 5): (
        "**Écran** : synthèse + **pont L6 (M0) — études & marché**.\n"
        "**Schéma** : **temps = décision** + **discipline** + **rituel** → **جسر — قراية وسوق الشغل** ; encart **M3 L28** « projection » (hors M0).\n"
        "**Une slide**."
    ),
    (5, 6): (
        "**Écran** : **3 créneaux** + **2 offres**.\n"
        "**Schéma** : checklist visuelle simple.\n"
        "**Fin de leçon**."
    ),
    # ——— Leçon 6 (ex-L7) ———
    (6, 0): (
        "**Écran** : **école** (notes, tests) vs **marché** (preuve, équipe).\n"
        "**Schéma** : deux colonnes comparées ; citation **leçon vs test** en texte sur slide ; pictos **diplôme actif**, **réseau**, **équilibre humain-numérique**.\n"
        "**But** : forte charge sémantique portée par l’image."
    ),
    (6, 1): (
        "**Écran** : **généraliste** vs **spécialiste**.\n"
        "**Schéma** : deux silhouettes ou outils — **couteau suisse** vs **laser** ; phrase **« السوق محتاج بجوج »**.\n"
        "**Réduire** la partie définition à l’oral."
    ),
    (6, 2): (
        "**Écran** : **Théorie (ساس)** ⟷ **Pratique (يد)**.\n"
        "**Schéma** : fondation + maison / ou racines + branches selon style graphique.\n"
        "**Message** : les deux se renforcent."
    ),
    (6, 3): (
        "**Écran** : **Maroc — sources**.\n"
        "**Schéma** : **HCP / hcp.ma** au centre ; autour **contexte pays** (secteurs, politiques) sans chiffres inventés ; **fracture numérique** → **alternatives** (biblio, asso…).\n"
        "**Sobriété** : logos institutionnels si autorisé."
    ),
    (6, 4): (
        "**Écran** : **scan employeur** en **30 s**.\n"
        "**Schéma** : loupe sur **CV** — ordre de lecture **métier → preuve → détail** ; **M1** en encart « approfondir ».\n"
        "**But** : le schéma remplace la relecture des critères."
    ),
    (6, 5): (
        "**Écran** : **synthèse** + **M1**.\n"
        "**Schéma** : **نقطة + تأهيل + portfolio** ; **Généraliste / Spécialiste** rappel une icône ; **HCP** ; ** valeur proposée**.\n"
        "**Pont** : entrée **Module 1**."
    ),
    (6, 6): (
        "**Écran** : les **2 phrases** (الشهادة / الدليل).\n"
        "**Schéma** : deux bulles larges pour lisibilité **face caméra** ; fond sobre.\n"
        "**Fin de module 0**."
    ),
}
