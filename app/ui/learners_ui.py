"""
Composant UI pour l'onglet Apprenants.

Lecture seule : profils issus de Tutor LMS + enrichissement ProMind7.
"""

import streamlit as st

from db import list_students, list_students_without_packs
from services.learners_service import (
    get_student,
    list_student_enrollments,
    list_course_learners,
    list_pack_enrollment_stats,
)
import re

def _pack_sort_key(title_or_none):
    # Tri alphabétique simple pour correspondre à l’onglet Parcours
    title = str(title_or_none or "")
    return title.lower()


def render_learners_tab():
    st.title("Apprenants")

    learners = list_students()
    if not learners:
        st.info(
            "Aucun apprenant en base. Les fiches viennent des inscriptions dans "
            "`tutor_lms/.../enrollments.json` (import Admin). Si le dépôt n’a pas d’inscriptions "
            "dans ces fichiers, exporte à nouveau depuis Tutor avec les données utilisateurs, "
            "puis relance l’import — local et Streamlit utiliseront la même source."
        )
        return

    learners_by_id = {s["id"]: s for s in learners}

    tab_profil, tab_parcours, tab_prospects = st.tabs(
        ["Par apprenant", "Par parcours", "Clients potentiels"]
    )

    # ==================================================
    # PARTIE 1 : VUE PAR APPRENANT
    # ==================================================
    with tab_profil:
        st.subheader("Recherche")

        search = st.text_input(
            "Rechercher par nom ou email",
            key="learners_search",
        ).strip().lower()

        filtered = (
            [
                s
                for s in learners
                if search in (s.get("name") or "").lower()
                or search in (s.get("email") or "").lower()
            ]
            if search
            else learners
        )

        if not filtered:
            st.warning("Aucun apprenant ne correspond à cette recherche.")
            return

        selected_id = st.selectbox(
            "Sélectionnez un apprenant",
            options=[s["id"] for s in filtered],
            format_func=lambda sid: learners_by_id[sid]["name"]
            or f"Apprenant #{sid}",
            key="learners_select",
        )

        student = get_student(selected_id)
        if not student:
            st.error("Apprenant introuvable.")
            return

        enrollments = list_student_enrollments(student["id"])

        col_left, col_right = st.columns([2, 3])

        # ----- Identité -----
        with col_left:
            st.subheader("Identité & contact")

            st.markdown(f"**Nom :** {student.get('name') or 'Inconnu'}")
            st.markdown(f"**Email :** {student.get('email') or 'Non renseigné'}")

            st.markdown("---")
            st.subheader("Profil apprenant ProMind7")

            st.markdown(
                f"**Téléphone :** {student.get('phone') or 'Non renseigné'}"
            )
            st.markdown(
                f"**Date de naissance :** {student.get('birthdate') or 'Non renseignée'}"
            )
            st.markdown(
                f"**Établissement :** {student.get('school') or 'Non renseignée'}"
            )
            st.markdown(
                f"**Niveau :** {student.get('level') or 'Non renseigné'}"
            )
            st.markdown(
                f"**Parent :** {student.get('parent_name') or 'Non renseigné'}"
            )
            st.markdown(
                f"**Téléphone parent :** {student.get('parent_phone') or 'Non renseigné'}"
            )
            st.markdown(
                f"**Email parent :** {student.get('parent_email') or 'Non renseigné'}"
            )

            st.markdown("**Profil / contexte**")
            st.write(student.get("profile") or "Aucun profil apprenant renseigné.")

        # ----- Parcours (cours Tutor LMS) -----
        with col_right:
            st.subheader("Historique des parcours / cours")

            if not enrollments:
                st.info("Aucune inscription enregistrée.")
            else:
                for e in enrollments:
                    code = e.get("course_code")
                    title = e.get("course_title") or "Cours sans titre"
                    status = e.get("status") or "statut inconnu"
                    date = e.get("enrolled_at") or "date inconnue"

                    # ID prefix logic removed
                    title = title

                    st.markdown(f"- **{title}** ({status}) – {date}")

            st.markdown("---")
            with st.expander("Autres apprenants inscrits sur un parcours", expanded=False):
                if enrollments:
                    pack_options = {
                        e["course_tutor_id"]: (e.get("course_code"), e.get("course_title"))
                        for e in enrollments
                    }

                    ordered_ids = sorted(
                        pack_options.keys(),
                        key=lambda cid: _pack_sort_key(pack_options[cid][1]),
                    )

                    def _pack_label(cid: int) -> str:
                        code, title = pack_options[cid]
                        title = title or "Cours sans titre"
                        # ID prefix logic removed
                        return title

                    selected_course_id = st.selectbox(
                        "Choisir un parcours",
                        options=ordered_ids,
                        format_func=_pack_label,
                        key="learners_pack_select_individual",
                    )

                    other_learners = list_course_learners(selected_course_id)
                    if other_learners:
                        # Exclure l'apprenant actuel de la liste
                        others = [l for l in other_learners if l.get("student_id") != student["id"]]
                        
                        if others:
                            st.markdown("**Autres apprenants :**")
                            for l in others:
                                st.markdown(
                                    f"- {l.get('name') or 'Apprenant'} "
                                    f"({l.get('email') or 'email inconnu'}) – "
                                    f"{l.get('status') or 'statut inconnu'} – "
                                    f"{l.get('enrolled_at') or 'date inconnue'}"
                                )
                        else:
                             st.info("Aucun autre apprenant inscrit sur ce parcours.")
                    else:
                        st.info("Aucun autre apprenant.")
                else:
                    st.info(
                        "Sélectionnez un apprenant qui a au moins un parcours pour voir les autres inscrits."
                    )

    # ==================================================
    # PARTIE 2 : VUE PAR PARCOURS
    # ==================================================
    with tab_parcours:
        st.subheader("Vue globale par parcours")

        pack_stats = list_pack_enrollment_stats()
        if not pack_stats:
            st.info("Aucune inscription enregistrée.")
            return

        sorted_stats = sorted(
            pack_stats,
            key=lambda r: _pack_sort_key(r.get("course_title"))
        )

        total_enrollments = sum(p.get("enrollments") or 0 for p in sorted_stats)

        options = [(f"Tous les parcours ({total_enrollments})", None)]
        options += [
            (
                f"{p.get('course_title') or 'Cours sans titre'} ({p.get('enrollments') or 0})",
                p["course_tutor_id"],
            )
            for p in sorted_stats
        ]

        selected_label = st.selectbox(
            "Choisir un parcours",
            options=[label for (label, _) in options],
            key="learners_pack_select_global",
        )
        selected_value = next(v for (label, v) in options if label == selected_label)

        st.subheader("Apprenants inscrits")

        # ----- Tous les parcours -----
        if selected_value is None:
            for p in sorted_stats:
                if (p.get("enrollments") or 0) > 0:
                    st.markdown(f"#### {p.get('course_title')}")
                    learners_for_pack = list_course_learners(p["course_tutor_id"])
                    for l in learners_for_pack:
                        st.markdown(
                            f"- {l.get('name')} ({l.get('email')}) — "
                            f"{l.get('status')} — {l.get('enrolled_at')}"
                        )

        # ----- Parcours individuel -----
        else:
            selected_pack = next(
                p for p in sorted_stats if p["course_tutor_id"] == selected_value
            )
            learners_for_pack = list_course_learners(selected_value)

            if learners_for_pack:
                st.markdown(f"#### {selected_pack.get('course_title')}")
                for l in learners_for_pack:
                    st.markdown(
                        f"- {l.get('name')} ({l.get('email')}) — "
                        f"{l.get('status')} — {l.get('enrolled_at')}"
                    )
            else:
                st.info("Aucun inscrit.")

    # ==================================================
    # PARTIE 3 : CLIENTS POTENTIELS
    # ==================================================
    with tab_prospects:
        st.subheader("Apprenants sans parcours")

        potential_students = list_students_without_packs()

        if potential_students:
            import pandas as pd

            df = pd.DataFrame(
                [
                    {
                        "Nom": s["name"],
                        "Email": s["email"],
                        "Téléphone": s["phone"],
                        "Établissement": s["school"],
                        "Niveau": s["level"],
                    }
                    for s in potential_students
                ]
            ).sort_values(by="Nom", kind="stable")

            st.caption(f"{len(df)} apprenant(s) sans parcours.")
            st.dataframe(df, use_container_width=True)
        else:
            st.caption("Aucun inscrit sans parcours pour le moment.")
