# -*- coding: utf-8 -*-
"""
Point d’entrée Streamlit : délègue vers ``app/promind7_console.py``.

Lancer depuis ce dossier : ``streamlit run promind7_console.py``
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent
_app = _root / "app"
_inner = _app / "promind7_console.py"

if not _inner.is_file():
    raise SystemExit(
        f"Fichier introuvable : {_inner}\n"
        "Réinstallez ou restaurez app/promind7_console.py."
    )

for _p in (_app, _root):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

runpy.run_path(str(_inner), run_name="__main__")
