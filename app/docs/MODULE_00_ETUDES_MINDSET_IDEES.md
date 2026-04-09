# Module 00 — Études & mindset : idées de complément + expertise métier

> **Priorité** : enrichir le **contenu technique et terrain** après les **000-Initiation** (intro / méthode / promesse, peu de technique).  
> **Ce document** : banque d’idées et **où** injecter l’expertise proM7.  
> **Leçons réelles** : inventaire ci-dessous (dossier sur disque). Croiser avec **`Input/Architecture cours/Architecture cours.xlsx`** si le catalogue produit évolue.

---

## 1. Rappel — règles établies (produit & ton)

| Règle | Détail |
|--------|--------|
| **Public** | Étudiant·e **marocain·e**, post-bac (dont filières techniques), du début de cursus au diplôme. |
| **Promesse** | **Méthode, lucidité, outils** — **pas** d’emploi/stage garanti, pas de « baguette magique ». |
| **Marché** | **Maroc**, entreprises et stages **réalistes** ; éviter le discours générique type Silicon Valley. |
| **Langue** | **Darija** pour le cœur des concepts **dans le produit fini** ; **FR / EN** pour le **vocabulaire professionnel** (stages, entretiens, docs). **Veille** : les vidéos / articles sources peuvent être dans **n’importe quelle langue** pour les **méthodes** transposables ; pour le **marché et le contexte Maroc**, rester **vigilant** et **adapter** (sources locales, pas de copier-coller d’un autre pays). |
| **Marque** | **proM7** uniquement dans les textes latins (pas PM7 / P7 / ProMind7 dans le neuf). |
| **Rôle proM7** | **Passerelle** formation ↔ terrain ; **accompagnement méthodologique** ; l’étudiant garde la responsabilité de son travail. |

*Référence complète :* `.cursor/skills/promind7-parcours-objectifs/SKILL.md`

### Objectif pédagogique du module 00 (brief)

> Ancrer la **relation études ↔ marché** : choix, lacunes techniques, stress, temps, projection, posture d’étudiant·e **déjà tourné·e vers l’employabilité**.

---

## 2. Rappel — format Word (scripts vidéo / scripts de leçon type parcours)

Aligné sur **`content/FORMAT_SCRIPTS_VIDEOS_PROFM7.md`** (à appliquer aux `.docx` de ce module si format « script vidéo » ou même logique éditoriale) :

1. **Titre du script** — un paragraphe, **tout en gras**, **Calibri 11 pt**.
2. **Section objectif** — titre **`الهدف`** en **gras** + **couleur verte** ; **un seul paragraphe en arabe uniquement** (intention pour la prod).
3. **Séquences** — titre de chaque séquence en **gras** + **couleur distinctive** (ex. bleu) ; corps en **texte normal** noir, **Calibri 11 pt** partout (pas de « Titre 1 » qui change la taille).
4. **RTL** — direction droite → gauche sur les paragraphes (darija / arabe) : `w:bidi` + `w:rtl` ; script Python : `tools/apply_rtl_all_parcours_docx.py` sur les fichiers hors gabarit `format_parcours_video_scripts.py`.

*Les vidéos gratuites* : dossier `000-Initiation` ; *le module 00* : voir chemin ci-dessous — **même discipline de format** si le livrable est un script Word.

---

## 2 bis. Inventaire — dossier Module 0 (vos fichiers)

**Chemin (Windows)**  
`D:\Promind7\IA\V2\Input\Script\Parcours stage & emploi\00-Module 0 - les études et le mindest`  

> Le nom du dossier contient **« mindest »** (orthographe actuelle sur le disque). Renommage éventuel en **mindset** : à faire ensemble si vous voulez aligner partout (raccourcis, Excel, Tutor).

**Chemin relatif (depuis la racine du projet V2)**  
`Input/Script/Parcours stage & emploi/00-Module 0 - les études et le mindest/`

| # dossier | Dossier leçon | Fichier `.docx` |
|-----------|----------------|-----------------|
| 01 | `01-Introduction au Parcours stage et emploi` | `Leçon 1 - Introduction au Parcours stage et emploi-darija.docx` |
| 02 | `02-Les études et le choix de la specialité` | `Leçon 2 - Les études et le choix de la specialité-darija.docx` |
| 03 | `03-les lacunes et la difficulté technique` | `Leçon 3 - les lacunes et la difficulté technique-darija.docx` |
| 04 | `04-la gestion du stress en tant qu'étudiant` | `Leçon 4 - la gestion du stress en tant qu'étudiant-darija.docx` |
| 05 | `05-La gestion du temps et la discipline` | `Leçon 5 - La gestion du temps et la discipline-darija.docx` |
| 06 | `06-la projection dans l'avenir` | `Leçon 6 - la projection dans l'avenir-fr - darija.docx` |
| 07 | `07-le lien entre les études et le marché du travail` | `Leçon 7 - le lien entre les études et le marché du travail-darija.docx` |

