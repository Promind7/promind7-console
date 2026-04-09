"""
Composant UI pour l'onglet Admin.

Affiche des informations techniques (taille de base), l'import Tutor LMS
depuis un dossier local (résolution auto), l'historique d'import, ainsi que les membres et apprenants.
"""

import streamlit as st

from db import (
    get_connection,
    get_db_path,
    list_students,
    list_students_with_packs,
    list_students_without_packs,
)
from services.admin_service import (
    get_database_size,
    format_db_size,
    get_import_history,
    ensure_import_history_table,
)
from services.tutor_lms_service import import_tutor_zip_folder
from services.team_members_service import (
    list_team_members,
    get_team_member,
    create_member,
    update_member,
    delete_member,
)
from services.learners_service import (
    list_students as svc_list_students,
    get_student as svc_get_student,
    list_student_enrollments as svc_list_student_enrollments,
    update_profile as svc_update_learner_profile,
)
from ai.paths import tutor_lms_export_root_default
from ui.pm7_cache import bump_pm7_data_cache


def render_admin_tab():
    """Affiche l'onglet d'administration ProMind7."""
    st.title("Admin ProMind7")

    tab_db, tab_members, tab_learners = st.tabs(
        ["Base & imports", "Membres", "Apprenants"]
    )

    with tab_db:
        # Base de donnees
        st.subheader("Base de donnees")
        db_size = get_database_size(get_db_path())
        st.metric("Taille de la base SQLite", format_db_size(db_size))

        st.subheader("Cache de l’interface")
        st.caption(
            "Listes parcours (onglets Parcours, Tâches) et agrégats du dashboard sont "
            "mis en cache (~3 min) ou actualisés après un import Tutor ci-dessous."
        )
        if st.button("Rafraîchir les données", key="admin_refresh_pm7_cache", type="secondary"):
            bump_pm7_data_cache()
            st.rerun()

        with st.expander("Historique et import Tutor LMS", expanded=False):
            _render_import_zip()

            conn = get_connection()
            try:
                ensure_import_history_table(conn)
                history = get_import_history(conn)
            finally:
                conn.close()

            if not history:
                st.info("Aucun import journalise pour le moment.")
            else:
                table = {
                    "Date": [row["imported_at"] for row in history],
                    "Fichier": [row["zip_name"] for row in history],
                    "Taille": [format_db_size(row["zip_size"] or 0) for row in history],
                    "Cours": [row["nb_courses"] for row in history],
                    "Modules": [row["nb_modules"] for row in history],
                    "Lecons": [row["nb_lessons"] for row in history],
                    "Statut": [row["status"] for row in history],
                    "Erreur": [row["error_message"] for row in history],
                }
                st.table(table)

        # NOTE ProMind7 :
        # La section "Import V3 – API Tutor LMS (Beta)" a été désactivée.
        # L'import apprenants se fait via l'export décompressé (résolution auto du dossier source).
        # Le code d'intégration API reste présent dans integrations/ et services/
        # pour d'éventuelles évolutions futures (V3.1).

    with tab_members:
        st.header("Gestion des membres ProMind7 - Profils")
        with st.expander("Creer / modifier / supprimer un membre", expanded=True):
            _render_member_crud()

    with tab_learners:
        st.header("Gestion des apprenants ProMind7")
        with st.expander(
            "Modifier le profil d'un apprenant (import Tutor LMS)",
            expanded=False,
        ):
            _render_learners_profiles()


