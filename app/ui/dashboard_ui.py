"""
Composant UI pour le Dashboard ProMind7.
Affiche les KPIs, synthèses et données clés (lecture seule).
"""

import streamlit as st


# ============================================================
#  TABLEAU DE BORD PRINCIPAL
# ============================================================
def render_dashboard_tab():
    """Affiche le tableau de bord principal ProMind7 (KPI + tableaux)."""
    import pandas as pd

    from db import count_open_tasks, count_tasks
    from ui.pm7_cache import (
        cached_dashboard_counts,
        cached_pack_enrollment_stats,
        get_pm7_cache_version,
    )

    st.title("Dashboard ProMind7")

    v = get_pm7_cache_version()
    counts = cached_dashboard_counts(v)
    enrollment_rows = cached_pack_enrollment_stats(v)

    st.subheader("Vue d'ensemble")
    _render_kpis_dashboard(counts)

    st.markdown("---")

    # Compteurs tâches non mis en cache : les onglets s’exécutent avant « Tâches » dans le script ;
    # un cache ici resterait faux sur le même cycle après une modification de tâche.
    st.subheader("Suivi de l'activité")
    _render_tasks_section_dashboard(count_open_tasks, count_tasks)

    st.markdown("---")

    st.subheader("Répartition des inscriptions")
    _render_learners_by_pack_dashboard(enrollment_rows, pd)


def _card(label: str, value: str | int, help_text: str = None):
    """Renders a styled metric card."""
    tooltip = f'title="{help_text}"' if help_text else ""
    st.markdown(
        f"""
        <div class="metric-card" {tooltip}>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpis_dashboard(counts: dict):
    """KPIs structure Tutor LMS & ProMind7 (données déjà agrégées / cachées)."""
    nb_courses = counts["nb_courses"]
    nb_modules = counts["nb_modules"]
    nb_lessons = counts["nb_lessons"]
    total_students = counts["total_students"]
    active_learners = counts["active_learners"]

    # Row 1: Content Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        _card("Parcours actifs", nb_courses)
    with col2:
        _card("Apprenants", total_students)
    with col3:
        _card("Inscrits", active_learners)
    with col4:
        _card("Modules", nb_modules)
    with col5:
        _card("Leçons", nb_lessons)


def _render_tasks_section_dashboard(count_open_tasks, count_tasks):
    """KPIs des tâches ProMind7 (lecture directe, toujours à jour)."""
    open_count = count_open_tasks()
    done_count = count_tasks(status="done")
    total = open_count + done_count
    completion_rate = int((done_count / total * 100)) if total > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        _card("Tâches en cours", open_count)
    with col2:
        _card("Tâches terminées", done_count)
    with col3:
        _card("Taux complétion", f"{completion_rate}%")


def _render_learners_by_pack_dashboard(rows: list, pd):
    """Affiche graphiques et tableau des apprenants par parcours (cours Tutor LMS)."""
    if not rows:
        st.info("Aucune donnée d'inscription disponible pour le graphique.")
        return

    df_packs = pd.DataFrame(rows)
    df_packs["Parcours"] = df_packs["course_title"]

    # Tri alphabétique simple pour correspondre aux autres onglets
    df_packs["sort_key"] = df_packs["Parcours"].astype(str).str.lower()
    df_packs = df_packs.sort_values(by="sort_key")

    col_chart, col_data = st.columns([1.5, 1])

    with col_chart:
        st.caption("Inscriptions par parcours")
        # Simple bar chart
        st.bar_chart(
            data=df_packs,
            x="Parcours",
            y="enrollments",
            color="#0F879B", 
            use_container_width=True
        )

    with col_data:
        st.caption("Détails chiffrés")
        df_display = df_packs[["Parcours", "enrollments"]].rename(
            columns={"enrollments": "Inscriptions"}
        )
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            height=300,
        )
