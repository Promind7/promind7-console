"""
Onglet « Rédaction & scripts » : onglets par parcours sous Input/Script.

Ordre et libellés : **Architecture plateforme Promind7** (§4 catalogue, §1 Accueil hors plaquette).
"""
from __future__ import annotations

import streamlit as st

from services.stage_emploi_service import (
    consulting_stage_emploi_scripts_dir,
    get_pack_root,
    get_script_library_root,
)
from ui.parcours_redaction_tabs import REDACTION_SCRIPT_PARCOURS, redaction_key_slug
from ui.stage_emploi_ui import render_script_browser_at_path, render_stage_emploi_redaction_section


def render_redaction_tab() -> None:
    st.subheader("Rédaction & scripts")
    st.caption(
        "Référence produit : **Architecture plateforme Promind7** — onglets dans l’ordre du **§4** "
        "(après **Accueil plateforme**, hors plaquette §1). "
        "Lecture des scripts Word (canonique ou jumeau `-V2` ; l’interface masque `-V2` et `-darija` dans les titres) "
        "et téléchargement `.docx`. "
        "**Stage & emploi** : structure par phases dans l’onglet **Architecture** ; dossier "
        "`Parcours stage & emploi` (dont `000-Initiation` — phase 0, L1–L5). "
        "Sommaire structuré : à refaire plus tard."
    )

    lib_root = get_script_library_root()
    if not lib_root.is_dir():
        st.warning(
            f"La bibliothèque de scripts est introuvable : `{lib_root}`. "
            "Vérifiez `Input/Script/` ou la variable `PROMIND7_SCRIPT_LIBRARY_ROOT`."
        )
        return

    tab_labels = [label for label, _ in REDACTION_SCRIPT_PARCOURS]
    sub = st.tabs(tab_labels)
    _STAGE_EMPLOI_FOLDER = "Parcours stage & emploi"
    for i, (label, rel_posix) in enumerate(REDACTION_SCRIPT_PARCOURS):
        with sub[i]:
            if rel_posix == _STAGE_EMPLOI_FOLDER:
                root = get_pack_root(_STAGE_EMPLOI_FOLDER)
                render_stage_emploi_redaction_section(
                    root,
                    display_name=label,
                    key_slug=redaction_key_slug(rel_posix),
                    missing_folder_hint=(
                        f"Emplacement attendu par défaut si le dossier existe : "
                        f"`{consulting_stage_emploi_scripts_dir()}`. Sinon : "
                        f"`Input/Script/{rel_posix}` ou variable `PROMIND7_STAGE_EMPLOI_SCRIPT_ROOT`."
                    ),
                )
            else:
                root = (lib_root / rel_posix.replace("\\", "/")).resolve()
                render_script_browser_at_path(
                    root,
                    display_name=label,
                    key_slug=redaction_key_slug(rel_posix),
                )