**Numérotation dans les titres internes** : certains documents utilisent « الدرس 1 » alors que le fichier est la **Leçon 2**, etc. — à harmoniser lors d’une passe éditoriale (sans changer la logique pédagogique).

**Alignement format cible** (`FORMAT_SCRIPTS_VIDEOS_PROFM7.md`) : les `.docx` actuels mélangent titres FR/ar et sections type « 1. … » ; pour la **prod** et l’aperçu Streamlit homogènes, viser **titre script en gras** → **الهدف** (vert, arabe seul) → **séquences** (titres gras bleus) + **RTL** + **Calibri 11** partout.

---

## 3. Rôle du module 00 par rapport aux vidéos gratuites

| 000 — Vidéos gratuites | Module 00 — Études & mindset |
|------------------------|------------------------------|
| Narratif, émotions, **questions** posées, **comment** travaille proM7, **ce que vous gagnez** (sans miracle). | **Approfondit** : **contenu** + **réflexes** pour lier **cours, projets, temps** à **ce que le marché lit** (compétences, preuves, posture). |
| Peu ou pas de technique métier. | C’est ici qu’on introduit **progressivement** la **lucidité technique** (lacunes, priorités, « bagage ») et le **mindset employabilité** **sans** remplacer les modules 01–07. |

**Fil rouge** : chaque leçon du 00 doit répondre implicitement à *« comment ce que je fais **cette semaine** aux études me rapproche (ou pas) d’un stagiaire / junior crédible ? »*

---

## 4. Idées de contenu — axes à développer (compléments)

**Cartographie rapide** (axe section 4 + expertise section 5) :

| Leçon | Thème du fichier | Axes de complément prioritaires | Injection expertise (ex.) |
|-------|------------------|----------------------------------|---------------------------|
| **1** | Intro parcours & agenda | Teasing **modules 01–07** sans tout dire ; rappel promesse **sans miracle** ; lien explicite avec **000-Initiation**. | Ce que **proM7** ne fait pas / ce qu’il fait (méthode, terrain Maroc). |
| **2** | Études & choix de spé | Grille **2 axes** (affinité × réalisme marché Maroc) ; tronc vs spé ; **CV-compétence** à partir d’un module. | Témoignage court **reconversion** / même diplôme, parcours différents. |
| **3** | Lacunes & difficulté technique | Liste **3 à 5 lacunes** typiques post-bac ; **protocole** : doc officielle, asso, prof, pair ; question pro à l’encadrant. | « Ce que l’**atelier** attend souvent dès J1 » vs programme scolaire. |
| **4** | Stress étudiant | Technique **concrète** (respiration, découpage charge, « good enough » sur le non-critique). | Stress **utile** (responsabilité) vs rumination ; parallèle **délai projet** en entreprise (léger). |
| **5** | Temps & discipline | **Time blocking** 1 semaine type ; **motivation vs discipline** (déjà amorcé — approfondir avec exemples cours/TP/PFE). | Rituel **15 min / jour** veille emploi (offres = vocabulaire) sans surcharge. |
| **6** | Projection / avenir | Éviter le seul discours « manifestation » : ancrer en **objectifs 6 mois / 2 ans / 5 ans** + **indicateurs** révisables. | « Vision » d’un **chef de projet** : jalons, pas seulement titre de poste. |
| **7** | Études ↔ marché | **Diplôme = passe** + **compétence = preuve** (déjà présent — renforcer avec 1 exemple **chiffré** HCP ou offre réelle anonymisée). | Ce que lit un **recruteur** en 30 secondes sur un CV (aligné module 05 plus tard). |

### A. Études comme **système** (pas seulement notes)

- Différence entre **réussir un examen** et **être prêt pour un problème ouvert** en entreprise.
- **Modules / projets** : comment les **nommer sur un CV** en **compétence** (verbes d’action + résultat), pas en liste de cours.
- **Tronc vs spé** : l’**exploration légitime** vs la **dilution** ; critères simples pour choisir sans se paralyser.

