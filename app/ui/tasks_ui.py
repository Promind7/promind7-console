"""
Composant UI pour l'onglet Taches.

Toute la logique UI de l'onglet Tasks (creation, listing, edition,
suppression, vue par membre) est centralisee ici et consomme les services
tasks_service et team_service sans requetes SQL directes.
"""

from datetime import date

import streamlit as st
import pandas as pd


from db import (
    get_connection,
    list_modules,
    list_lessons,
    list_quizzes,
    resolve_pack_label,
)
from services.parcours_menu_order import sort_parcours_entries_by_menu_order
from ui.pm7_cache import cached_list_parcours_for_tasks, get_pm7_cache_version
from services.tasks_service import (
    add_task,
    delete_task,
    get_all_tasks,
    get_tasks_by_member,
    update_task,
    update_task_status,
)
from services.team_service import get_all_team_members


def _parcours_options_for_tasks_ui() -> tuple[dict[str, str], list[str]]:
    """Parcours issus de Tutor LMS (import), ordre menu = onglet Parcours."""
    rows = cached_list_parcours_for_tasks(get_pm7_cache_version())
    rows = sort_parcours_entries_by_menu_order(rows)
    pack_options = {r["title"]: r["pack_code"] for r in rows}
    pack_labels = [r["title"] for r in rows]
    return pack_options, pack_labels


def render_tasks_tab():
    """Affiche l'onglet Tasks et gere toutes les interactions UI."""
    st.title("Taches - Suivi ProMind7")

    conn = get_connection()
    try:
        tab_create, tab_list, tab_by_member, tab_by_parcours = st.tabs(
            [
                "Creer / modifier",
                "Liste des taches",
                "Taches par membre",
                "Taches par parcours",
            ]
        )

        with tab_create:
            _render_create_form(conn)

        with tab_list:
            _render_tasks_list(conn)

        with tab_by_member:
            _render_tasks_by_member(conn)

        with tab_by_parcours:
            _render_member_dossier(conn)
    finally:
        conn.close()


