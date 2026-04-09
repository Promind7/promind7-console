"""
Ebauche du schema de donnees pour les fonctionnalites IA.

Documente les tables AI (profils generes, notes) sans executer de migration.
L'implementation actuelle n'utilise pas encore ces tables.
"""


def create_learner_profiles_ai_table_sql() -> str:
    """SQL pour stocker les profils IA generes pour chaque apprenant."""
    return """
    CREATE TABLE IF NOT EXISTS learner_profiles_ai (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        learner_id INTEGER NOT NULL,
        profile_json TEXT, -- stockage brut du profil IA
        model TEXT,
        created_at TEXT
    );
    """


def create_learner_notes_table_sql() -> str:
    """SQL pour stocker les notes/commentaires generes par l'IA."""
    return """
    CREATE TABLE IF NOT EXISTS learner_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        learner_id INTEGER NOT NULL,
        note TEXT,
        source TEXT, -- ex: 'agent', 'profiling'
        created_at TEXT
    );
    """


def create_ai_style_reference_table_sql() -> str:
    """SQL pour la table de references de style pour l'IA (Strategist)."""
    return """
    CREATE TABLE IF NOT EXISTS ai_style_reference (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE,
        value TEXT
    );
    """


