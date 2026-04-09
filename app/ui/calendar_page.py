"""
UI Calendrier / Sessions.

Formulaire de creation / edition de session
et liste filtree des sessions.
Respecte la separation UI/Services (aucun acces DB direct).
"""

from __future__ import annotations

from datetime import date, datetime, time
import streamlit as st

from services import learners_service, session_service, team_members_service


FORM_PREFIX = "calendar_form_"
TITLE_KEY = f"{FORM_PREFIX}title"
DESCRIPTION_KEY = f"{FORM_PREFIX}description"
START_DATE_KEY = f"{FORM_PREFIX}start_date"
END_DATE_KEY = f"{FORM_PREFIX}end_date"
START_TIME_KEY = f"{FORM_PREFIX}start_time"
END_TIME_KEY = f"{FORM_PREFIX}end_time"
CREATE_GOOGLE_KEY = f"{FORM_PREFIX}create_google"
PACK_KEY = f"{FORM_PREFIX}pack"
MEMBERS_KEY = "calendar_members_selected"
LEARNERS_KEY = "calendar_learners_selected"
LOADED_SESSION_KEY = "calendar_form_loaded_session_id"
ALL_MEMBERS_LABEL = "[Tous les membres]"
ALL_LEARNERS_LABEL = "[Tous les apprenants]"


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------