def _render_create_form(conn):
    """Formulaire de creation de tache."""
    st.subheader("Ajouter une tache")

    # Membres de l'equipe pour l'assignation
    team = get_all_team_members(conn)
    team_names = [m["name"] for m in team] if team else []

    # Source de vérité : tutor_courses (+ courses.code après import), pas la table packs (peut être obsolète)
    pack_options, pack_labels = _parcours_options_for_tasks_ui()

    with st.form("new_task_form"):
        title = st.text_input("Titre de la tache")
        desc = st.text_area("Description", height=80)

        col1, col2, col3 = st.columns(3)
        with col1:
            status = st.selectbox("Statut", ["todo", "in_progress", "done"], index=0)
        with col2:
            priority = st.selectbox("Priorite", ["low", "normal", "high"], index=1)
        with col3:
            due_date = st.date_input("Echeance (facultatif)", value=None)

        st.markdown("### Lier la tache a un element ProMind7 (facultatif)")
        col_p, col_m, col_l, col_q = st.columns(4)

        pack_code = None
        module_id = None
        lesson_id = None
        quiz_id = None

        pack_codes_all = list(pack_options.values()) if pack_options else []

        with col_p:
            if pack_labels:
                options_packs = ["Tous les parcours"] + pack_labels
                packs_selection = st.multiselect(
                    "Parcours concernes :",
                    options=options_packs,
                    key="task_packs",
                )
            else:
                packs_selection = []
                st.info("Aucun parcours disponible.")

        modules = list_modules(pack_code) if pack_code else []
        module_map = {
            f"{m['module_code']} - {m['title']}": m["id"] for m in modules
        } if modules else {}

        with col_m:
            if module_map:
                module_label = st.selectbox(
                    "Module",
                    options=["(aucun)"] + list(module_map.keys()),
                    key="task_module",
                )
                if module_label != "(aucun)":
                    module_id = module_map[module_label]
            else:
                st.write("")

        lessons = list_lessons(module_id) if module_id else []
        lesson_map = {
            f"{l['lesson_code']} - {l['title']}": l["id"] for l in lessons
        } if lessons else {}

        with col_l:
            if lesson_map:
                lesson_label = st.selectbox(
                    "Lecon",
                    options=["(aucun)"] + list(lesson_map.keys()),
                    key="task_lesson",
                )
                if lesson_label != "(aucun)":
                    lesson_id = lesson_map[lesson_label]
            else:
                st.write("")

        quizzes = list_quizzes(lesson_id) if lesson_id else []
        quiz_map = {
            f"{q['quiz_code']} - {q['title']}": q["id"] for q in quizzes
        } if quizzes else {}

        with col_q:
            if quiz_map:
                quiz_label = st.selectbox(
                    "Quizz",
                    options=["(aucun)"] + list(quiz_map.keys()),
                    key="task_quiz",
                )
                if quiz_label != "(aucun)":
                    quiz_id = quiz_map[quiz_label]
            else:
                st.write("")

        st.markdown(
            "### Assigner la tache a un ou plusieurs membres de l'equipe (facultatif)"
        )
        assignees_selection = []
        if team_names:
            options_assignees = ["Tous les membres"] + team_names
            assignees_selection = st.multiselect(
                "Assignee(s) :",
                options=options_assignees,
                key="task_assignees",
            )
        else:
            st.info(
                "Aucun membre dans l'equipe. Ajoute des membres dans l'onglet 'Team'."
            )

        submitted = st.form_submit_button("Creer la tache", type="primary")
        if submitted:
            if not title.strip():
                st.warning("Le titre de la tache est obligatoire.")
            else:
                base_data = {
                    "title": title.strip(),
                    "description": desc.strip(),
                    "priority": priority,
                    "due_date": due_date.isoformat()
                    if isinstance(due_date, date)
                    else None,
                    "module_id": module_id,
                    "lesson_id": lesson_id,
                    "quiz_id": quiz_id,
                    "status": status,
                }

                # Construire les cibles packs
                if packs_selection:
                    if "Tous les parcours" in packs_selection:
                        target_pack_codes = (
                            pack_codes_all[:] if pack_codes_all else [None]
                        )
                    else:
                        target_pack_codes = [
                            pack_options[label]
                            for label in packs_selection
                            if label in pack_options
                        ]
                else:
                    target_pack_codes = [None]

                # Construire les cibles assignees
                if assignees_selection:
                    if "Tous les membres" in assignees_selection:
                        target_assignees = team_names[:] if team_names else [None]
                    else:
                        target_assignees = assignees_selection[:]
                else:
                    target_assignees = [None]

                for pack_code in target_pack_codes:
                    for assignee in target_assignees:
                        data = {
                            **base_data,
                            "pack_code": pack_code,
                            "assignee": assignee,
                        }
                        add_task(data=data, conn=conn)

                st.success("Tache(s) creee(s).")
                st.rerun()