### B. Mindset **employabilité** (sans culpabiliser)

- **Curiosité marché** : 30 min / semaine pour lire des offres **sans postuler** (dictionnaire vivant FR/EN).
- **Identité** : « je suis en formation » **et** « je construis déjà une preuve » (portfolio minuscule, compte-rendu, mini-projet).
- **Comparaison sociale** : normaliser le **doute** ; le cadre proM7 = **méthode**, pas **course au buzz**.

### C. **Temps, stress, charge** (opérationnel)

- Priorisation **RICE light** ou matrice **urgent / important** adaptée étudiant.
- **Pics** (partiels, PFE) : comment **ne pas zéro** la veille pro pendant 6 mois.
- Sommeil, écrans : message **court** et réaliste (pas moralisateur).

### D. **Lacunes techniques** (amorce du « technique » sans faire le module 02)

- « Ce que l’entreprise suppose souvent que tu sais déjà » vs « ce que l’école a le temps de donner ».
- **Autonomie d’apprentissage** : où trouver **doc officielle**, **norme**, **vidéo terrain** ; comment poser une **question pro** à un encadrant (contexte, ce que j’ai essayé).

### E. **Lien avec la suite du parcours** (teasing maîtrisé)

- Une phrase du type : *le module 01 mettra des **chiffres** et un **cadre** sur ce marché ; le 04/05 sur **stage** et **emploi*** — sans tout dévoiler.

---

## 5. Où injecter **l’expertise métier** proM7 (ce qui compte le plus)

L’expertise = **regard terrain** (maintenance, énergie, industrie, reconversion, hiérarchie, projets sous pression) — déjà esquissée dans les scripts gratuits (témoignages, « chantier vs bureau », rigueur, adaptation).

| Type d’expertise | Exemple d’idée concrète pour le module 00 |
|------------------|-------------------------------------------|
| **Ce que voit un encadrant** | « Les 3 premières choses que je regarde chez un stagiaire Bac+2/3 » (ponctualité des livrables, clarté quand il bloque, prise de notes). |
| **Écart cours / atelier / terrain** | Histoire courte : **même diplôme**, deux profils — celui qui **reformule** un TD en **problème client** vs celui qui attend le TP noté. |
| **Vocabulaire** | 5 termes **FR** qu’on entend en réunion et qu’il faut **reconnaître** avant le premier stage (sans cours de langue complet — renvoi module 07). |
| **Preuve** | « Mini-preuve » : screenshot d’un tableau simple, git, ou compte-rendu d’une demi-journée d’observation — **éthique** (pas de données d’entreprise réelles sensibles). |
| **Choix de spé** | Critère **marché Maroc** + critère **affinité personnalité** (sans dire « X est mieux que Y ») — aligné Leçon 3 gratuite mais **outil** ici (grille 2 axes). |
| **Honesty** | Ce qu’**un diplôme ne remplace pas** le premier mois (communication, fiabilité, apprentissage actif). |

**Règle d’or** : chaque séquence « expert » doit finir par un **geste étudiant** faisable cette semaine (micro-action), pas seulement une anecdote.

---

## 6. Prochaines étapes pratiques

1. **Régénération Word (v1)** : depuis la racine V2, `python tools/format_module00_scripts.py` — réécrit les **7** `.docx` du Module 0 (titre → **الهدف** → séquences, RTL). Option : `--out-dir CHEMIN` (recrée les sous-dossiers `01-…` … `07-…`). Fermer les Word avant lancement.
2. Travailler **leçon par leçon** : le texte darija « riche » (restauré depuis `reports/parcours_lessons_extract.md` + complétions + ajouts) est dans **`tools/module00_rich_content.py`** ; la mise en page Word dans **`tools/format_module00_scripts.py`**.
3. Si besoin d’une **passe RTL** sur d’autres fichiers du pack : `python tools/apply_rtl_all_parcours_docx.py`.
4. Vérifier cohérence avec **`Architecture cours.xlsx`** (titres affichés plateforme vs noms de fichiers).

---

## 7. Piste de veille (rappel)

- **`docs/RESSOURCES_VIDEOS_DOCS_PARCOURS_VIDEOS.md`** — pack **000** + HCP, OnisepTV, SCUIO, MOOC.  
- **`docs/MODULE_00_SOURCES_WEB_YOUTUBE.md`** — **liens web + YouTube / TED / Lumni** mappés **leçon par leçon** pour le **Module 00** (7 leçons).

---

