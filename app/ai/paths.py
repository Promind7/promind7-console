"""Chemins projet pour la couche IA."""
from __future__ import annotations

import os
from pathlib import Path


def app_root() -> Path:
    """Dossier ``app/`` (contient ``ai/``, ``ui/``, ``tools/``, ``content/``, …)."""
    return Path(__file__).resolve().parent.parent


def project_root() -> Path:
    """Racine du projet console (``Input/``, ``app/``, ``db/``)."""
    return app_root().parent


def _tutor_export_has_courses(d: Path) -> bool:
    return (d / "courses").is_dir()


def tutor_lms_export_root_default() -> Path:
    """
    Dossier de référence pour l’export Tutor LMS décompressé (doit contenir ``courses/``).

    Ordre de résolution :
    1) variable d'environnement ``PROMIND7_TUTOR_LMS_ROOT`` ;
    2) ``<03-Streamlit>/04-tutorLMS`` si présent **et** contient ``courses/`` (dépôt local) ;
    3) ``<racine projet>/tutor_lms`` (copie versionnée pour le cloud — même contenu).
    """
    env = os.getenv("PROMIND7_TUTOR_LMS_ROOT", "").strip()
    if env:
        return Path(env)

    sibling_legacy = project_root().parent / "04-tutorLMS"
    bundled = project_root() / "tutor_lms"
    if sibling_legacy.is_dir() and _tutor_export_has_courses(sibling_legacy):
        return sibling_legacy
    if bundled.is_dir() and _tutor_export_has_courses(bundled):
        return bundled
    if sibling_legacy.is_dir():
        return sibling_legacy
    return bundled


def content_root() -> Path:
    return Path(os.getenv("PROMIND7_CONTENT_ROOT", app_root() / "content"))


def style_guide_path() -> Path:
    return content_root() / "style_guide.md"


def writer_overrides_path() -> Path:
    return content_root() / "writer_style_overrides.md"


def writer_editing_instructions_path() -> Path:
    """Consignes pour l’agent IA d’édition / révision (scripts V2, simplification, etc.)."""
    return content_root() / "writer_editing_instructions.md"


def writer_mba_agent_consignes_path() -> Path:
    """Brief pédagogique MBA-technicien, architecture parcours, corpus, sources."""
    return content_root() / "writer_mba_agent_consignes.md"


def redaction_drafts_dir() -> Path:
    d = content_root() / "redaction_drafts"
    d.mkdir(parents=True, exist_ok=True)
    return d