def _render_tasks_list(conn):
    """Affiche la liste des taches avec edition/suppression."""
    st.subheader("Liste des taches")

    show_done = st.checkbox(
        "Afficher aussi les taches terminees (done)", value=False
    )
    tasks = get_all_tasks(conn, include_done=show_done)

    if not tasks:
        st.info("Aucune tache pour le moment.")
        return

    # Trier les taches par id croissant pour avoir un ordre stable
    tasks_sorted = sorted(tasks, key=lambda t: t.get("id", 0))

    status_options = ["todo", "in_progress", "done"]

    # En-tete du "tableau"
    header_cols = st.columns([0.8, 3.0, 2.0, 1.8, 3.0, 1.2, 1.2])
    header_cols[0].markdown("**N°**")
    header_cols[1].markdown("**Tache**")
    header_cols[2].markdown("**Responsable**")
    header_cols[3].markdown("**Statut**")
    header_cols[4].markdown("**Parcours**")
    header_cols[5].markdown("**Suppr.**")
    header_cols[6].markdown("**Selection**")

    # Filtres alignes sous l'en-tete
    assignees = sorted({(t.get("assignee") or "").strip() for t in tasks_sorted})
    pack_labels = sorted(
        {
            (t.get("pack_label") or t.get("pack_code") or "").strip()
            for t in tasks_sorted
            if (t.get("pack_label") or t.get("pack_code"))
        }
    )

    filter_cols = st.columns([0.8, 3.0, 2.0, 1.8, 3.0, 1.2, 1.2])
    filter_cols[0].markdown("")
    title_filter = filter_cols[1].text_input(
        "Filtrer par tache",
        value="",
        key="task_title_filter",
        label_visibility="collapsed",
        placeholder="Filtrer par tache",
    )
    assignee_options = ["(Tous)"]
    if "" in assignees:
        assignee_options.append("(Non assigne)")
    assignee_options += [a for a in assignees if a]
    assignee_filter = filter_cols[2].selectbox(
        "Responsable",
        assignee_options,
        key="task_assignee_filter",
        label_visibility="collapsed",
    )
    status_filter_options = ["(Tous)"] + status_options
    status_filter = filter_cols[3].selectbox(
        "Statut",
        status_filter_options,
        key="task_status_filter",
        label_visibility="collapsed",
    )
    pack_options = ["(Tous)"] + pack_labels
    pack_filter = filter_cols[4].selectbox(
        "Parcours",
        pack_options,
        key="task_pack_filter",
        label_visibility="collapsed",
    )
    filter_cols[5].markdown("")
    filter_cols[6].markdown("")

    def _match_filters(task):
        title_match = True
        if title_filter and title_filter.strip():
            title_match = title_filter.strip().lower() in (
                task.get("title") or ""
            ).lower()

        assignee_val = (task.get("assignee") or "").strip()
        if assignee_filter == "(Tous)":
            assignee_match = True
        elif assignee_filter == "(Non assigne)":
            assignee_match = assignee_val == ""
        else:
            assignee_match = assignee_val == assignee_filter

        status_val = (task.get("status") or "").strip()
        if status_filter == "(Tous)":
            status_match = True
        else:
            status_match = status_val == status_filter

        pack_val = (task.get("pack_label") or task.get("pack_code") or "").strip()
        pack_match = pack_filter == "(Tous)" or pack_val == pack_filter

        return title_match and assignee_match and status_match and pack_match

    display_tasks = [t for t in tasks_sorted if _match_filters(t)]

    if not display_tasks:
        st.info("Aucune tache ne correspond aux filtres.")

    for idx, t in enumerate(display_tasks, start=1):
        assignee = t.get("assignee") or ""
        pack_label = t.get("pack_label") or t.get("pack_code") or ""
        current_status = t.get("status") or "todo"
        if current_status not in status_options:
            current_status = "todo"
        task_id = t.get("id")
        task_number = task_id if task_id is not None else idx

        row_cols = st.columns([0.8, 3.0, 2.0, 1.8, 3.0, 1.2, 1.2])
        row_cols[0].markdown(str(task_number))
        row_cols[1].markdown(t["title"])
        row_cols[2].markdown(assignee)

        # Selectbox pour changer le statut
        status_select_key = f"task_status_{t['id']}"
        status_choice = row_cols[3].selectbox(
            "",
            status_options,
            index=status_options.index(current_status),
            key=status_select_key,
            label_visibility="collapsed",
        )

        # Si le choix de l'utilisateur differe du statut actuel en base, on met a jour
        if status_choice != current_status:
            update_task_status(task_id=t["id"], status=status_choice, conn=conn)

        row_cols[4].markdown(pack_label)

        # Bouton de suppression individuel
        if task_id is not None:
            if row_cols[5].button("Suppr.", key=f"delete_task_{task_id}"):
                delete_task(task_id=task_id, conn=conn)
                st.success("Tache supprimee.")
                st.rerun()
        else:
            row_cols[5].markdown("-")

        # Checkbox pour la selection multiple
        select_key = f"select_task_{t['id']}"
        row_cols[6].checkbox("", key=select_key, value=False)

    # Suppression groupee des taches selectionnees
    selected_ids = [
        t["id"]
        for t in tasks_sorted
        if st.session_state.get(f"select_task_{t['id']}", False)
        and t.get("id") is not None
    ]
    if selected_ids:
        if st.button(
            f"Supprimer les {len(selected_ids)} tache(s) selectionnee(s)",
            type="secondary",
            key="delete_selected_tasks",
        ):
            for task_id in selected_ids:
                delete_task(task_id=task_id, conn=conn)
            st.success("Taches selectionnees supprimees.")
            st.rerun()

    st.markdown("### Modifier ou supprimer une tache")

    # On se base sur la liste triee
    tasks_sorted = sorted(tasks, key=lambda t: t.get("id", 0))

    # Construire les options du selectbox (ex: "1. Titre (Responsable)")
    options = {}
    for idx, t in enumerate(tasks_sorted, start=1):
        assignee_label = t.get("assignee") or "non assignee"
        task_number = t.get("id") if t.get("id") is not None else idx
        label = f"{task_number}. {t['title']} ({assignee_label})"
        options[label] = t

    selected_label = st.selectbox(
        "Selectionnez une tache a modifier ou supprimer :",
        options=list(options.keys()),
        key="task_edit_select",
    )

    selected_task = options[selected_label]
    task_id = selected_task["id"]

    # Recuperer la liste des membres pour l'assignee
    team = get_all_team_members(conn)
    team_names = [m["name"] for m in team] if team else []
    assignee_options = ["(non assigne)"] + team_names

    current_assignee = selected_task.get("assignee") or None
    if current_assignee and current_assignee in team_names:
        assignee_index = assignee_options.index(current_assignee)
    else:
        assignee_index = 0

    current_status = selected_task.get("status") or "todo"
    status_options = ["todo", "in_progress", "done"]
    if current_status not in status_options:
        current_status = "todo"

    rows = cached_list_parcours_for_tasks(get_pm7_cache_version())
    rows = sort_parcours_entries_by_menu_order(rows)
    pack_option_pairs = [(r["title"], r["pack_code"]) for r in rows]
    if not pack_option_pairs:
        observed_packs = set()
        for t in tasks_sorted:
            raw_label = t.get("pack_label") or t.get("pack_code")
            if raw_label:
                observed_packs.add(raw_label)
        for lbl in sorted(observed_packs):
            pack_option_pairs.append((lbl, lbl))

    pack_select_options = ["(aucun)"] + [label for label, _ in pack_option_pairs]
    current_pack_raw = (
        selected_task.get("pack_code") or selected_task.get("pack_label") or None
    )
    if current_pack_raw and current_pack_raw in pack_select_options:
        pack_index = pack_select_options.index(current_pack_raw)
    elif current_pack_raw:
        matched_idx = None
        for idx_opt, (label, code) in enumerate(
            pack_option_pairs, start=1
        ):  # +1 pour "(aucun)"
            if code == current_pack_raw:
                matched_idx = idx_opt
                break
        pack_index = matched_idx if matched_idx is not None else 0
    else:
        pack_index = 0

    with st.form("edit_task_form"):
        new_title = st.text_input(
            "Titre de la tache",
            value=selected_task["title"],
            key=f"edit_task_title_{task_id}",
        )
        new_desc = st.text_area(
            "Description",
            value=selected_task.get("description") or "",
            height=80,
            key=f"edit_task_desc_{task_id}",
        )
        new_priority = st.selectbox(
            "Priorite",
            ["low", "normal", "high"],
            index=["low", "normal", "high"].index(
                selected_task.get("priority") or "normal"
            ),
            key=f"edit_task_priority_{task_id}",
        )
        new_status = st.selectbox(
            "Statut",
            status_options,
            index=status_options.index(current_status),
            key=f"edit_task_status_{task_id}",
        )
        new_pack_label = st.selectbox(
            "Parcours",
            pack_select_options,
            index=pack_index,
            key=f"edit_task_pack_{task_id}",
        )
        new_assignee_choice = st.selectbox(
            "Assignee",
            assignee_options,
            index=assignee_index,
            key=f"edit_task_assignee_{task_id}",
        )
        col_update, col_delete = st.columns(2)
        with col_update:
            do_update = st.form_submit_button("Mettre a jour", type="primary")
        with col_delete:
            do_delete = st.form_submit_button("Supprimer", type="secondary")

    if do_update:
        fields = {
            "title": new_title.strip(),
            "description": new_desc.strip(),
            "priority": new_priority,
            "assignee": None
            if new_assignee_choice == "(non assigne)"
            else new_assignee_choice,
            "pack_code": None
            if new_pack_label == "(aucun)"
            else dict(pack_option_pairs).get(new_pack_label, new_pack_label),
        }
        update_task(task_id=selected_task["id"], fields=fields, conn=conn)
        update_task_status(task_id=selected_task["id"], status=new_status, conn=conn)
        st.success("Tache mise a jour.")
        st.rerun()

    if do_delete:
        delete_task(task_id=selected_task["id"], conn=conn)
        st.success("Tache supprimee.")
        st.rerun()


