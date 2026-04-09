"""
Cache Streamlit (`st.cache_data`) pour limiter les lectures SQLite répétées.

- Version dans `st.session_state` : incrémenter après import Tutor (ou bouton Rafraîchir).
- TTL court en secours si la version n’est pas bumpée.
"""
from __future__ import annotations

import streamlit as st

PM7_CACHE_VERSION_KEY = "_pm7_data_cache_version"

# TTL (secondes) si aucun bump de version — évite données trop vieilles en session longue
_CACHE_TTL = 180


def get_pm7_cache_version() -> int:
    return int(st.session_state.get(PM7_CACHE_VERSION_KEY, 0))


@st.cache_data(ttl=_CACHE_TTL, show_spinner=False)
def cached_get_all_tutor_courses(_version: int) -> list[dict]:
    """Liste des cours Tutor LMS (miroir DB), pour l’onglet Parcours."""
    from services.tutor_lms_service import get_all_courses

    return get_all_courses()


@st.cache_data(ttl=_CACHE_TTL, show_spinner=False)
def cached_list_parcours_for_tasks(_version: int) -> list[dict]:
    """Lignes parcours pour l’onglet Tâches (tutor_courses + courses.code)."""
    from db import get_connection, list_parcours_for_tasks

    conn = get_connection()
    try:
        return list_parcours_for_tasks(conn)
    finally:
        conn.close()


@st.cache_data(ttl=_CACHE_TTL, show_spinner=False)
def cached_pack_enrollment_stats(_version: int) -> list[dict]:
    """Statistiques d’inscriptions par parcours (Dashboard)."""
    from db.queries.students import list_pack_enrollment_stats

    return list_pack_enrollment_stats()


@st.cache_data(ttl=_CACHE_TTL, show_spinner=False)
def cached_dashboard_counts(_version: int) -> dict:
    """Compteurs vue d’ensemble (parcours, modules, leçons, apprenants)."""
    from db import (
        count_active_learners,
        count_courses,
        count_lessons,
        count_modules,
        count_students,
    )

    return {
        "nb_courses": count_courses(),
        "nb_modules": count_modules(),
        "nb_lessons": count_lessons(),
        "total_students": count_students(),
        "active_learners": count_active_learners(),
    }


def bump_pm7_data_cache() -> None:
    """Invalide les caches dépendant de la version (import Tutor, action manuelle).

    Note Streamlit Cloud : ``@st.cache_data`` est **global** à toutes les sessions.
    Sans ``.clear()``, une première visite (base vide) peut figer une liste de cours
    vide pour la clé ``(_version=0,)`` ; les autres onglets / nouvelles sessions
    restent vides jusqu’au TTL même après import. D’où l’invalidation explicite.
    """
    st.session_state[PM7_CACHE_VERSION_KEY] = get_pm7_cache_version() + 1
    cached_get_all_tutor_courses.clear()
    cached_list_parcours_for_tasks.clear()
    cached_pack_enrollment_stats.clear()
    cached_dashboard_counts.clear()