*Inventaire disque : mars 2026. À mettre à jour si vous ajoutez des leçons ou renommez le dossier Module 0.*

---

## 8. Propositions d’amélioration — méthodologie **déjà définie** (les 7 leçons)

**Méthode appliquée à chaque leçon** (identique aux règles §1–2 + fil rouge §3) :

| Étape | Règle |
|--------|--------|
| **Structure Word** | Titre gras (Calibri 11) → **الهدف** (vert, **un** paragraphe **arabe seul**) → **Séquences** (titres gras **bleu**) → corps darija + termes **FR/EN** entre parenthèses si besoin. |
| **Ton** | Lucidité, Maroc, **pas** de promesse magique ; **proM7** = accompagnement méthodologique. |
| **Expertise** | Au moins **une** séquence « terrain » (encadrant, atelier, recruteur, délai réel). |
| **Clôture** | **Micro-action** étudiant **cette semaine** (répétable). |
| **Cohérence** | Renvoi explicite vers **module 01** (marché), **04–05** (stage/emploi), **07** (langues) quand c’est pertinent — **une phrase**, pas un cours. |

Les **الهدف** ci-dessous sont des **propositions** à coller/adapter en arabe pour la prod ; le corps reste en **darija** dans les séquences.

---

### Leçon 1 — Introduction au parcours Stage & emploi

| Élément | Proposition |
|---------|-------------|
| **الهدف (proposition)** | تقديم مسار « التدريب والشغل » في سياقه الكامل؛ ربطه بوضوح بفيديوهات الترحيب المجانية؛ شرح ما تقدمه proM7 من منهجية وتمارين عملية وما لا تقدمه (لا ضمان توظيف ولا وعود سحرية)؛ وعرض خريطة الوحدات 01–07 في جملة واحدة لكل وحدة ليعرف الطالب أين يتجه. |
| **Séquences suggérées** | **Séquence d’ouverture** — الترحيب والسياق المغربي · **Séquence 2** — ماذا قالت فيديوهات 000 (أسئلة مشروعة) · **Séquence 3** — خريطة المسار: ماذا سنغطي في كل وحدة (01→07) · **Séquence 4** — كيف يعمل proM7: الدارجة + المفاتيح المهنية FR/EN · **Séquence 5** — التزامك الشخصي + **micro-action** |
| **Expertise** | جملة صريحة: في الميدان ما كيفرّقش غير الشهادة؛ الطريقة باش كتخدم وكتسول هي اللي كيبان بيها الفرق. |
| **Micro-action** | كتابة **3 أسئلة شخصية** يأمل أن يجيب عنها المسار + تثبيت **موعد أسبوعي** 30 دقيقة للمتابعة (يوم ثابت). |
| **Amélioration** | إزالة التكرار الطويل مع نصوص 000؛ الاكتفاء ب **جسر**: شفتو الفيديوهات؟ هنا ندخلو للتفصيل. |

---

### Leçon 2 — Les études et le choix de la spécialité

| Élément | Proposition |
|---------|-------------|
| **الهدف (proposition)** | تطبيع الشك في اختيار التخصص بعد الباكالوريا؛ تقديم أداة بسيطة (جدول اثنين في اثنين) للموازنة بين الاهتمام الشخصي وواقع سوق الشغل في المغرب؛ وربط أحد المقررات أو المشاريع بصيغة **كفاءة** يمكن ذكرها لاحقاً في السيرة الذاتية. |
| **Séquences suggérées** | **Séquence 1** — علاش كانتخاف من «الاختيار الغلط»؟ · **Séquence 2** — **Grille 2 axes** (Affinité / Réalisme marché) — شرح بالدارجة + مثال · **Séquence 3** — Tronc commun: استكشاف مشروع vs تشتت · **Séquence 4** — من مادة واحدة إلى سطر CV: فعل + نتيجة (مثال FR: *Réalisé…*, *Contribué à…*) · **Séquence 5** — **Renvoi** الوحدة 01 للأرقام والإطار |
| **Expertise** | مثال قصير: **نفس الدبلوم**، مساران مختلفان (تقني ميدان vs مكتب) — بدون احتقار أحد المسارين. |
| **Micro-action** | ملء **Grille** لمادتين أو تخصصين محتملين + صياغة **سطر واحد** كفاءة من مشروع أو TP حالي. |
| **Amélioration** | توحيد الترقيم الداخلي (الدرس = رقم الملف Leçon 2)؛ استبدال النصائح العامة ب **مثال واحد مُسمّى** (مادة + مهارة). |

