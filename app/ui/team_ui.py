"""Composant UI pour l'onglet Team (lecture seule)."""

import streamlit as st


try:
    from services.team_members_service import list_team_members, get_team_member
    _USE_SERVICE = True
except ImportError:
    _USE_SERVICE = False
    from db import (
        list_team_members as db_list_team_members,
        get_team_member as db_get_team_member,
    )

from db import get_connection
from services.tasks_service import get_tasks_by_member


def _load_members():
    if _USE_SERVICE:
        return list_team_members()
    return db_list_team_members()


def _load_member(member_id: int):
    if _USE_SERVICE:
        return get_team_member(member_id)
    return db_get_team_member(member_id)


def render_team_tab():
    """Affiche l'onglet Team - lecture seule sur les profils."""
    st.title("Team - Profils membres ProMind7")

    members = _load_members()
    if not members:
        st.info("Aucun membre n'a encore été ajouté. Utilisez l'onglet Admin.")
        return

    # Tri par nom pour une sélection plus agréable
    sorted_members = sorted(
        members,
        key=lambda m: (m.get("name") or "").lower(),
    )

    label_to_member = {
        (m.get("name") or f"Membre #{m.get('id')}"): m for m in sorted_members
    }

    col_left, col_right = st.columns([1.4, 2])

    with col_left:
        st.subheader("Sélection des membres")

        selected_label = st.selectbox(
            "Sélectionner un membre :",
            list(label_to_member.keys()),
            key="team_member_select",
        )
        selected_member = label_to_member[selected_label]

        # Petit récap visuel
        st.markdown("---")
        st.markdown("**Résumé rapide**")

        role = selected_member.get("role") or ""
        email = selected_member.get("email") or ""
        phone = selected_member.get("phone") or ""

        if role:
            st.markdown(f"- Fonction : {role}")
        if email:
            st.markdown(f"- Email : {email}")
        if phone:
            st.markdown(f"- Téléphone : {phone}")

    with col_right:
        member_id = selected_member.get("id")
        full = _load_member(member_id) if member_id else selected_member

        st.subheader(f"Profil membre – {full.get('name') or selected_label}")

        fn = full.get("first_name") or ""
        ln = full.get("last_name") or ""
        identity = (fn + " " + ln).strip()

        if identity:
            st.markdown(f"**Identité complète :** {identity}")

        role = full.get("role") or ""
        email = full.get("email") or ""
        phone = full.get("phone") or ""
        birthdate = full.get("birthdate") or ""

        if role:
            st.markdown(f"**Fonction :** {role}")
        if email:
            st.markdown(f"**Email :** {email}")
        if phone:
            st.markdown(f"**Téléphone :** {phone}")
        if birthdate:
            st.markdown(f"**Date de naissance :** {birthdate}")

        bio = full.get("bio") or "Aucune bibliographie renseignée pour ce membre."
        st.markdown("**Bibliographie**")
        st.write(bio)

        # --- Affichage des tâches assignées ---
        st.markdown("---")
        st.subheader("Tâches assignées")
        
        # On a besoin d'une connexion pour récupérer les tâches
        conn = get_connection()
        try:
            tasks = get_tasks_by_member(full["id"], conn)
        finally:
            conn.close()

        if not tasks:
            st.info("Aucune tâche assignée pour le moment.")
        else:
            # On filtre les tâches 'done' si on veut, ou on les affiche différemment.
            # Ici on affiche tout avec un badge de statut.
            
            # Ordonner par priorité (High > Normal > Low) puis Statut
            prio_map = {"high": 3, "normal": 2, "low": 1, None: 0}
            tasks.sort(key=lambda t: prio_map.get(t.get("priority"), 0), reverse=True)

            for t in tasks:
                title = t.get("title") or "Tâche sans titre"
                status = t.get("status") or "todo"
                prio = t.get("priority") or "normal"
                pack_code = t.get("pack_code")
                
                # Couleurs et icones simples
                status_icon = "🟢" if status == "done" else ("🔵" if status == "in_progress" else "🔴")
                prio_str = f"[{prio.upper()}]" if prio == "high" else ""
                
                pack_info = f" *({pack_code})*" if pack_code else ""
                
                st.markdown(f"{status_icon} **{title}** {prio_str}{pack_info} – `{status}`")

# Onglet en lecture seule : création/édition dans Admin.
