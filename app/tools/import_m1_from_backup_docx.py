# -*- coding: utf-8 -*-
"""
Lit les .docx de sauvegarde Module 1 (développement contenu) et régénère
tools/module01_rich_content.py avec le texte intégral des paragraphes.

- Ne modifie pas le dossier de sauvegarde.
- Post-traitements : ProMind7 -> proM7 ; الساروت -> التأهيل الرسمي (L14) ;
  « وراق » au sens diplôme dans contexte employeur -> صفحة الشهادة (éviter ambiguïté).

Ensuite : python app/tools/format_modules_01_02_scripts.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from docx import Document
except ImportError:
    print("pip install python-docx", file=sys.stderr)
    sys.exit(1)

PROMIND7 = Path(r"D:\Promind7")
DEV = next(PROMIND7.glob("d*veloppement contenu"))
M1_BACKUP = next((DEV / "scripts").glob("01-Module 1*"))
ROOT = Path(__file__).resolve().parent.parent
OUT_PY = ROOT / "tools" / "module01_rich_content.py"

MODULE1_LIGNE_CADRE = "Module 1 : L'économie et le marché du travail (الاقتصاد وسوق الشغل)"

LESSON_TITLES: dict[int, tuple[str, str, str]] = {
    9: ("Leçon 9 — Le marché du travail", "Leçon 9 : Le marché du travail (سوق الشغل)", "فهم سوق الشغل والمنطق الاقتصادي للتوظيف؛ التحول من عقلية المدرسة إلى مزود قيمة؛ أطراف اللعبة والقيمة العادلة؛ السوق الحقيقي والرقمي."),
    10: ("Leçon 10 — L'impact de l'économie sur le marché du travail", "Leçon 10 : L'impact de l'économie sur le marché du travail (تأثير الاقتصاد)", "المحرك الاقتصادي؛ القيمة المضافة؛ السياسات والاستثمار؛ السوق الرئيسي والمشتق؛ التحول والمرونة."),
    11: ("Leçon 11 — Le marché du travail international", "Leçon 11 : Le marché du travail international (سوق الشغل الدولي)", "التقييس والمعايير؛ اللغة المهنية؛ منطق الاستثمار والرقمي؛ التحقق من الأرقام عبر الوثائق الرسمية المحدثة."),
    12: ("Leçon 12 — Le marché du travail au Maroc", "Leçon 12 : Le marché du travail au Maroc (سوق الشغل في المغرب)", "خصوصيات السوق؛ أرقام رسمية (تحديث HCP)؛ جغرافيا؛ سوق خفي؛ أنماط المقاولات."),
    13: ("Leçon 13 — Les tendances du marché", "Leçon 13 : Les tendances du marché (توجهات السوق)", "الرادار والسلاسل؛ بروفيلات؛ قاطرات قطاعية؛ أدوات متابعة عملية."),
    14: ("Leçon 14 — Le diplôme et le marché du travail", "Leçon 14 : Le diplôme et le marché du travail (الشهادة والسوق)", "الشبكة والفرز؛ مسارات حسب المستوى؛ Troubleshooting؛ الدكتوراه والجغرافيا."),
    15: ("Leçon 15 — Offre et demande d'emploi", "Leçon 15 : Offre et demande d'emploi (العرض والطلب)", "قانون العرض والطلب؛ الندرة؛ IA؛ الريزو؛ تحسين العرض الشخصي."),
    16: ("Leçon 16 — Les règles (souvent invisibles) du marché de l'emploi", "Leçon 16 : Règles invisibles du marché (قواعد مخفية)", "سوق خفي؛ تكلفة التوظيف؛ إعلانات؛ الإدراك."),
    17: ("Leçon 17 — Partir à l'étranger ou rester au Maroc", "Leçon 17 : Partir ou rester (الخارج أم البقاء)", "قرار استراتيجي؛ مسار وتجربة؛ مخاطر؛ خبير محلي."),
    18: ("Leçon 18 — Lien marché du travail et entreprises", "Leçon 18 : Marché et entreprise (السوق والمقاولة)", "خلاصة المنظومة؛ مدينة وعنوان؛ تصفية؛ تمهيد الموديل 2."),
}


def extract_paragraphs(path: Path) -> list[str]:
    doc = Document(str(path))
    return [p.text.strip() for p in doc.paragraphs if (p.text or "").strip()]


def postprocess(text: str, lesson_id: int) -> str:
    t = text
    t = re.sub(r"\bProMind7\b", "proM7", t, flags=re.I)
    t = re.sub(r"\bPM7\b", "proM7", t)
    # L14 lexique
    if lesson_id == 14:
        t = t.replace("الساروت ديالك", "التأهيل الرسمي ديالك")
        t = t.replace("الساروت", "التأهيل الرسمي")
    t = t.replace(
        "المهارات التقنية هي الساروت،",
        "المهارات التقنية هي الأساس،",
    )
    # L9 backup: "ما يكونوش فاهمين التقنيات" - keep
    # Diplôme / وراق in employer context (L9 line about مشغل)
    t = t.replace(
        "ما كيهمهومش شحال واعر نتا في الوراق",
        "ما كيهمهومش الشهادة وحدها بلا دليل عملي",
    )
    return t


_START_SEQ = re.compile(
    r"^[\s]*(?:🎥\s*)?[\s]*"
    r"(\(الدخلة|\(الفكرة|\(خاتمة|\(الخاتمة|Séquence\s+\d+)",
    re.I,
)


def paragraphs_to_sequences(paras: list[str], lesson_id: int) -> list[tuple[str, list[str]]]:
    """Regroupe les paragraphes : chaque marqueur (الدخلة / الفكرة / خاتمة / 🎥) démarre une séquence."""
    sequences: list[tuple[str, list[str]]] = []
    current_title = ""
    current_body: list[str] = []

    for raw in paras:
        line = postprocess(raw, lesson_id).strip()
        if not line:
            continue
        if _START_SEQ.match(line):
            if current_body:
                tid = current_title or f"Séquence {len(sequences) + 1}"
                sequences.append((tid, current_body.copy()))
            n = len(sequences) + 1
            # Titre court pour Word : le marqueur oral (الدخلة، الفكرة…) reste uniquement dans le corps.
            current_title = f"Séquence {n}"
            current_body = [line]
        else:
            if not current_title:
                current_title = f"Séquence {len(sequences) + 1} — Partie"
            current_body.append(line)

    if current_body:
        tid = current_title or f"Séquence {len(sequences) + 1}"
        sequences.append((tid, current_body))

    if not sequences and paras:
        sequences = [
            ("Séquence 1 — Script", [postprocess(p, lesson_id).strip() for p in paras if p.strip()])
        ]
    return sequences


def lesson_paths() -> dict[int, Path]:
    out: dict[int, Path] = {}
    for p in sorted(M1_BACKUP.rglob("*.docx")):
        if "Brain storming" in str(p) or "test Module" in str(p):
            continue
        folder = p.parent.name
        try:
            lid = int(folder.split("-", 1)[0])
        except ValueError:
            continue
        if 9 <= lid <= 18:
            out[lid] = p
    return out


def py_str_literal(s: str) -> str:
    return repr(s)


def build_file(lessons_data: dict[int, dict]) -> str:
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""',
        "Scripts oraux darija — Module 1 : économie & marché du travail.",
        "Contenu réimporté depuis les .docx de sauvegarde (développement contenu/scripts/01-Module 1…).",
        "Post-traitements : proM7 ; lexique L14 (التأهيل الرسمي) ; formulation employeur sans « وراق » ambigu.",
        "Régénération Word : python app/tools/format_modules_01_02_scripts.py",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        f"MODULE1_LIGNE_CADRE = {py_str_literal(MODULE1_LIGNE_CADRE)}",
        "",
        "LESSONS: dict[int, dict] = {",
    ]
    for lid in sorted(lessons_data):
        d = lessons_data[lid]
        lines.append(f"    {lid}: {{")
        lines.append(f'        "title": {py_str_literal(d["title"])},')
        lines.append('        "cadre_lignes": (')
        lines.append(f"            MODULE1_LIGNE_CADRE,")
        lines.append(f"            {py_str_literal(d['cadre_l2'])},")
        lines.append("        ),")
        lines.append(f'        "objectif_ar": {py_str_literal(d["objectif_ar"])},')
        lines.append('        "sequences": [')
        for title, bodies in d["sequences"]:
            lines.append("            (")
            lines.append(f"                {py_str_literal(title)},")
            lines.append("                [")
            for b in bodies:
                lines.append(f"                    {py_str_literal(b)},")
            lines.append("                ],")
            lines.append("            ),")
        lines.append("        ],")
        lines.append("    },")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    paths = lesson_paths()
    missing = [i for i in range(9, 19) if i not in paths]
    if missing:
        print("Missing lessons:", missing, file=sys.stderr)
        sys.exit(1)

    lessons_data: dict[int, dict] = {}
    for lid in range(9, 19):
        paras = extract_paragraphs(paths[lid])
        title, cadre_l2, objectif_ar = LESSON_TITLES[lid]
        seqs = paragraphs_to_sequences(paras, lid)
        lessons_data[lid] = {
            "title": title,
            "cadre_l2": cadre_l2,
            "objectif_ar": objectif_ar,
            "sequences": seqs,
        }

    OUT_PY.write_text(build_file(lessons_data), encoding="utf-8")
    print("Wrote", OUT_PY, "lessons", list(lessons_data.keys()))


if __name__ == "__main__":
    main()