def _render_import_zip():
    st.subheader("Imports Tutor LMS")
    with st.expander("Importer depuis le dossier Tutor LMS (résolution auto)", expanded=False):
        export_root_path = tutor_lms_export_root_default().resolve()
        export_root = str(export_root_path)
        st.markdown(
            "**Source import :** "
            "`PROMIND7_TUTOR_LMS_ROOT` (si défini), sinon **`03-Streamlit/04-tutorLMS`** en local "
            "s’il contient `courses/`, sinon **`tutor_lms/` à la racine du dépôt** (celui utilisé sur le cloud). "
            "Après une mise à jour locale dans `04-tutorLMS`, recopiez vers `tutor_lms/` puis poussez Git."
        )
        st.code(export_root, language=None)
        if not export_root_path.is_dir():
            st.warning(
                "Ce dossier est absent dans l'environnement d'exécution courant. "
                "Placez l'export Tutor dans ce chemin, ou définissez `PROMIND7_TUTOR_LMS_ROOT`, "
                "puis relancez l'import."
            )
        st.caption(
            "Après import : miroir cours + inscriptions alignés sur la source détectée ; "
            "les apprenants affichés sont reconstruits depuis `tutor_enrollments` (plus besoin de supprimer la base à la main). "
            "Les cours absents du dossier sont retirés du miroir SQLite."
        )
        if st.button("Lancer l'import", key="admin_tutor_import_btn"):
            if not export_root_path.is_dir():
                st.error("Le dossier source Tutor LMS est introuvable ou n’est pas un répertoire.")
                return

            conn = None
            try:
                conn = get_connection()
                with st.spinner("Import en cours..."):
                    result = import_tutor_zip_folder(export_root, conn=conn)
                    nb_courses, nb_modules, nb_lessons = result

                st.success(
                    f"Import termine : {nb_courses} cours, "
                    f"{nb_modules} modules, {nb_lessons} lecons."
                )
                bump_pm7_data_cache()
                st.rerun()
            except Exception as e:
                st.error(f"Erreur pendant l'import : {e}")
            finally:
                if conn:
                    conn.close()


