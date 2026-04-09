"""
Composant UI pour l’onglet Parcours.

Affiche l’import Tutor LMS (via Admin) et la navigation cours / modules / leçons
en lecture seule, via services/tutor_lms_service.py et db.get_connection.
"""

from __future__ import annotations

import streamlit as st

from services.parcours_menu_order import parcours_menu_sort_key_course
from ui.pm7_cache import cached_get_all_tutor_courses, get_pm7_cache_version
from services.tutor_lms_service import (
    get_course_details,
    get_modules_for_course,
    get_lessons_for_module,
)


def render_parcours_tab() -> None:
    """Affiche l’onglet Parcours (miroir Tutor LMS en lecture seule)."""
    st.title("Parcours — vue miroir Tutor LMS (lecture seule)")
    st.markdown(
        "Cette section affiche une vue en lecture seule des parcours (cours Tutor LMS), "
        "modules et leçons issus de l’export importé depuis le dossier projet "
        "`tutor_lms/` à la racine du dépôt (import Admin)."
    )

    courses = cached_get_all_tutor_courses(get_pm7_cache_version())
    if not courses:
        st.info(
            "Aucun cours Tutor LMS en base. Dépose l’export décompressé dans `tutor_lms/` "
            "à la racine du dépôt, puis lance l’import depuis l’onglet Admin."
        )
        return

    sorted_courses = sorted(courses, key=parcours_menu_sort_key_course)

    label_to_id = {
        (c["title"] or f"Cours {c['tutor_id']}"): c["tutor_id"] for c in sorted_courses
    }

    st.subheader("Sélection du parcours")
    selected_label = st.selectbox(
        "Sélectionner un parcours (cours Tutor LMS) :",
        list(label_to_id.keys()),
        key="parcours_course_select",
    )
    selected_tutor_id = label_to_id[selected_label]

    selected = get_course_details(selected_tutor_id)

    if selected:
        st.subheader("Détails du parcours")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Titre :** {selected.get('title') or '-'}")
            st.markdown(f"**Statut :** {selected.get('status') or '-'}")

        with col2:
            st.markdown(f"**Créé le :** {selected.get('created_at') or '-'}")
            st.markdown(f"**Modifié le :** {selected.get('updated_at') or '-'}")

        cats = selected.get("categories")
        tags = selected.get("tags")
        if cats or tags:
            with st.expander("Catégories & tags", expanded=False):
                if cats:
                    st.markdown("**Catégories :** " + ", ".join(map(str, cats)))
                if tags:
                    st.markdown("**Tags :** " + ", ".join(map(str, tags)))

    st.markdown("---")

    st.subheader("Modules du parcours")

    modules = get_modules_for_course(selected_tutor_id)
    if not modules:
        st.info("Aucun module trouvé pour ce parcours.")
        return

    for mod in modules:
        module_title = mod.get("title") or "Module sans titre"
        with st.expander(module_title, expanded=False):
            st.markdown(f"**Statut :** {mod.get('status') or '-'}")

            lessons = get_lessons_for_module(mod["tutor_id"])
            if not lessons:
                st.info("Aucune leçon dans ce module.")
            else:
                st.markdown("#### Leçons")
                for les in lessons:
                    lesson_title = les.get("title") or "Leçon sans titre"
                    st.markdown(f"- **{lesson_title}**")

                    info_bits = []
                    if les.get("lesson_type"):
                        info_bits.append(f"Type : {les['lesson_type']}")
                    if les.get("duration"):
                        info_bits.append(f"Durée : {les['duration']}")

                    if info_bits:
                        st.markdown("  " + " | ".join(info_bits))
