"""Chemins projet pour la couche IA."""
from __future__ import annotations

import os
from pathlib import Path


def app_root() -> Path:
    """Dossier ``app/`` (contient ``ai/``, ``ui/``, ``tools/``, ``content/``, …)."""
    return Path(__file__).resolve().parent.parent


def project_root() -> Path:
    """Racine du projet console (``Input/``, ``tutor_lms/``, ``app/``, ``db/``)."""
    return app_root().parent


def tutor_lms_export_root_default() -> Path:
    """
    Dossier projet pour l’export Tutor LMS décompressé (doit contenir ``courses/``).
    Convention : ``<racine projet>/tutor_lms``. Seule source de l'import Tutor dans
    la console Streamlit (Admin) ; pas de chemin personnalisable dans l'UI.
    """
    return project_root() / "tutor_lms"


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
