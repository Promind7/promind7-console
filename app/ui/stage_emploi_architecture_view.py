# -*- coding: utf-8 -*-
"""
Vue « Architecture » du parcours Stage & emploi (schéma produit, par phases).

Données figées dans ce module (pas de lecture du fichier .md externe).
Raccourci **Script** : bouton par leçon « Ln — … » → ``st.session_state`` consommé
par l’onglet Script (voir ``stage_emploi_script_jump_session_key``).
"""
from __future__ import annotations

from pathlib import Path
from typing import TypedDict, cast, List

import streamlit as st

from services.stage_emploi_service import (
    is_architecture_lesson_line,
    list_lesson_docx_files,
    module_index_from_architecture_module_title,
    pick_module_bucket_from_files,
    pick_phase0_bucket_from_files,
    resolve_architecture_lesson_line_to_rel_posix,
    stage_emploi_script_jump_session_key,
)


class _LessonRow(TypedDict):
    type: str
    text: str


class _JalonRow(TypedDict):
    type: str
    text: str
    unit: str


class _TestLiveRow(TypedDict):
    type: str
    text: str
    unit: str


class _ModuleRow(TypedDict):
    type: str
    title: str
    unit: str
    lessons: list[str]


PhaseRow = _LessonRow | _JalonRow | _TestLiveRow | _ModuleRow


class PhaseSpec(TypedDict):
    title: str
    rows: list[PhaseRow]