---

### Leçon 3 — Les lacunes et la difficulté technique

| Élément | Proposition |
|---------|-------------|
| **الهدف (proposition)** | تعلم التعامل مع النواقص التقنية دون إحباط؛ تطبيق **بروتوكول** بحث (وثائق رسمية، فيديوهات موثوقة، أستاذ، زميل)؛ وصياغة **سؤال احترافي** عند طلب المساعدة من مشرف أو محترف؛ مع فكرة واقعية عما قد يتوقعه الميدان في الأيام الأولى. |
| **Séquences suggérées** | **Séquence 1** — منطقة الراحة: متى تخدمك ومتى تخسرك؟ · **Séquence 2** — **5 نواقص شائعة** بعد الباك (مثال: أوتوماتisation، قراءة مخطط، إنجليزية تقنية، أداة معينة…) — قابلة للتخصيص حسب الشعبة · **Séquence 3** — **Protocole 4 خطوات** قبل السؤال · **Séquence 4** — نموذج سؤال: جرّبت X، توقفت عند Y، بحثت في Z · **Séquence 5** — **Terrain** — ما يتوقعه المشرف في الأسبوع الأول (وضوح، ملاحظات، انضباط) |
| **Expertise** | اللي كيبان فالورشة ماشي هو نفس اللي فالكتاب؛ السلوك المتوقع: ملاحظة، سؤال، ما تخمّنش بلا أساس. |
| **Micro-action** | اختيار **نقص واحد** + **مصدر واحد** (رابط/كتاب/playlist) + **موعد نهائي** خلال 7 أيام. |
| **Amélioration** | ربط صريح بالوحدة **02** (الشركة) لاحقاً: غنفهمو علاش كيهتمو بالمردودية — جملة واحدة. |

---

### Leçon 4 — Gestion du stress (étudiant)

| Élément | Proposition |
|---------|-------------|
| **الهدف (proposition)** | إعادة إطار التوتر كعلامة على الاهتمام والمسؤولية وليس كضعف؛ تقديم أدوات عملية قصيرة (تجزئة المهام، حد أدنى مقبول للمهام الثانوية، روتين قبل الامتحان)؛ وفهم الفرق بين ضغط **محدد بموعد** كما في المشاريع المهنية وبين القلق المفتوح بدون خطة. |
| **Séquences suggérées** | **Séquence 1** — صدمة ما بعد الباك (الاعتراف بالمشاعر) · **Séquence 2** — Stress **مفيد** vs دوامة التفكير · **Séquence 3** — **Technique** (مثال: **Pomodoro** أو timeboxing 25/5 + قائمة *good enough*) · **Séquence 4** — مثال خفيف: **دليل مشروع** في الشركة = موعد + جودة متفق عليها · **Séquence 5** — متى تطلب مساعدة (طبيب، أستاذ، مقرب) — بدون وصم |
| **Expertise** | فالخدمة التوتر كاين؛ الفارق هو **الخطة** و**التواصل** مع الفريق. |
| **Micro-action** | جدولة **أسبوع واحد** مع **3 فترات تركيز** ثابتة + تحديد **مهمة واحدة** على مستوى «مقبول» وليس مثالية. |
| **Amélioration** | تجنب الإطالة العاطفية فقط؛ كل قصة = **أداة** تلحقها. |

---

### Leçon 5 — Gestion du temps et discipline

| Élément | Proposition |
|---------|-------------|
| **الهدف (proposition)** | الفصل بين الاعتماد على الحافز اليومي وبناء **انضباط** قابل للتكرار؛ تطبيق **تخطيط أسبوعي** واقعي (الدراسة، المشاريع، الراحة)؛ وإدماج **rituel قصير** (15 دقيقة) لقراءة عروض الشغل كقاموس حي للمفردات المهنية دون إرهاق. |
| **Séquences suggérées** | **Séquence 1** — ما تستناش الوقت يفرّغ لك · **Séquence 2** — **Motivation** (متقلبة) vs **Discipline** (نظام) · **Séquence 3** — **Time blocking** — نموذج أسبوع طالب تقني · **Séquence 4** — **15 دقيقة عروض** (FR/EN) — بدون تقديم طلب · **Séquence 5** — فترات الامتحانات: **حد أدنى** غير قابل للتفاوض لـ«الخط المهني» (مثال: لغة، سطر واحد في السيرة) |
| **Expertise** | اللي كيوصل للأهداف كيخدم حتى ملي ما عندوش المزاج — ربط ب **rendu** في السطاج. |
| **Micro-action** | حجز **3 كتل زمنية** متكررة في الأسبوع + تفعيل **مؤقت 15 دقيقة** يوم واحد لقراءة عرضين على الأقل. |
| **Amélioration** | توحيد المصطلحات اللاتينية: **Discipline**, **time blocking** — مرة واحدة مع تعريف بالدارجة. |

