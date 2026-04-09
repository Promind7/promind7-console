"""
Onglets « Rédaction & scripts » : libellés + chemins relatifs à ``Input/Script``.

Alignement : **Architecture plateforme Promind7** — **§4** (catalogue, ordre d’affichage).

- **Accueil plateforme** (hors plaquette, §1) : contenus **transverses** ; ce n’est pas le
  sous-dossier ``000-Initiation`` (phase 0) du parcours Stage & emploi.
- Puis les **parcours** dans l’ordre du catalogue : adhésion communauté → orientation lycéen
  → stage & emploi → évolution → expertise → mental & personnalité.
- **Stage & emploi** : dossier ``Parcours stage & emploi`` ; arborescence pédagogique / Tutor
  figée au **§5.2** du document d’architecture (phases, modules, leçons L…, tests, lives).

Le dossier disque ``Parcours abonnement`` reste le chemin scripts pour l’**Adhésion communauté
proM7** (libellé public §2 / §4).

Les dossiers peuvent être créés plus tard : l’UI affiche un message si le chemin est absent.
"""

from __future__ import annotations


def redaction_key_slug(rel_posix: str) -> str:
    """Fragment sûr pour les clés Streamlit (évite /, \\, &)."""
    return rel_posix.replace("/", "_").replace("\\", "_").replace("&", "_")[:96]


# (libellé public §4, chemin relatif sous Input/Script — hors Accueil)
REDACTION_SCRIPT_PARCOURS: list[tuple[str, str]] = [
    ("Accueil plateforme", "Accueil plateforme"),
    ("Adhésion communauté proM7", "Parcours abonnement"),
    ("Orientation lycéen", "Parcours orientation lycéens"),
    ("Stage & emploi", "Parcours stage & emploi"),
    ("Évolution professionnelle", "Parcours évolution professionnelle"),
    ("Expertise professionnelle", "Parcours expertise professionnelle"),
    ("Mental & personnalité", "Parcours mental et personnalité"),
]