# Une entrée par bloc d’affichage (live d’ouverture, phases, clôture)
STAGE_EMPLOI_ARCHITECTURE_PHASES: list[PhaseSpec] = [
    {
        "title": "Live d’ouverture — Parcours Stage & emploi",
        "rows": [
            {
                "type": "live",
                "text": "Live d’ouverture — Parcours Stage & emploi",
                "unit": "",
            },
            {
                "type": "lesson",
                "text": "Hors unités Tutor #1–#20 (§5.3) ; distinct des lives de phase et du live de clôture (#20).",
            },
        ],
    },
    {
        "title": "PHASE 0 — Initiation au parcours stage & emploi",
        "rows": [
            {"type": "lesson", "text": "L1 — Présentation du parcours stage & emploi"},
            {"type": "lesson", "text": "L2 — Les questions les plus fréquentes"},
            {"type": "lesson", "text": "L3 — L’orientation et le choix du domaine"},
            {"type": "lesson", "text": "L4 — La méthode proM7"},
            {"type": "lesson", "text": "L5 — L’objectif proM7"},
            {
                "type": "test",
                "text": "Test de connaissance — Phase 0 — Initiation au parcours stage & emploi",
                "unit": "",
            },
        ],
    },
    {
        "title": "PHASE 1 — LE CONTEXTE",
        "rows": [
            {"type": "jalon", "text": "« Le Contexte »", "unit": "#2"},
            {
                "type": "module",
                "title": "Module 0 — Les études et le mindset",
                "unit": "#3",
                "lessons": [
                    "L1 — Introduction au parcours stage et emploi",
                    "L2 — Les études et le choix de la spécialité",
                    "L3 — Les lacunes et la difficulté technique",
                    "L4 — La gestion du stress en tant qu’étudiant",
                    "L5 — La gestion du temps et la discipline",
                    "L6 — Le lien entre les études et le marché du travail",
                ],
            },
            {
                "type": "module",
                "title": "Module 1 — L’économie et le marché du travail",
                "unit": "#4",
                "lessons": [
                    "L7 — Le marché du travail",
                    "L8 — L’impact de l’économie sur le marché du travail",
                    "L9 — Le marché du travail international",
                    "L10 — Le marché du travail au Maroc",
                    "L11 — Les tendances du marché",
                    "L12 — Le diplôme et le marché du travail",
                    "L13 — Offre et demande d’emploi — comment fonctionne le marché",
                    "L14 — Les règles (souvent invisibles) du marché de l’emploi",
                    "L15 — Partir à l’étranger ou rester au Maroc",
                    "L16 — Le lien entre le marché du travail et les entreprises",
                    "Test — Module 1 — Phase 1 — Le Contexte",
                ],
            },
            {
                "type": "module",
                "title": "Module 2 — L’entreprise",
                "unit": "#5",
                "lessons": [
                    "L17 — Pourquoi les entreprises existent",
                    "L18 — Les différentes tailles d’entreprises",
                    "L19 — Le business model",
                    "L20 — Anatomie de l’entreprise — qui fait quoi",
                    "L21 — Le fonctionnement d’une entreprise",
                    "L22 — La finance d’une entreprise",
                    "L23 — Le code du travail",
                    "L24 — Le processus de recrutement vu de l’intérieur",
                    "L25 — Le rôle de la personnalité au sein de l’entreprise",
                    "Test — Module 2 — Phase 1 — Le Contexte",
                ],
            },
            {"type": "test", "text": "Test — Phase 1 — Le Contexte", "unit": "#6"},
            {"type": "live", "text": "Live — Phase 1 — Le Contexte", "unit": "#7"},
        ],
    },
    {
        "title": "PHASE 2 — LA PRÉPARATION",
        "rows": [
            {"type": "jalon", "text": "« La Préparation »", "unit": "#8"},
            {
                "type": "module",
                "title": "Module 3 — Les attentes comportementales",
                "unit": "#9",
                "lessons": [
                    "L1 — Changement de mindset",
                    "L2 — La projection dans l’avenir",
                    "L3 — Soft skills",
                    "L4 — Savoir écouter et progresser",
                    "L5 — Se situer dans l’organigramme — anticipation du métier",
                    "L6 — La gestion du stress",
                    "Test — Module 3 — Phase 2 — La Préparation",
                ],
            },
            {
                "type": "module",
                "title": "Module 4 — Comment trouver un stage",
                "unit": "#10",
                "lessons": [
                    "L7 — Les types de stages (découverte, technicien, PFE, etc.)",
                    "L8 — Le choix du stage (terrain, bureau, etc.)",
                    "L9 — Où faire mon stage (grande structure, sous-traitant, etc.)",
                    "L10 — Les attentes d’un tuteur de stage (technicien)",
                    "L11 — Comment marquer son stage (technicien)",
                    "L12 — Comment soutenir et vendre son stage (technicien)",
                    "L13 — Comment utiliser son stage pour trouver un travail (technicien)",
                    "L14 — Les attentes d’un tuteur de stage (PFE)",
                    "L15 — Comment marquer son stage (PFE)",
                    "L16 — Comment soutenir et vendre son stage (PFE)",
                    "L17 — Comment utiliser son stage pour trouver un travail (PFE)",
                    "Test — Module 4 — Phase 2 — La Préparation",
                ],
            },
            {
                "type": "module",
                "title": "Module 5 — Comment trouver un emploi",
                "unit": "#11",
                "lessons": [
                    "L18 — Préparation psychologique",
                    "L19 — Storytelling — valorisation de ce qu’on sait déjà faire",
                    "L20 — Canaux de recrutement",
                    "L21 — Analyser une offre d’emploi comme un pro",
                    "L22 — Partir à l’étranger ou rester au Maroc",
                    "L23 — Les types de contrat",
                    "L24 — Négociation de l’offre (CDD, CDI, intérim, etc.)",
                    "L25 — CV + entretien",
                    "Test — Module 5 — Phase 2 — La Préparation",
                ],
            },
            {"type": "test", "text": "Test — Phase 2 — La Préparation", "unit": "#12"},
            {"type": "live", "text": "Live — Phase 2 — La Préparation", "unit": "#13"},
        ],
    },
    {
        "title": "PHASE 3 — LANGUES ET OUTILS NUMÉRIQUES",
        "rows": [
            {
                "type": "jalon",
                "text": "« Les langues et les outils numériques »",
                "unit": "#14",
            },
            {
                "type": "module",
                "title": "Module 6 — Les outils numériques",
                "unit": "#15",
                "lessons": [
                    "L1 — Comprendre et utiliser les outils numériques",
                    "L2 — Combiner l’IA avec les outils classiques",
                    "L3 — L’intégration de l’IA dans l’apprentissage",
                    "L4 — La mesure de la performance — KPI",
                    "L5 — Le tableau de bord",
                    "Test — Module 6 — Phase 3 — Langues et outils numériques",
                ],
            },
            {
                "type": "module",
                "title": "Module 7 — Les langues",
                "unit": "#16",
                "lessons": [
                    "L6 — Pourquoi apprendre les langues",
                    "L7 — Les bases du français",
                    "L8 — Les bases de l’anglais",
                    "L9 — Le vocabulaire professionnel",
                    "L10 — Préparation de l’entretien en français",
                    "L11 — Préparation de l’entretien en anglais",
                    "L12 — La pratique et la simulation",
                    "Test — Module 7 — Phase 3 — Langues et outils numériques",
                ],
            },
            {
                "type": "test",
                "text": "Test — Phase 3 — Langues et outils numériques",
                "unit": "#17",
            },
            {
                "type": "live",
                "text": "Live — Phase 3 — Langues et outils numériques",
                "unit": "#18",
            },
        ],
    },
    {
        "title": "CLÔTURE PARCOURS",
        "rows": [
            {"type": "test", "text": "Test — Phase finale — Parcours Stage & emploi", "unit": "#19"},
            {"type": "live", "text": "Live — Phase finale — Parcours Stage & emploi", "unit": "#20"},
        ],
    },
]