def _render_tasks_by_member(conn):
    """Affiche les taches par membre."""
    st.subheader("Taches par membre de l'equipe")

    team = get_all_team_members(conn)
    if not team:
        st.info("Aucun membre dans l'equipe. Ajoute des membres dans l'onglet 'Team'.")
        return

    member_options = {m["name"]: m["id"] for m in team}
    selected_member_name = st.selectbox(
        "Choisir un membre de l'equipe :",
        list(member_options.keys()),
        key="tasks_by_member",
    )
    selected_member_id = member_options[selected_member_name]

    show_done = st.checkbox(
        "Afficher aussi les taches terminees (done)",
        value=False,
        key="tasks_by_member_show_done",
    )
    filtered = get_tasks_by_member(selected_member_id, conn)
    if not show_done:
        filtered = [
            t for t in filtered if (t.get("status") or "").lower() != "done"
        ]
    if not filtered:
        st.info(f"Aucune tache assignee a {selected_member_name}.")
    else:
        for t in filtered:
            raw_pack = t.get("pack_label") or t.get("pack_code")
            pack_display = resolve_pack_label(raw_pack) if raw_pack else "-"
            task_id = t.get("id")
            task_id_display = task_id if task_id is not None else "?"

            st.markdown(
                f"- #{task_id_display} – **{t['title']}** "
                f"({t['status']}, prio={t['priority'] or 'normal'}, "
                f"parcours={pack_display})"
            )


