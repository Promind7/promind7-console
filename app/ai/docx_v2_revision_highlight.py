"""
Colore les blocs du corps d’un document Word **nouvellement généré** (V2) par rapport à une baseline (V1),
mêmes couleurs que l’aperçu Streamlit : vert = ajouté, ambre = modifié.

Les scripts ``format_module*`` **n’invoquent plus** ce module par défaut (V2 = texte normal à l’ouverture Word).
Outil **optionnel** pour un diff couleur manuel ; à appeler **avant** ``apply_rtl_to_document`` si réintégré.
"""
from __future__ import annotations

from pathlib import Path

import docx
from docx.document import Document as DocumentObject
from docx.shared import RGBColor
from docx.table import Table
from docx.text.paragraph import Paragraph

from ai.docx_preview_html import compute_body_diff_marks_v1_vs_v2, _iter_block_items

_COLOR_ADD = RGBColor(0x1E, 0x7E, 0x34)
_COLOR_CHG = RGBColor(0x85, 0x64, 0x04)


def _apply_rgb_to_paragraph(paragraph: Paragraph, rgb: RGBColor) -> None:
    for run in paragraph.runs:
        if run.text:
            run.font.color.rgb = rgb


def _apply_rgb_to_table(table: Table, rgb: RGBColor) -> None:
    for row in table.rows:
        for cell in row.cells:
            for block in _iter_block_items(cell):
                if isinstance(block, Paragraph):
                    _apply_rgb_to_paragraph(block, rgb)
                elif isinstance(block, Table):
                    _apply_rgb_to_table(block, rgb)


def apply_v2_revision_font_colors(doc_new: DocumentObject, doc_v1: DocumentObject) -> None:
    """Colore les blocs du corps de ``doc_new`` (comparaison à ``doc_v1``)."""
    marks = compute_body_diff_marks_v1_vs_v2(doc_v1, doc_new)
    if not marks:
        return
    for j, block in enumerate(_iter_block_items(doc_new)):
        m = marks.get(j)
        if not m:
            continue
        rgb = _COLOR_ADD if m == "add" else _COLOR_CHG
        if isinstance(block, Paragraph):
            _apply_rgb_to_paragraph(block, rgb)
        elif isinstance(block, Table):
            _apply_rgb_to_table(block, rgb)


def apply_v2_revision_font_colors_vs_v1_path(doc_new: DocumentObject, path_v1: Path) -> None:
    """Charge V1 depuis le disque et applique ``apply_v2_revision_font_colors``."""
    if not path_v1.is_file():
        return
    try:
        doc_v1 = docx.Document(str(path_v1))
    except Exception:  # noqa: BLE001
        return
    apply_v2_revision_font_colors(doc_new, doc_v1)
