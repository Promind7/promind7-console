"""
Service Dashboard ProMind7.

Expose des fonctions de haut niveau pour le tableau de bord :
- KPI globaux
- statistiques par pack
- timeline des inscriptions
- apprenants à risque

Toute la logique métier reste ici.
Aucun code Streamlit dans ce fichier.
"""

from db import (
    count_courses,
    count_active_learners,
    count_total_tutor_enrollments,
    count_open_tasks,
    count_high_priority_open_tasks,
    list_pack_enrollment_stats,
    list_enrollment_timeline,
    list_risky_learners,
)


def get_global_kpis() -> dict:
    """Retourne les KPI globaux pour le Dashboard."""
    return {
        "students": count_active_learners(),
        "packs": count_courses(),
        "total_enrollments": count_total_tutor_enrollments(),
        "open_tasks": count_open_tasks(),
        "high_priority_open_tasks": count_high_priority_open_tasks(),
    }


def get_pack_stats():
    """Retourne les statistiques d'inscriptions par pack."""
    return list_pack_enrollment_stats()


def get_enrollment_timeline():
    """Retourne la timeline journalière des inscriptions."""
    raw_rows = list_enrollment_timeline()
    return [
        {"day": row["date"], "enrollments": row["enrollments"]}
        for row in raw_rows
    ]


def get_risky_learners(limit: int = 10):
    """Apprenants à surveiller (annulations sans complétion)."""
    return list_risky_learners(limit=limit)