---

### Leçon 6 — Projection dans l’avenir

| Élément | Proposition |
|---------|-------------|
| **الهدف (proposition)** | بناء **رؤية قابلة للمراجعة** على أجزاء زمنية (6 أشهر، سنتان، 5 سنوات) مع **مؤشرات بسيطة** (مهارة، شهادة، تجربة)؛ تجنب الاكتفاء بالتخيل دون إجراء؛ وربط الرؤية بمسارات لاحقة في الدورة (سطاج، عمل). |
| **Séquences suggérées** | **Séquence 1** — شنو الفرق بين **حلم** و **مشروع بجداول زمنية**؟ · **Séquence 2** — **Jalons 6 mois / 2 ans / 5 ans** (أمثلة واقعية) · **Séquence 3** — **Indicateurs** قابلة للقياس (مثال: مستوى لغة، مشروع، تدريب صيفي) · **Séquence 4** — تحذير لطيف: التصور وحده لا يغني عن **العمل الأسبوعي** · **Séquence 5** — **Renvoi** الوحدات 04 و 05 |
| **Expertise** | صيغة **chef de projet**: أهداف = **jalons + موارد + مخاطر** — جملة أو مثال مصغر. |
| **Micro-action** | كتابة **3 جداول زمنية** + **مؤشر واحد** لكل مرحلة + **خطوة واحدة** للأسبوع القادم. |
| **Amélioration** | إعادة إطار مصطلحات مثل **Manifestation**: إما حذفها أو استبدالها ب **تخطيط ومراجعات** لتبقى متسقة مع منهجية proM7 (واقعية، قابلة للقياس). |

---

### Leçon 7 — Lien entre les études et le marché du travail

| Élément | Proposition |
|---------|-------------|
| **الهدف (proposition)** | توضيح أن الشهادة غالباً **بوابة اعتماد** وفتح مجال، بينما سوق الشغل يقرأ **الكفاءة والدليل**؛ تقديم مثال موجز لواقع سوق العمل في المغرب (اتجاه أو رقم من مصدر رسمي عند الحاجة)؛ وربط ذلك بما سيأتي في الوحدة 01 والوحدة 05. |
| **Séquences suggérées** | **Séquence 1** — نهاية عصر «النقطة وحدها» كرصيد كافٍ · **Séquence 2** — الدبلوم كـ **pass** (اعتراف + أهلية) · **Séquence 3** — الكفاءة = **preuve** (مشروع، تدريب، نتيجة قابلة للتوضيح) · **Séquence 4** — **Encadré chiffre** (HCP أو ملخص قصير جداً) — جملتان كحد أقصى في النص المنطوق · **Séquence 5** — **30 ثانية**: ماذا يبحث عنه المشغل في السيرة؟ + **Renvoi** Module 01 |
| **Expertise** | فـ30 ثانية، كنشوف: التخصص، آخر تجربة، والفعل — من منظور encadrant/recruteur (عام، أخلاقي). |
| **Micro-action** | صياغة **جملتين**: (1) جملة «الشهادة تفتح لي…» (2) جملة «الدليل عندي هو…» — بإمكان قراءتهما بصوت عالٍ. |
| **Amélioration** | الإبقاء على القوة الحالية للدرس؛ إضافة **مصدر واحد** في الشريط أو الوصف (HCP) للشفافية. |

---

### Synthèse — تسلسل المودول بعد التحسين

1. **1** — خريطة + عقد نفسي مع المنهجية.  
2. **2** — أداة اختيار + بداية صياغة كفاءة.  
3. **3** — بروتوكول تقني + سؤال محترف.  
4. **4** — إدارة التوتر بأدوات.  
5. **5** — نظام وقت + عادة سوق الشغل الصغيرة.  
6. **6** — رؤية بجداول ومؤشرات.  
7. **7** — جملة الخلاصة: شهادة + دليل + انتقال إلى **01**.

---

*Section 8 : propositions opérationnelles — à intégrer progressivement dans les `.docx` puis passe RTL/format (§6).*
