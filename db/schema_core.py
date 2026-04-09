"""
Ebauche du schema de base de donnees ProMind7 (coeur metier).

Ce fichier ne migre rien automatiquement : il documente les structures
en place ou planifiees (learners, packs, enrollments, taches, etc.) et
fournit des templates SQL a utiliser plus tard. L'existant (db package)
reste la source unique pour init_db dans l'application actuelle.
"""


def create_learners_table_sql() -> str:
    """SQL de creation de la table learners (apprenants internes)."""
    return """
    CREATE TABLE IF NOT EXISTS learners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        username TEXT,
        language_level_id INTEGER,
        soft_skill_profile_id INTEGER,
        created_at TEXT,
        updated_at TEXT
    );
    """


def create_language_levels_table_sql() -> str:
    """SQL de creation de la table language_levels (ex: A1, B2...)."""
    return """
    CREATE TABLE IF NOT EXISTS language_levels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        label TEXT,
        description TEXT
    );
    """


def create_soft_skills_table_sql() -> str:
    """SQL de creation de la table soft_skills (profil soft skills)."""
    return """
    CREATE TABLE IF NOT EXISTS soft_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT
    );
    """


def create_packs_table_sql() -> str:
    """SQL de creation de la table packs (referentiel interne)."""
    return """
    CREATE TABLE IF NOT EXISTS packs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        title TEXT,
        description TEXT,
        tutor_course_id INTEGER,
        created_at TEXT,
        updated_at TEXT
    );
    """


def create_enrollments_table_sql() -> str:
    """SQL de creation de la table enrollments (liaison learners/packs)."""
    return """
    CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        learner_id INTEGER NOT NULL,
        pack_code TEXT NOT NULL,
        course_tutor_id INTEGER,
        enrolled_at TEXT,
        status TEXT,
        progress REAL,
        UNIQUE(learner_id, pack_code)
    );
    """


def create_tasks_table_sql() -> str:
    """
    SQL de creation de la table tasks, alignee sur la structure actuelle
    (id, title, description, status, priority, due_date, pack/module/lesson/quiz, assignee).
    """
    return """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'todo',
        priority TEXT DEFAULT 'normal',
        due_date TEXT,
        pack_code TEXT,
        module_id INTEGER,
        lesson_id INTEGER,
        quiz_id INTEGER,
        assignee TEXT
    );
    """


def create_team_members_table_sql() -> str:
    """SQL de creation de la table team_members (ref interne)."""
    return """
    CREATE TABLE IF NOT EXISTS team_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    """


def get_import_history_schema_sql() -> str:
    """Retourne la requete SQL de creation de la table import_history (journal des imports Tutor LMS)."""
    return """
    CREATE TABLE IF NOT EXISTS import_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imported_at TEXT,
        zip_name TEXT,
        zip_size INTEGER,
        nb_courses INTEGER,
        nb_modules INTEGER,
        nb_lessons INTEGER,
        status TEXT,
        error_message TEXT
    );
    """


def create_user_preferences_table_sql() -> str:
    """SQL pour stocker les preferences utilisateur generiques."""
    return """
    CREATE TABLE IF NOT EXISTS user_preferences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE,
        value TEXT
    );
    """


