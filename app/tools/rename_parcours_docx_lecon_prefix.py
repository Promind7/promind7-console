"""
Renomme les .docx du pack « Parcours stage & emploi » pour que le nom
commence par « Leçon N - … » (N = numéro de la leçon).

Usage (depuis la racine du projet V2) :
    python app/tools/rename_parcours_docx_lecon_prefix.py
    python app/tools/rename_parcours_docx_lecon_prefix.py --dry-run
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PACK_REL = Path("Input") / "Script" / "Parcours stage & emploi"

# Déjà au bon format (Leçon / Lecon / Leçon unicode)
_LECON_OK = re.compile(r"^le[cç]on\s+(\d+)\s*-\s*(.+)$", re.I)
# 09-Titre, 02-Titre, etc.
_LEADING_NUM = re.compile(r"^(\d+)\s*-\s*(.+)$")
# Module 0 - titre (fichier stress module 0)
_MODULE0 = re.compile(r"^module\s+0\s*-\s*(.+)$", re.I)
# Dossier parent 04-xxx, 09-xxx
_PARENT_NUM = re.compile(r"^(\d+)\s*-\s*")
# Ex. « 01-Module 1 - … » : le chiffre est l’index du module, pas la leçon
_MODULE_ROOT = re.compile(r"^\d+\s*-\s*Module\b", re.I)

# test Module N / test Module N.docx → numéro aligné sur la fin du module (tri UI)
_TEST_LESSON_BY_MOD: dict[int, int] = {
    1: 19,
    2: 29,
    3: 32,
    4: 43,
    5: 51,
    6: 56,
    7: 63,
}


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def proposed_stem(stem: str, parent_name: str) -> str | None:
    """
    Retourne le nouveau stem (sans .docx) ou None si inchangé.
    """
    s = stem.strip()
    if not s:
        return None

    m = _LECON_OK.match(s)
    if m:
        n = int(m.group(1))
        rest = m.group(2).strip()
        pm = _PARENT_NUM.match(parent_name)
        # Aligner N sur le préfixe du dossier (ex. 01-Introduction → Leçon 1, pas Leçon 0).
        # On n’aligne pas si le dossier est « 000-… » (fn == 0) ni sur une racine « NN-Module ».
        if pm and not _MODULE_ROOT.match(parent_name):
            fn = int(pm.group(1))
            if fn > 0 and n != fn:
                return f"Leçon {fn} - {rest}"
        canon = f"Leçon {n} - {rest}"
        return canon if canon != s else None

    m = _LEADING_NUM.match(s)
    if m:
        return f"Leçon {int(m.group(1))} - {m.group(2).strip()}"

    m = _MODULE0.match(s)
    if m:
        pm = _PARENT_NUM.match(parent_name)
        if pm:
            rest = m.group(1).strip()
            return f"Leçon {int(pm.group(1))} - {rest}"

    pm = _PARENT_NUM.match(parent_name)
    if (
        pm
        and not _LEADING_NUM.match(s)
        and not _MODULE0.match(s)
        and not _MODULE_ROOT.match(parent_name)
    ):
        return f"Leçon {int(pm.group(1))} - {s}"

    if s.lower() == "brain storming":
        return "Leçon 8 - Brain storming"

    tm = re.match(r"^test Module (\d+)$", parent_name.strip(), re.I)
    if tm:
        mod = int(tm.group(1))
        if s.lower() == f"test module {mod}".lower():
            n = _TEST_LESSON_BY_MOD.get(mod)
            if n is not None:
                return f"Leçon {n} - test Module {mod}"

    return None


def collect_renames(pack: Path, *, dry_run: bool) -> list[tuple[Path, Path]]:
    moves: list[tuple[Path, Path]] = []
    skip_dirs = {"Sources", "V2", "_exports", "Textes_ameliores"}

    for p in sorted(pack.rglob("*.docx")):
        rel_parts = p.relative_to(pack).parts
        if any(part in skip_dirs for part in rel_parts):
            continue
        parent_name = p.parent.name
        new_stem = proposed_stem(p.stem, parent_name)
        if not new_stem:
            continue
        dest = p.with_name(new_stem + p.suffix)
        if dest == p:
            continue
        moves.append((p, dest))

    # Cibles distinctes
    dests = [d for _, d in moves]
    if len(dests) != len(set(dests)):
        from collections import Counter

        c = Counter(str(d) for d in dests)
        dup = [k for k, v in c.items() if v > 1]
        raise SystemExit(f"Collision de noms cibles : {dup[:5]}")

    for src, dst in moves:
        if dst.exists() and dst.resolve() != src.resolve():
            raise SystemExit(f"Cible existe déjà : {dst}")

    if not dry_run:
        # Éviter écrasement si A→B et B→A : renommage en deux passes via noms temporaires
        tmp_suffix = ".__pm7_ren__"
        phase1: list[tuple[Path, Path]] = []
        for i, (src, dst) in enumerate(moves):
            tmp = src.with_name(src.stem + tmp_suffix + str(i) + src.suffix)
            src.rename(tmp)
            phase1.append((tmp, dst))
        for tmp, dst in phase1:
            tmp.rename(dst)

    return moves


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Afficher sans renommer")
    args = ap.parse_args()
    root = _project_root()
    pack = root / PACK_REL
    if not pack.is_dir():
        print("Pack introuvable :", pack, file=sys.stderr)
        return 1

    moves = collect_renames(pack, dry_run=args.dry_run)
    for src, dst in moves:
        print(f"{'[dry-run] ' if args.dry_run else ''}{src.name}")
        print(f"  -> {dst.name}")
    print(f"Total : {len(moves)} fichier(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