def _render_member_dossier(conn):
    """Affiche les taches par parcours ProMind7."""
    st.subheader("Taches par parcours")
    show_done = st.checkbox(
        "Afficher aussi les taches terminees (done)",
        value=False,
        key="tasks_by_pack_show_done",
    )
    tasks = get_all_tasks(conn, include_done=show_done)
    if not tasks:
        st.info("Aucune tache pour le moment.")
        return

    # Construire la liste des parcours a partir des taches existantes
    pack_labels = []
    for t in tasks:
        label = t.get("pack_label") or t.get("pack_code")
        if label:
            pack_labels.append(label)

    pack_labels = sorted(set(pack_labels))

    if not pack_labels:
        st.info("Aucune tache n'est liee a un parcours pour le moment.")
        return

    selected_pack = st.selectbox(
        "Choisissez un parcours",
        options=pack_labels,
        key="tasks_by_pack_select",
    )

    # Filtrer les taches du parcours selectionne
    pack_tasks = [
        t
        for t in tasks
        if (t.get("pack_label") or t.get("pack_code")) == selected_pack
    ]

    if not pack_tasks:
        st.info("Aucune tache pour ce parcours.")
        return

    st.markdown(f"### Taches pour le parcours : {selected_pack}")

    # Affichage simple des taches du parcours
    rows = [
        {
            "N°": t.get("id") or "",
            "Tache": t["title"],
            "Responsable": t.get("assignee") or "",
            "Statut": t.get("status") or "",
            "Echeance": t.get("due_date") or "",
        }
        for t in pack_tasks
    ]

    if rows:
        df_rows = pd.DataFrame(rows)
        st.dataframe(
            df_rows,
            use_container_width=True,
            hide_index=True,
            height=min(40 * (len(df_rows) + 1), 320),
        )
    else:
        st.info("Aucune tache a afficher pour ce parcours.")