def _render_arch_lesson_row_with_script_button(
    *,
    pack_root: Path,
    line: str,
    bucket: str | None,
    key_slug: str,
    button_uid: str,
) -> None:
    """Une ligne « Ln — … » + bouton pour cibler l’onglet Script."""
    if not bucket:
        st.markdown(f"- {line}")
        return
    rel = resolve_architecture_lesson_line_to_rel_posix(
        pack_root,
        architecture_line=line,
        bucket=bucket,
    )
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown(f"- {line}")
    with c2:
        if rel:
            if st.button(
                "Script",
                key=f"arch_op_{key_slug}_{button_uid}",
                help="Pré-sélectionne ce .docx dans l’onglet Script (puis ouvrez Script).",
                use_container_width=True,
            ):
                st.session_state[stage_emploi_script_jump_session_key(key_slug)] = rel
        else:
            st.caption("—")


def render_stage_emploi_architecture_tab(
    *,
    pack_root: Path | None = None,
    key_slug: str = "",
) -> None:
    """Onglet Streamlit : architecture par phases (modules en sous-expanders)."""
    st.subheader("Architecture")

    root = pack_root
    use_script_links = bool(key_slug) and root is not None and root.is_dir()
    files_cache: List[dict] = list_lesson_docx_files(root) if use_script_links else []
    phase0_bucket = (
        pick_phase0_bucket_from_files(files_cache) if files_cache else None
    )

    if use_script_links:
        st.caption(
            "Pour chaque leçon **L…** : **Script** enregistre le fichier cible ; "
            "passez à l’onglet **Script** pour voir l’aperçu."
        )

    for pi, phase in enumerate(STAGE_EMPLOI_ARCHITECTURE_PHASES):
        with st.expander(
            phase["title"],
            expanded=phase["title"].startswith("PHASE 0 —"),
        ):
            for ri, row in enumerate(phase["rows"]):
                t = row["type"]
                if t == "lesson":
                    lr0 = cast(_LessonRow, row)
                    text = lr0["text"]
                    if (
                        use_script_links
                        and phase["title"].startswith("PHASE 0 —")
                        and is_architecture_lesson_line(text)
                    ):
                        _render_arch_lesson_row_with_script_button(
                            pack_root=cast(Path, root),
                            line=text,
                            bucket=phase0_bucket,
                            key_slug=key_slug,
                            button_uid=f"{pi}_{ri}",
                        )
                    else:
                        st.markdown(f"- {text}")
                elif t == "jalon":
                    jr = cast(_JalonRow, row)
                    st.markdown(f"{jr['text']} `{jr['unit']}`")
                elif t == "module":
                    mr = cast(_ModuleRow, row)
                    mod_idx = module_index_from_architecture_module_title(mr["title"])
                    mod_bucket = (
                        pick_module_bucket_from_files(files_cache, mod_idx)
                        if use_script_links and mod_idx is not None
                        else None
                    )
                    with st.expander(f"📁 {mr['title']} `{mr['unit']}`", expanded=False):
                        for li, line in enumerate(mr["lessons"]):
                            if (
                                use_script_links
                                and mod_bucket
                                and is_architecture_lesson_line(line)
                            ):
                                _render_arch_lesson_row_with_script_button(
                                    pack_root=cast(Path, root),
                                    line=line,
                                    bucket=mod_bucket,
                                    key_slug=key_slug,
                                    button_uid=f"{pi}_{ri}_{li}",
                                )
                            else:
                                st.markdown(f"- {line}")
                elif t == "test":
                    tr = cast(_TestLiveRow, row)
                    u = (tr.get("unit") or "").strip()
                    suffix = f" `{u}`" if u else ""
                    # Le libellé complet est déjà dans ``text`` (ex. « Test — Phase 1 — … »).
                    st.markdown(f"{tr['text']}{suffix}")
                elif t == "live":
                    lr = cast(_TestLiveRow, row)
                    u = (lr.get("unit") or "").strip()
                    suffix = f" `{u}`" if u else ""
                    st.markdown(f"{lr['text']}{suffix}")
