from __future__ import annotations

from pathlib import Path
import sys

# app/ + racine projet (dossier contenant app/, db/, Input/, tutor_lms/)
_app = Path(__file__).resolve().parent
_repo = _app.parent
for _p in (_app, _repo):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

import streamlit as st

from db import init_db, get_connection
from ui.styles import inject_global_styles

from ui.dashboard_ui import render_dashboard_tab
from ui.team_ui import render_team_tab
from ui.tasks_ui import render_tasks_tab
from ui.learners_ui import render_learners_tab
from ui.parcours_ui import render_parcours_tab
from ui.admin_ui import render_admin_tab
from ui.calendar_page import render as render_calendar_tab
from ui.redaction_ui import render_redaction_tab


def _render_tab_safe(label: str, render_fn) -> None:
    """Évite qu’une exception dans un onglet fasse planter toute l’application."""
    try:
        render_fn()
    except Exception as e:
        st.error(
            f"Impossible d’afficher la section « {label} » pour le moment. "
            "Réessayez ou ouvrez Admin → Base & imports → « Rafraîchir les données »."
        )
        with st.expander("Détails techniques", expanded=False):
            st.exception(e)


def ensure_team_schema() -> None:
    """
    S'assure que :
    - la table team_members existe,
    - la colonne 'assignee' existe dans la table tasks,
    - quelques membres d'équipe par défaut sont présents.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Création de la table team_members si elle n'existe pas
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS team_members (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
        """
    )

    # Ensure extended profile columns exist
    cur.execute("PRAGMA table_info(team_members);")
    cols = [row[1] for row in cur.fetchall()]
    def _ensure_column(col_name: str, col_type: str) -> None:
        if col_name not in cols:
            cur.execute(f"ALTER TABLE team_members ADD COLUMN {col_name} {col_type};")

    _ensure_column("first_name", "TEXT")
    _ensure_column("last_name", "TEXT")
    _ensure_column("email", "TEXT")
    _ensure_column("phone", "TEXT")
    _ensure_column("role", "TEXT")
    _ensure_column("birthdate", "TEXT")
    _ensure_column("bio", "TEXT")

    # Ajout de la colonne assignee dans tasks si elle n'existe pas
    cur.execute("PRAGMA table_info(tasks);")
    cols = [row[1] for row in cur.fetchall()]
    if "assignee" not in cols:
        cur.execute("ALTER TABLE tasks ADD COLUMN assignee TEXT;")
    conn.commit()
    conn.close()


def main() -> None:
    # Configuration de la page
    st.set_page_config(
        page_title="Promind7 — Console",
        page_icon="PM7",
        layout="wide",
    )

    # Une seule injection CSS (évite les doublons à chaque onglet / rerun)
    inject_global_styles()

    st.title("Promind7 — Console")

    # Initialisation de la base
    init_db()
    ensure_team_schema()

    # Définition des onglets
    (
        tab_dashboard,
        tab_team,
        tab_parcours,
        tab_redaction,
        tab_students,
        tab_tasks,
        tab_calendar,
        tab_admin,
    ) = st.tabs(
        [
            "Dashboard",
            "Team",
            "Parcours",
            "Rédaction & scripts",
            "Apprenants",
            "Tâches",
            "Calendrier",
            "Admin",
        ]
    )

    with tab_dashboard:
        _render_tab_safe("Dashboard", render_dashboard_tab)

    with tab_team:
        _render_tab_safe("Team", render_team_tab)

    with tab_parcours:
        _render_tab_safe("Parcours", render_parcours_tab)

    with tab_redaction:
        _render_tab_safe("Rédaction & scripts", render_redaction_tab)

    with tab_students:
        _render_tab_safe("Apprenants", render_learners_tab)

    with tab_tasks:
        _render_tab_safe("Tâches", render_tasks_tab)

    with tab_calendar:
        _render_tab_safe("Calendrier", render_calendar_tab)

    with tab_admin:
        _render_tab_safe("Admin", render_admin_tab)


if __name__ == "__main__":
    main()

