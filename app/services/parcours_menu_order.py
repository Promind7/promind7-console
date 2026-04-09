"""
Ordre d’affichage des parcours (menu produit), aligné sur **Architecture plateforme Promind7** §4.
"""
from __future__ import annotations

import unicodedata
from typing import Any


def norm_title_ascii_lower(title: str | None) -> str:
    s = unicodedata.normalize("NFKD", title or "")
    return s.encode("ascii", "ignore").decode("ascii").lower()


def parcours_menu_sort_key_from_title(title: str | None) -> tuple[int, str]:
    """
    Clé de tri pour les titres Tutor / parcours (§4) :
    adhésion communauté / abonnement → orientation lycéen → stage & emploi → évolution → expertise → mental.
    """
    t = norm_title_ascii_lower(title)
    if (
        "abonnement" in t
        or "podcast" in t
        or "adhesion" in t
        or "communaute" in t
        or "community" in t
        or "membership" in t
    ):
        rank = 0
    elif "orientation" in t and "lyceen" in t:
        rank = 1
    elif "stage" in t and "emploi" in t:
        rank = 2
    elif "evolution" in t and "professionnelle" in t:
        rank = 3
    elif "expertise" in t and "professionnelle" in t:
        rank = 4
    elif "mental" in t:
        rank = 5
    else:
        rank = 99
    return (rank, t)


def sort_parcours_entries_by_menu_order(
    entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return sorted(
        entries,
        key=lambda e: parcours_menu_sort_key_from_title(e.get("title")),
    )


def parcours_menu_sort_key_course(course: dict) -> tuple[int, str]:
    """Compat : dict type retour par get_all_courses()."""
    return parcours_menu_sort_key_from_title(course.get("title"))