def _init_form_state() -> None:
    defaults = {
        "calendar_edit_session_id": None,
        "calendar_edit_session_data": None,
        LOADED_SESSION_KEY: None,
        MEMBERS_KEY: [],
        LEARNERS_KEY: [],
        TITLE_KEY: "",
        DESCRIPTION_KEY: "",
        START_DATE_KEY: date.today(),
        END_DATE_KEY: date.today(),
        START_TIME_KEY: time(9, 0),
        END_TIME_KEY: time(10, 0),
        CREATE_GOOGLE_KEY: True,
        PACK_KEY: "(Aucun)",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def _purge_calendar_state_and_rerun() -> None:
    keys_to_delete = [
        key for key in list(st.session_state.keys()) if key.startswith("calendar_")
    ]
    for key in keys_to_delete:
        st.session_state.pop(key, None)
    st.rerun()


def _parse_iso_to_date_time(value: str):
    try:
        dt_value = datetime.fromisoformat(value)
        return dt_value.date(), dt_value.time()
    except Exception:  # noqa: BLE001
        return None, None


def _build_datetime_iso(selected_date: date, selected_time: time) -> str:
    if not selected_date or not selected_time:
        raise ValueError("Date et heure doivent etre renseignees.")
    combined = datetime.combine(selected_date, selected_time)
    return combined.isoformat()


def _is_google_calendar_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return "google calendar" in message or "googlecalendar" in message


def _prepare_edit_defaults(edit_data: dict | None, member_options: dict, learner_options: dict) -> None:
    if not edit_data:
        st.session_state[LOADED_SESSION_KEY] = None
        return

    if st.session_state.get(LOADED_SESSION_KEY) == edit_data.get("id"):
        return

    start_date_default, start_time_default = _parse_iso_to_date_time(edit_data.get("start_at", ""))
    end_date_default, end_time_default = _parse_iso_to_date_time(edit_data.get("end_at", ""))

    st.session_state[TITLE_KEY] = edit_data.get("title", "") or ""
    st.session_state[DESCRIPTION_KEY] = edit_data.get("description") or ""
    st.session_state[START_DATE_KEY] = start_date_default or date.today()
    st.session_state[END_DATE_KEY] = end_date_default or date.today()
    st.session_state[START_TIME_KEY] = start_time_default or time(9, 0)
    st.session_state[END_TIME_KEY] = end_time_default or time(10, 0)

    label_by_member_id = {v: k for k, v in member_options.items()}
    label_by_learner_id = {v: k for k, v in learner_options.items()}

    st.session_state[MEMBERS_KEY] = [
        label_by_member_id[mid]
        for mid in [m.get("id") for m in (edit_data.get("members") or [])]
        if mid in label_by_member_id
    ]
    st.session_state[LEARNERS_KEY] = [
        label_by_learner_id[lid]
        for lid in [l.get("id") for l in (edit_data.get("learners") or [])]
        if lid in label_by_learner_id
    ]
    st.session_state[LOADED_SESSION_KEY] = edit_data.get("id")


def _normalize_all_selection(selection_key: str, all_label: str, valid_labels: list[str]) -> None:
    selected = st.session_state.get(selection_key, [])
    if all_label in selected:
        st.session_state[selection_key] = list(valid_labels)
    else:
        st.session_state.setdefault(selection_key, [])


# ---------------------------------------------------------------------------
# Service helpers (Google fallback)
# ---------------------------------------------------------------------------


def _create_session_with_google_fallback(*, create_google_event: bool, **kwargs):
    if create_google_event:
        try:
            return session_service.create_session(create_google_event=True, **kwargs)
        except Exception as exc:
            if _is_google_calendar_error(exc):
                session = session_service.create_session(create_google_event=False, **kwargs)
                st.warning(
                    "Echec lors de la creation de l'evenement Google Calendar. La session a ete creee sans evenement Google."
                )
                return session
            raise
    return session_service.create_session(create_google_event=False, **kwargs)


def _update_session_with_google_fallback(*, with_google_event: bool, **kwargs) -> None:
    if with_google_event:
        try:
            session_service.update_session(with_google_event=True, **kwargs)
            return
        except Exception as exc:
            if _is_google_calendar_error(exc):
                session_service.update_session(with_google_event=False, **kwargs)
                st.warning(
                    "Echec de la mise a jour de l'evenement Google Calendar. La session a ete mise a jour sans evenement Google."
                )
                return
            raise
    session_service.update_session(with_google_event=False, **kwargs)


# ---------------------------------------------------------------------------
# Formulaire creation / edition
# ---------------------------------------------------------------------------


def _render_create_form() -> None:
    st.subheader("Creer / modifier une session")
    _init_form_state()

    members = team_members_service.list_team_members() or []
    learners = learners_service.list_students() or []
    packs = session_service.list_packs() or []

    member_options = {(m.get("name") or f"Membre {m['id']}"): m["id"] for m in members}
    learner_options = {(l.get("name") or f"Apprenant {l['id']}"): l["id"] for l in learners}

    pack_labels = ["(Aucun)"] + [p.get('name') or p.get('title') or f"Parcours {p['id']}" for p in packs]
    pack_label_to_id = {p.get('name') or p.get('title') or f"Parcours {p['id']}": p["id"] for p in packs}

    edit_data = st.session_state.get("calendar_edit_session_data")
    is_edit_mode = edit_data is not None

    if st.session_state[PACK_KEY] not in pack_labels:
        st.session_state[PACK_KEY] = "(Aucun)"

    _prepare_edit_defaults(edit_data, member_options, learner_options)

    member_labels = list(member_options.keys())
    learner_labels = list(learner_options.keys())
    all_members_label = f"[Tous les membres ({len(member_labels)})]"
    all_learners_label = f"[Tous les apprenants ({len(learner_labels)})]"
    _normalize_all_selection(MEMBERS_KEY, all_members_label, member_labels)
    _normalize_all_selection(LEARNERS_KEY, all_learners_label, learner_labels)

    with st.form(key="session_create_form"):
        st.text_input("Titre (optionnel)", key=TITLE_KEY)
        st.text_area("Description / notes internes", height=80, key=DESCRIPTION_KEY)

        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Date de debut", key=START_DATE_KEY)
            st.time_input("Heure de debut", key=START_TIME_KEY)
        with col2:
            st.date_input("Date de fin", key=END_DATE_KEY)
            st.time_input("Heure de fin", key=END_TIME_KEY)

        st.markdown("### Membres P7")
        st.multiselect(
            "Selection des membres",
            options=[all_members_label] + member_labels,
            key=MEMBERS_KEY,
        )
        raw_members = st.session_state.get(MEMBERS_KEY, []) or []
        all_members_selected = any(
            isinstance(m, str) and m.startswith("[Tous les memb") for m in raw_members
        )
        if all_members_selected:
            members_display = member_labels
            members_display_text = f"Tous les membres ({len(member_labels)}) seront inclus."
        else:
            members_display = [
                m for m in raw_members if isinstance(m, str) and not m.startswith("[Tous les memb")
            ]
            if members_display:
                members_display_text = "Membres inclus : " + ", ".join(members_display)
            else:
                members_display_text = "Membres inclus : aucun."
        st.caption(
            f"Selectionner « {all_members_label} » inclura tous les membres P7 ({len(member_labels)})."
        )

        st.markdown("### Apprenants")
        st.multiselect(
            "Selection des apprenants",
            options=[all_learners_label] + learner_labels,
            key=LEARNERS_KEY,
        )
        raw_learners = st.session_state.get(LEARNERS_KEY, []) or []
        all_learners_selected = any(
            isinstance(l, str) and l.startswith("[Tous les appren") for l in raw_learners
        )
        if all_learners_selected:
            learners_display = learner_labels
            learners_display_text = f"Tous les apprenants ({len(learner_labels)}) seront inclus."
        else:
            learners_display = [
                l for l in raw_learners if isinstance(l, str) and not l.startswith("[Tous les appren")
            ]
            if learners_display:
                learners_display_text = "Apprenants inclus : " + ", ".join(learners_display)
            else:
                learners_display_text = "Apprenants inclus : aucun."
        st.caption(
            f"Selectionner « {all_learners_label} » inclura tous les apprenants ({len(learner_labels)})."
        )

        st.selectbox("Parcours (optionnel)", options=pack_labels, key=PACK_KEY)
        st.caption(
            "Si vous choisissez un parcours et ne selectionnez aucun apprenant, tous les inscrits du parcours seront ajoutes automatiquement."
        )

        st.checkbox("Creer l'evenement Google Calendar (Meet auto)", key=CREATE_GOOGLE_KEY)

        if is_edit_mode:
            st.info(f"Vous modifiez la session #{edit_data['id']}")

        submitted = st.form_submit_button("Mettre a jour la session" if is_edit_mode else "Creer la session")

        if submitted:
            try:
                start_at = _build_datetime_iso(st.session_state[START_DATE_KEY], st.session_state[START_TIME_KEY])
                end_at = _build_datetime_iso(st.session_state[END_DATE_KEY], st.session_state[END_TIME_KEY])

                member_ids = [member_options[label] for label in members_display if label in member_options]
                learner_ids = [learner_options[label] for label in learners_display if label in learner_options]

                if is_edit_mode:
                    _update_session_with_google_fallback(
                        session_id=edit_data["id"],
                        title=st.session_state[TITLE_KEY] or "",
                        description=st.session_state[DESCRIPTION_KEY] or None,
                        start_at=start_at,
                        end_at=end_at,
                        member_ids=member_ids,
                        learner_ids=learner_ids,
                        with_google_event=st.session_state[CREATE_GOOGLE_KEY],
                        db=None,
                    )
                else:
                    _create_session_with_google_fallback(
                        title=st.session_state[TITLE_KEY] or None,
                        description=st.session_state[DESCRIPTION_KEY] or None,
                        start_at=start_at,
                        end_at=end_at,
                        member_ids=member_ids,
                        learner_ids=learner_ids,
                        create_google_event=st.session_state[CREATE_GOOGLE_KEY],
                        pack_id=pack_label_to_id.get(st.session_state[PACK_KEY])
                        if st.session_state[PACK_KEY] != "(Aucun)"
                        else None,
                    )

                _purge_calendar_state_and_rerun()
            except Exception as exc:  # noqa: BLE001
                st.error(f"Erreur lors de la creation / mise a jour de la session : {exc}")


# ---------------------------------------------------------------------------
# Liste des sessions
# ---------------------------------------------------------------------------


def _render_sessions_list() -> None:
    st.subheader("Sessions planifiees")

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:
        use_dates = st.checkbox("Filtrer par dates", value=False)
    if use_dates:
        with filter_col1:
            date_from = st.date_input("A partir du", key="sess_from")
        with filter_col2:
            date_to = st.date_input("Jusqu'au", key="sess_to")
    else:
        date_from = None
        date_to = None

    members = team_members_service.list_team_members() or []
    learners = learners_service.list_students() or []

    member_map = {m.get("name") or f"Membre {m['id']}": m["id"] for m in members}
    learner_map = {l.get("name") or f"Apprenant {l['id']}": l["id"] for l in learners}

    with filter_col3:
        member_label = st.selectbox(
            "Filtrer par membre",
            options=["(Tous)"] + list(member_map.keys()),
            key="sess_member",
        )
    with filter_col4:
        learner_label = st.selectbox(
            "Filtrer par apprenant",
            options=["(Tous)"] + list(learner_map.keys()),
            key="sess_learner",
        )

    status = st.selectbox(
        "Statut",
        options=["(Tous)", "planned", "completed", "cancelled"],
        key="sess_status",
    )

    filters = {
        "date_from": date_from.isoformat() if date_from else None,
        "date_to": date_to.isoformat() if date_to else None,
        "member_id": member_map.get(member_label) if member_label != "(Tous)" else None,
        "learner_id": learner_map.get(learner_label) if learner_label != "(Tous)" else None,
        "status": status if status != "(Tous)" else None,
    }

    sessions = session_service.list_sessions(
        date_from=filters["date_from"],
        date_to=filters["date_to"],
        member_id=filters["member_id"],
        learner_id=filters["learner_id"],
        status=filters["status"],
    )

    if not sessions:
        st.info("Aucune session trouvee.")
        return

    filtered_sessions = []
    for session in sessions:
        sess_status = session.get("status")
        if status == "(Tous)" and sess_status == "cancelled":
            continue
        if status not in ("(Tous)", None) and sess_status != status:
            continue
        filtered_sessions.append(session)

    if not filtered_sessions:
        st.info("Aucune session trouvee apres filtrage.")
        return

    for session in filtered_sessions:
        st.markdown("---")
        cols = st.columns([3, 2, 2, 1, 1])

        with cols[0]:
            st.markdown(f"### {session.get('title') or '(Sans titre)'}")
            st.caption(f"{session['start_at']} -> {session['end_at']}")

        with cols[1]:
            member_names = ", ".join([m.get("name") or "-" for m in session.get("members", [])])
            st.write(f"**Membres :** {member_names or '-'}")

        with cols[2]:
            learner_names = ", ".join([l.get("name") or "-" for l in session.get("learners", [])])
            st.write(f"**Apprenants :** {learner_names or '-'}")
            st.write(f"**Statut :** {session.get('status', '-')}")

        with cols[3]:
            if st.button("Modifier", key=f"edit_{session['id']}"):
                st.session_state["calendar_edit_session_id"] = session["id"]
                st.session_state["calendar_edit_session_data"] = session
                st.rerun()

        with cols[4]:
            if session.get("status") == "planned":
                if st.button("Annuler", key=f"cancel_{session['id']}"):
                    ok = session_service.cancel_session(
                        db=None,
                        session_id=session["id"],
                        cancel_google_event=True,
                    )
                    if ok:
                        st.rerun()
                    else:
                        st.error("Impossible d'annuler la session.")

        with st.expander(f"Details de la session #{session['id']}"):
            st.markdown(f"**Titre :** {session.get('title', '')}")
            if session.get("description"):
                st.markdown(f"**Description :** {session['description']}")
            st.markdown(f"**Debut :** {session.get('start_at', '')}")
            st.markdown(f"**Fin :** {session.get('end_at', '')}")
            st.markdown(f"**Statut :** {session.get('status', '')}")

            members_list = session.get("members", []) or []
            learners_list = session.get("learners", []) or []
            members_names = ", ".join(m.get("name", "") for m in members_list) or "-"
            learners_names = ", ".join(l.get("name", "") for l in learners_list) or "-"

            st.markdown(f"**Membres :** {members_names}")
            st.markdown(f"**Apprenants :** {learners_names}")

            meet_url = session.get("meet_url")
            if meet_url:
                st.markdown(f"**Lien Meet :** {meet_url}")
            else:
                st.markdown("**Lien Meet :** (aucun)")


# ---------------------------------------------------------------------------
# Entree principale
# ---------------------------------------------------------------------------


def render() -> None:
    _init_form_state()
    st.title("Calendrier / Sessions")

    _render_create_form()
    st.markdown("---")
    _render_sessions_list()