def _render_member_crud():
    st.subheader("Profils membres ProMind7")

    members = list_team_members()
    members_by_id = {m["id"]: m for m in members}

    col_left, col_right = st.columns([2, 3])

    with col_left:
        st.subheader("Creer / modifier un membre")

        mode = st.radio(
            "Mode",
            options=["Creer un nouveau membre", "Modifier / supprimer un membre existant"],
            key="admin_member_mode",
        )

        if mode == "Creer un nouveau membre":
            create_first_name = st.text_input("Prenom", key="create_member_first_name")
            create_last_name = st.text_input("Nom", key="create_member_last_name")
            create_email = st.text_input("Email", key="create_member_email")
            create_phone = st.text_input("Telephone", key="create_member_phone")
            create_role = st.text_input("Fonction dans ProMind7", key="create_member_role")
            create_birthdate = st.text_input(
                "Date de naissance (YYYY-MM-DD, optionnel)",
                key="create_member_birthdate",
            )
            create_bio = st.text_area(
                "Bibliographie / Profil detaille",
                key="create_member_bio",
                height=200,
                help=(
                    "Ecrivez ici la bibliographie du membre : parcours, style "
                    "d'accompagnement, experiences, domaines de specialite, etc. "
                    "Ce texte sera utilise plus tard par l'IA."
                ),
            )

            if st.button("Creer le membre", key="create_member_button"):
                if create_first_name.strip() or create_last_name.strip():
                    create_member(
                        first_name=create_first_name.strip(),
                        last_name=create_last_name.strip(),
                        email=create_email.strip() or None,
                        phone=create_phone.strip() or None,
                        role=create_role.strip() or None,
                        birthdate=create_birthdate.strip() or None,
                        bio=create_bio.strip() or None,
                    )
                    st.success("Membre cree avec succes.")
                    st.rerun()
                else:
                    st.error("Veuillez renseigner au moins un prenom ou un nom.")

        else:
            if not members:
                st.info("Aucun membre a modifier pour le moment.")
                selected_member = None
            else:
                edit_selected_id = st.selectbox(
                    "Selectionnez un membre a modifier / supprimer",
                    options=[m["id"] for m in members],
                    format_func=lambda mid: members_by_id[mid]["name"] or f"Membre #{mid}",
                    key="edit_member_select",
                )
                selected_member = (
                    get_team_member(edit_selected_id) or members_by_id[edit_selected_id]
                )

            if selected_member is not None:
                edit_first_name = st.text_input(
                    "Prenom",
                    value=selected_member.get("first_name") or "",
                    key=f"edit_member_first_name_{selected_member['id']}",
                )
                edit_last_name = st.text_input(
                    "Nom",
                    value=selected_member.get("last_name") or "",
                    key=f"edit_member_last_name_{selected_member['id']}",
                )
                edit_email = st.text_input(
                    "Email",
                    value=selected_member.get("email") or "",
                    key=f"edit_member_email_{selected_member['id']}",
                )
                edit_phone = st.text_input(
                    "Telephone",
                    value=selected_member.get("phone") or "",
                    key=f"edit_member_phone_{selected_member['id']}",
                )
                edit_role = st.text_input(
                    "Fonction dans ProMind7",
                    value=selected_member.get("role") or "",
                    key=f"edit_member_role_{selected_member['id']}",
                )
                edit_birthdate = st.text_input(
                    "Date de naissance (YYYY-MM-DD, optionnel)",
                    value=selected_member.get("birthdate") or "",
                    key=f"edit_member_birthdate_{selected_member['id']}",
                )
                edit_bio = st.text_area(
                    "Bibliographie / Profil detaille",
                    value=selected_member.get("bio") or "",
                    height=200,
                    key=f"edit_member_bio_{selected_member['id']}",
                )

                if st.button(
                    "Enregistrer les modifications",
                    key="edit_member_save_button",
                ):
                    update_member(
                        member_id=selected_member["id"],
                        first_name=edit_first_name.strip() or None,
                        last_name=edit_last_name.strip() or None,
                        email=edit_email.strip() or None,
                        phone=edit_phone.strip() or None,
                        role=edit_role.strip() or None,
                        birthdate=edit_birthdate.strip() or None,
                        bio=edit_bio.strip() or None,
                    )
                    st.success("Membre mis a jour avec succes.")
                    st.rerun()

                st.markdown("---")
                st.markdown("### Suppression du membre")

                confirm_delete = st.checkbox(
                    "Je confirme la suppression definitive de ce membre.",
                    key="edit_member_confirm_delete",
                )

                if st.button(
                    "Supprimer ce membre",
                    key="edit_member_delete_button",
                ):
                    if not confirm_delete:
                        st.warning(
                            "Veuillez cocher la case de confirmation avant de supprimer ce membre."
                        )
                    else:
                        try:
                            deleted = delete_member(selected_member["id"])
                        except ValueError as e:
                            st.error(str(e))
                        else:
                            if deleted:
                                st.success("Membre supprime avec succes.")
                                st.rerun()
                            else:
                                st.warning(
                                    "Impossible de supprimer ce membre : des taches lui sont encore assignees."
                                )

    with col_right:
        st.subheader("Apercu du dossier")

        if not members:
            st.info("Aucun membre a afficher pour le moment.")
        else:
            preview_member = None
            if (
                "edit_member_select" in st.session_state
                and st.session_state.get("edit_member_select")
            ):
                preview_member = members_by_id.get(
                    st.session_state.get("edit_member_select")
                )

            if preview_member is None:
                preview_member = members[0]

            full_name = (
                (preview_member.get("first_name") or "")
                + " "
                + (preview_member.get("last_name") or "")
            ).strip() or preview_member.get("name") or "Membre"

            st.markdown(f"### {full_name}")

            role_txt = preview_member.get("role") or ""
            email_txt = preview_member.get("email") or ""
            phone_txt = preview_member.get("phone") or ""
            birth_txt = preview_member.get("birthdate") or ""
            bio_preview = (
                preview_member.get("bio")
                or "Aucune bibliographie renseignee pour ce membre."
            )

            if role_txt:
                st.markdown(f"**Fonction :** {role_txt}")
            if email_txt:
                st.markdown(f"**Email :** {email_txt}")
            if phone_txt:
                st.markdown(f"**Telephone :** {phone_txt}")
            if birth_txt:
                st.markdown(f"**Date de naissance :** {birth_txt}")

            st.markdown("**Bibliographie**")
            st.write(bio_preview)


