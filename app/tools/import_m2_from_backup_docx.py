# -*- coding: utf-8 -*-
"""
Lit les .docx de sauvegarde Module 2 (développement contenu) et régénère
tools/module02_rich_content.py avec le texte intégral des paragraphes.

- Ne modifie pas le dossier de sauvegarde.
- Leçon 24 : hors scope du pack Python (comme format_modules_01_02_scripts.py) — non importée.
- Post-traitements : ProMind7 -> proM7 ; « الساروت » (CV) -> « التأهيل الرسمي » quand c’est le sens diplôme/CV.

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
M2_BACKUP = next((DEV / "scripts").glob("02-Module 2*"))
ROOT = Path(__file__).resolve().parent.parent
OUT_PY = ROOT / "tools" / "module02_rich_content.py"

MODULE2_LIGNE_CADRE = "Module 2 : L'entreprise (المقاولة)"

# Titres + cadre ligne 2 + objectif_ar (métadonnées pack V2 — le corps vient du backup)
LESSON_META: dict[int, tuple[str, str, str]] = {
    20: (
        "Leçon 20 — Pourquoi les entreprises existent",
        "Leçon 20 : Pourquoi les entreprises existent (علاش كاين المقاولات)",
        "تلبية الحاجات؛ تجميع الموارد؛ القيمة المضافة والربح كاستمرارية؛ دور اجتماعي وجبائي باختصار؛ "
        "ربط فهم المنطق الاقتصادي بموقع الموظف المستقبلي.",
    ),
    21: (
        "Leçon 21 — Les différentes tailles d'entreprises",
        "Leçon 21 : Tailles d'entreprises (الأحجام)",
        "TPE/PME/كبرى/متعددة الجنسيات؛ أنماط التسيير؛ ما ينتظره المشغل من خريج جديد؛ "
        "الأرقام المعيارية للتصنيف: تابع المصادر الرسمية المحدثة.",
    ),
    22: (
        "Leçon 22 — Le business model",
        "Leçon 22 : Business model (النموذج الاقتصادي)",
        "عرض القيمة، الشريحة، نموذج الإيرادات؛ مثال صيانة تصحيحية مقابل وقائية؛ "
        "Business Model مقابل Business Plan؛ ربط الفهم بقراءة عروض الشغل.",
    ),
    23: (
        "Leçon 23 — Anatomie de l'entreprise",
        "Leçon 23 : Anatomie — qui fait quoi (التشريح الوظيفي)",
        "وظائف أساسية وداعمة؛ تدفقات المادة والمعلومة والمال؛ مثال تطبيقي؛ "
        "فهم فين يدخل المتدرب فالسلسلة.",
    ),
    25: (
        "Leçon 25 — La finance d'une entreprise",
        "Leçon 25 : La finance d'une entreprise (مالية المقاولة)",
        "مصادر التمويل؛ الرافعة المالية بحذر؛ دورة الاستغلال؛ الربح مقابل السيولة (الخزينة)؛ "
        "التخطيط المالي — من منظور موظف واعٍ.",
    ),
    26: (
        "Leçon 26 — Le code du travail",
        "Leçon 26 : Le code du travail (مدونة الشغل)",
        "إطار العمل القانوني؛ أنواع العقود؛ فترة التجربة؛ ساعات العمل؛ "
        "التحقق من النصوص المحدثة مع مصادر موثوقة.",
    ),
    27: (
        "Leçon 27 — Processus de recrutement",
        "Leçon 27 : Processus de recrutement (كواليس التوظيف)",
        "من الحاجة للإعلان؛ بطاقة الوظيفة؛ الفرز و ATS؛ الاتصال الأول؛ المقابلات؛ "
        "عدم أخذ الصمت كإهانة شخصية.",
    ),
    28: (
        "Leçon 28 — Personnalité en entreprise",
        "Leçon 28 : La personnalité au sein de l'entreprise (الشخصية)",
        "الشهادة تفتح الباب؛ الذكاء العاطفي؛ العمل الجماعي؛ مرونة التعلم؛ انسجام الثقافة؛ "
        "بناء سمعة مهنية.",
    ),
}

_START_SEQ_M1 = re.compile(
    r"^[\s]*(?:🎥\s*)?[\s]*"
    r"(\(الدخلة|\(الفكرة|\(خاتمة|\(الخاتمة|Séquence\s+\d+)",
    re.I,
)


def is_m2_sequence_start(line: str) -> bool:
    s = (line or "").strip()
    if not s:
        return False
    if _START_SEQ_M1.match(s):
        return True
    if re.match(r"^\d+\.\s", s):
        return True
    if s.startswith("الفقرة "):
        return True
    if s.startswith("Les TPE") or s.startswith("Les 3 Piliers"):
        return True
    if s.startswith("الوظائف الأساسية") or s.startswith("وظائف الدعم"):
        return True
    if s.startswith("وظيفـة ") or s.startswith("وظيفة "):
        return True
    if s.startswith("Script Vidéo") or s.startswith("سكربت"):
        return True
    return False


def extract_paragraphs(path: Path) -> list[str]:
    doc = Document(str(path))
    return [p.text.strip() for p in doc.paragraphs if (p.text or "").strip()]


def postprocess(text: str) -> str:
    t = text
    t = re.sub(r"\bProMind7\b", "proM7", t, flags=re.I)
    t = re.sub(r"\bPM7\b", "proM7", t)
    t = re.sub(r"\bP7\b", "proM7", t)
    t = t.replace("الساروت", "التأهيل الرسمي")
    return t


def paragraphs_to_sequences(paras: list[str]) -> list[tuple[str, list[str]]]:
    sequences: list[tuple[str, list[str]]] = []
    current_title = ""
    current_body: list[str] = []

    for raw in paras:
        line = postprocess(raw).strip()
        if not line:
            continue
        if is_m2_sequence_start(line):
            if current_body:
                tid = current_title or f"Séquence {len(sequences) + 1}"
                sequences.append((tid, current_body.copy()))
            n = len(sequences) + 1
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
            ("Séquence 1 — Script", [postprocess(p).strip() for p in paras if p.strip()]),
        ]
    return sequences


def lesson_paths() -> dict[int, Path]:
    out: dict[int, Path] = {}
    for p in sorted(M2_BACKUP.rglob("*.docx")):
        if "test Module" in str(p):
            continue
        folder = p.parent.name
        try:
            lid = int(folder.split("-", 1)[0])
        except ValueError:
            continue
        if lid == 24:
            continue
        if lid in LESSON_META:
            out[lid] = p
    return out


def py_str_literal(s: str) -> str:
    return repr(s)


def build_file(lessons_data: dict[int, dict]) -> str:
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""',
        "Scripts oraux darija — Module 2 : l'entreprise.",
        "Contenu réimporté depuis les .docx de sauvegarde (développement contenu/scripts/02-Module 2…).",
        "Leçon 24 : volontairement hors scope (demande produit).",
        "Post-traitements : proM7 ; « الساروت » (CV) → « التأهيل الرسمي ».",
        "Régénération Word : python app/tools/format_modules_01_02_scripts.py",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        f"MODULE2_LIGNE_CADRE = {py_str_literal(MODULE2_LIGNE_CADRE)}",
        "",
        "LESSONS: dict[int, dict] = {",
    ]
    for lid in sorted(lessons_data):
        d = lessons_data[lid]
        lines.append(f"    {lid}: {{")
        lines.append(f'        "title": {py_str_literal(d["title"])},')
        lines.append('        "cadre_lignes": (')
        lines.append("            MODULE2_LIGNE_CADRE,")
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
    expected = sorted(LESSON_META.keys())
    missing = [i for i in expected if i not in paths]
    if missing:
        print("Missing lessons:", missing, file=sys.stderr)
        sys.exit(1)

    lessons_data: dict[int, dict] = {}
    for lid in expected:
        paras = extract_paragraphs(paths[lid])
        title, cadre_l2, objectif_ar = LESSON_META[lid]
        seqs = paragraphs_to_sequences(paras)
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
