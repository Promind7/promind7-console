"""Audit ponctuel : densité des scripts (caractères / paragraphes). Usage : python app/tools/_audit_lesson_density.py"""
from __future__ import annotations

import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
_ROOT = _TOOLS.parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))


def body_text(item: object) -> str:
    if isinstance(item, tuple) and len(item) == 2:
        return str(item[1] or "")
    return str(item)


def analyze_lessons(lessons: dict, mod_label: str) -> list[dict]:
    rows = []
    for lid in sorted(lessons.keys()):
        data = lessons[lid]
        seqs = data.get("sequences") or []
        n_seq = len(seqs)
        all_lens: list[int] = []
        short_paras = 0
        very_short_seqs = 0
        for _title, bodies in seqs:
            blens = [len(body_text(b).strip()) for b in bodies]
            all_lens.extend(blens)
            if blens:
                if max(blens) < 120:
                    very_short_seqs += 1
                for L, b in zip(blens, bodies):
                    t = body_text(b).strip()
                    if L < 80 and not t.startswith("(") and not t.startswith("Séquence"):
                        short_paras += 1
        total_chars = sum(all_lens)
        n_paras = len(all_lens)
        avg = total_chars / n_paras if n_paras else 0.0
        rows.append(
            {
                "id": lid,
                "mod": mod_label,
                "n_seq": n_seq,
                "n_paras": n_paras,
                "total": total_chars,
                "avg": avg,
                "short_paras": short_paras,
                "very_short_seqs": very_short_seqs,
                "title": (data.get("title") or "")[:60],
            }
        )
    return rows


def main() -> None:
    modules = [
        ("M0", "module00_rich_content", "LESSONS"),
        ("M1", "module01_rich_content", "LESSONS"),
        ("M2", "module02_rich_content", "LESSONS"),
        ("M3", "module03_rich_content", "LESSONS"),
        ("M4", "module04_rich_content", "LESSONS"),
        ("M5", "module05_rich_content", "LESSONS"),
        ("M6", "module06_rich_content", "LESSONS"),
        ("M7", "module07_rich_content", "LESSONS"),
    ]
    all_rows: list[dict] = []
    for mod, mname, lname in modules:
        m = __import__(mname, fromlist=[lname])
        all_rows.extend(analyze_lessons(getattr(m, lname), mod))

    thin = sorted(all_rows, key=lambda r: (r["total"], -r["short_paras"]))
    print("=== 35 leçons les plus légères (total caractères corps de séquences) ===")
    for r in thin[:35]:
        print(
            f"{r['mod']} L{r['id']:3d}  total={r['total']:5d}  avg_para={r['avg']:.0f}  "
            f"seq={r['n_seq']}  paras={r['n_paras']}  courts<80c={r['short_paras']}  "
            f"seq_max<120c={r['very_short_seqs']}  | {r['title']}"
        )

    print()
    print("=== Beaucoup de paragraphes très courts (hors lignes entre parenthèses) ===")
    by_short = sorted(all_rows, key=lambda r: (-r["short_paras"], r["total"]))
    for r in by_short[:25]:
        if r["short_paras"] > 0:
            print(
                f"{r['mod']} L{r['id']:3d}  courts={r['short_paras']:3d}  total={r['total']:5d}  | {r['title']}"
            )

    # Médiane globale
    totals = sorted(r["total"] for r in all_rows)
    med = totals[len(totals) // 2]
    print()
    print(f"Médiane total caractères / leçon : {med}")


if __name__ == "__main__":
    main()