def _render_learners_profiles():
    filter_option = st.radio(
        "Filtrer les apprenants",
        ("Tous", "Avec parcours", "Sans parcours"),
        horizontal=True,
    )

    if filter_option == "Tous":
        learners = list_students()
    elif filter_option == "Avec parcours":
        learners = list_students_with_packs()
    else:  # "Sans parcours"
        learners = list_students_without_packs()

    if not learners:
        st.info("Aucun apprenant importe depuis Tutor LMS pour le moment.")
        return

    learners_by_id = {s["id"]: s for s in learners}

    search = st.text_input(
        "Rechercher un apprenant (nom ou email)",
        key="admin_learners_search",
    ).strip().lower()

    filtered_learners = [
        s
        for s in learners
        if (not search)
        or (search in (s.get("name") or "").lower())
        or (search in (s.get("email") or "").lower())
    ]

    if not filtered_learners:
        st.warning("Aucun apprenant ne correspond a cette recherche.")
        return

    selected_id = st.selectbox(
        "Selectionnez un apprenant",
        options=[s["id"] for s in filtered_learners],
        format_func=lambda sid: f'{learners_by_id[sid]["name"]} ({learners_by_id[sid]["email"] or "sans email"})',
        key="admin_learners_select",
    )

    student = svc_get_student(selected_id)
    if not student:
        st.error("Apprenant introuvable.")
        return
    learner_id = selected_id

    col_left, col_right = st.columns([2, 3])

    with col_left:
        st.subheader("Donnees importees (lecture seule)")
        st.markdown(f"**Nom (Tutor LMS) :** {student.get('name') or 'Inconnu'}")
        st.markdown(f"**Email (Tutor LMS) :** {student.get('email') or 'Non renseigne'}")
        st.markdown(f"**ID utilisateur Tutor :** {student.get('tutor_user_id') or 'N/A'}")

        st.markdown("---")
        st.subheader("Profil apprenant ProMind7 (editable)")

        phone = st.text_input(
            "Telephone de l'apprenant",
            value=student.get("phone") or "",
            key=f"admin_learners_phone_{learner_id}",
        )
        birthdate = st.text_input(
            "Date de naissance (YYYY-MM-DD, optionnel)",
            value=student.get("birthdate") or "",
            key=f"admin_learners_birthdate_{learner_id}",
        )
        school = st.text_input(
            "Ecole / Etablissement",
            value=student.get("school") or "",
            key=f"admin_learners_school_{learner_id}",
        )
        level = st.text_input(
            "Niveau / Classe",
            value=student.get("level") or "",
            key=f"admin_learners_level_{learner_id}",
        )
        parent_name = st.text_input(
            "Nom du parent / tuteur",
            value=student.get("parent_name") or "",
            key=f"admin_learners_parent_name_{learner_id}",
        )
        parent_phone = st.text_input(
            "Telephone du parent / tuteur",
            value=student.get("parent_phone") or "",
            key=f"admin_learners_parent_phone_{learner_id}",
        )
        parent_email = st.text_input(
            "Email du parent / tuteur",
            value=student.get("parent_email") or "",
            key=f"admin_learners_parent_email_{learner_id}",
        )

        profile = st.text_area(
            "Profil apprenant / contexte / objectifs",
            value=student.get("profile") or "",
            height=200,
            key=f"admin_learners_profile_{learner_id}",
            help=(
                "Decrivez ici la situation de l'apprenant, ses objectifs, "
                "ses difficultes, ses points forts… Ce texte pourra etre "
                "utilise plus tard par l'IA."
            ),
        )

        if st.button("Enregistrer le profil apprenant", key="admin_learners_save"):
            svc_update_learner_profile(
                student_id=student["id"],
                phone=phone.strip() or None,
                birthdate=birthdate.strip() or None,
                school=school.strip() or None,
                level=level.strip() or None,
                parent_name=parent_name.strip() or None,
                parent_phone=parent_phone.strip() or None,
                parent_email=parent_email.strip() or None,
                profile=profile.strip() or None,
            )
            st.success("Profil apprenant mis a jour.")
            st.rerun()

    with col_right:
        st.subheader("Inscriptions (Tutor LMS – lecture seule)")

        enrollments = svc_list_student_enrollments(student["id"])
        if not enrollments:
            st.info("Aucune inscription enregistree pour cet apprenant.")
        else:
            for e in enrollments:
                course_code = e.get("course_code")
                course_title = e.get("course_title") or "Cours sans titre"
                status = e.get("status") or "statut inconnu"
                enrolled_at = e.get("enrolled_at") or "date inconnue"

                full_title = course_title

                st.markdown(f"- **{full_title}** ({status}) – {enrolled_at}")
