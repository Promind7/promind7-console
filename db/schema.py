
from db.connection import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # === Schéma interne ProMind7 (packs / modules / leçons / quizz) ===
    cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tutor_id INTEGER,
            code TEXT,
            title TEXT,
            description TEXT,
            UNIQUE(tutor_id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tutor_id INTEGER,
            course_tutor_id INTEGER,
            module_code TEXT,
            title TEXT,
            description TEXT,
            UNIQUE(tutor_id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tutor_id INTEGER,
            module_tutor_id INTEGER,
            lesson_code TEXT,
            title TEXT,
            content TEXT,
            UNIQUE(tutor_id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tutor_id INTEGER,
            lesson_tutor_id INTEGER,
            quiz_code TEXT,
            title TEXT,
            UNIQUE(tutor_id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tutor_user_id INTEGER UNIQUE,
            name TEXT,
            email TEXT
        );
    """)

    # Extend students table with learner profile fields
    cur.execute("PRAGMA table_info(students);")
    student_cols = [row[1] for row in cur.fetchall()]

    def _ensure_student_column(col_name: str, col_type: str) -> None:
        if col_name not in student_cols:
            cur.execute(f"ALTER TABLE students ADD COLUMN {col_name} {col_type};")

    _ensure_student_column("phone", "TEXT")
    _ensure_student_column("birthdate", "TEXT")
    _ensure_student_column("school", "TEXT")
    _ensure_student_column("level", "TEXT")
    _ensure_student_column("parent_name", "TEXT")
    _ensure_student_column("parent_phone", "TEXT")
    _ensure_student_column("parent_email", "TEXT")
    _ensure_student_column("profile", "TEXT")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_tutor_id INTEGER,
            enrolled_at TEXT,
            status TEXT
        );
    """)

    # Tâches
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            priority TEXT,
            status TEXT DEFAULT 'todo',
            due_date TEXT,
            assignee TEXT,
            pack_code TEXT,
            module_id INTEGER,
            lesson_id INTEGER,
            quiz_id INTEGER,
            created_at TEXT
        );
    """)

    # Sessions (calendrier / rendez-vous)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            start_at TEXT NOT NULL,
            end_at TEXT NOT NULL,
            status TEXT NOT NULL,
            meet_url TEXT,
            google_event_id TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS session_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS session_learners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            learner_id INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );
    """)

    # Packs ProMind7 (codes P0, P1, etc.)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS packs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            title TEXT,
            description TEXT
        );
    """)

    # Miroir direct de l'export Tutor LMS (cours / modules / leçons / inscriptions)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tutor_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tutor_id INTEGER UNIQUE,
            title TEXT,
            status TEXT,
            created_at TEXT,
            updated_at TEXT,
            categories_json TEXT,
            tags_json TEXT,
            raw_json TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tutor_modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tutor_id INTEGER UNIQUE,
            course_tutor_id INTEGER,
            title TEXT,
            status TEXT,
            order_index INTEGER,
            raw_json TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tutor_lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tutor_id INTEGER UNIQUE,
            course_tutor_id INTEGER,
            module_tutor_id INTEGER,
            title TEXT,
            status TEXT,
            order_index INTEGER,
            meta_json TEXT,
            raw_json TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tutor_enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_tutor_id INTEGER,
            student_name TEXT,
            student_email TEXT,
            student_username TEXT,
            enrolled_at TEXT,
            status TEXT,
            raw_json TEXT
        );
    """)

    conn.commit()
    conn.close()
