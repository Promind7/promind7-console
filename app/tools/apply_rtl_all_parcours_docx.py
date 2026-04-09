"""
Applique la lecture RTL (droite → gauche) à tous les .docx du pack
« Parcours stage & emploi » (w:bidi + w:rtl), hors dossiers réservés.

Usage (racine du projet V2) :
    python app/tools/apply_rtl_all_parcours_docx.py
"""
from __future__ import annotations

import sys
from pathlib import Path

_APP_DIR = Path(__file__).resolve().parent.parent
_REPO_ROOT = _APP_DIR.parent
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

from docx import Document

from ai.word_rtl import apply_rtl_to_document

PACK = _REPO_ROOT / "Input" / "Script" / "Parcours stage & emploi"
SKIP_PARTS = frozenset({"Sources", "V2", "_exports", "Textes_ameliores"})


def main() -> int:
    if not PACK.is_dir():
        print("Pack introuvable :", PACK, file=sys.stderr)
        return 1
    ok = 0
    err = 0
    for path in sorted(PACK.rglob("*.docx")):
        rel_parts = path.relative_to(PACK).parts
        if any(p in SKIP_PARTS for p in rel_parts):
            continue
        try:
            doc = Document(str(path))
            apply_rtl_to_document(doc)
            doc.save(str(path))
            print("OK", path.relative_to(PACK))
            ok += 1
        except Exception as e:
            print("ERR", path.relative_to(PACK), e, file=sys.stderr)
            err += 1
    print(f"Terminé : {ok} fichier(s), {err} erreur(s).")
    return 0 if err == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
