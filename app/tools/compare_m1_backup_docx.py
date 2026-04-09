# -*- coding: utf-8 -*-
"""Compare Module 1 Word scripts: backup (développement contenu) vs V2 pack. Read-only on both."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from docx import Document
except ImportError:
    print("python-docx required", file=sys.stderr)
    sys.exit(1)

PROMIND7 = Path(r"D:\Promind7")
DEV = next(PROMIND7.glob("d*veloppement contenu"), None)
if not DEV:
    print("Could not find développement contenu", file=sys.stderr)
    sys.exit(1)
M1_BACKUP = next((DEV / "scripts").glob("01-Module 1*"), None)
if not M1_BACKUP:
    print("Could not find 01-Module 1 under backup scripts", file=sys.stderr)
    sys.exit(1)

ROOT_V2 = Path(__file__).resolve().parent.parent.parent
M1_V2 = next((ROOT_V2 / "Input/Script/Parcours stage & emploi").glob("01-Module 1*"), None)
if not M1_V2:
    print("Could not find 01-Module 1 under V2 pack", file=sys.stderr)
    sys.exit(1)


def extract_paragraphs(doc_path: Path) -> list[str]:
    doc = Document(str(doc_path))
    return [p.text.strip() for p in doc.paragraphs if (p.text or "").strip()]


def stats(path: Path) -> tuple[int, int]:
    paras = extract_paragraphs(path)
    return len(paras), len("\n".join(paras))


def main() -> None:
    lesson_backup = [
        p
        for p in sorted(M1_BACKUP.rglob("*.docx"))
        if "Brain storming" not in str(p) and "test Module" not in str(p)
    ]

    rows: list[tuple[str, int, int, int, int]] = []
    for bpath in sorted(lesson_backup, key=lambda x: str(x)):
        rel = bpath.relative_to(M1_BACKUP)
        prefix = bpath.parent.name.split("-", 1)[0].strip()
        v2_folder = next(
            (d for d in M1_V2.iterdir() if d.is_dir() and d.name.startswith(prefix + "-")),
            None,
        )
        v2_matches = list(v2_folder.glob("*.docx")) if v2_folder else []
        if not v2_matches:
            bp, bc = stats(bpath)
            rows.append((str(rel), bp, bc, 0, 0))
            continue
        bp, bc = stats(bpath)
        vp, vc = stats(v2_matches[0])
        rows.append((str(rel), bp, bc, vp, vc))

    report = ROOT_V2 / "reports" / "m1_backup_vs_v2_docx.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    md = [
        "# Module 1 — comparaison `.docx` (sauvegarde `développement contenu` vs dépôt V2)",
        "",
        "La sauvegarde **n’a pas été modifiée**.",
        "",
        "| Leçon (dossier) | Paragraphes backup | Caractères backup | Paragraphes V2 | Caractères V2 | Écart car. |",
        "|-----------------|-------------------:|------------------:|---------------:|--------------:|-----------:|",
    ]
    for rel, bp, bc, vp, vc in rows:
        folder = rel.replace("\\", "/").split("/")[0]
        md.append(f"| `{folder}` | {bp} | {bc} | {vp} | {vc} | {vc - bc:+d} |")
    md.append("")
    md.append(
        "**Synthèse** : le `.docx` **V2** ajoute le **cadre** (2 lignes), **الهدف** + texte d’objectif, et un titre **Séquence N** par bloc — d’où un léger **surplus** de caractères par rapport au backup « brut ». "
        "Le **corps darija** du V2 est réimporté depuis le backup ; comparer l’écart global avant/après réimport dans l’historique du dépôt."
    )
    md.append("")
    report.write_text("\n".join(md), encoding="utf-8")
    print("OK ->", report)


if __name__ == "__main__":
    main()
