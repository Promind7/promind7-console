"""
Service Admin.

Fonctions utilitaires pour l'administration : journal d'import Tutor LMS,
infos techniques sur la base et formatage de tailles.
"""

import os
from pathlib import Path

from services.content_service import (
    cleanup_orphan_content_folders,
    sync_content_folders_from_tutor,
)


def log_import_result(
    conn,
    zip_name: str,
    zip_size: int,
    nb_courses: int | None,
    nb_modules: int | None,
    nb_lessons: int | None,
    status: str,
    error_message: str | None = None,
) -> None:
    """
    Enregistre le resultat d'un import Tutor LMS dans import_history.
    """
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO import_history (
            imported_at, zip_name, zip_size, nb_courses, nb_modules, nb_lessons, status, error_message
        ) VALUES (datetime('now'), ?, ?, ?, ?, ?, ?, ?);
        """,
        (zip_name, zip_size, nb_courses, nb_modules, nb_lessons, status, error_message),
    )
    conn.commit()


def get_import_history(conn):
    """
    Retourne la liste des imports Tutor LMS, du plus recent au plus ancien.
    """
    ensure_import_history_table(conn)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, imported_at, zip_name, zip_size, nb_courses, nb_modules, nb_lessons, status, error_message
        FROM import_history
        ORDER BY imported_at DESC, id DESC;
        """
    )
    return cur.fetchall()


def get_database_size(db_path: str) -> int:
    """
    Retourne la taille du fichier SQLite en octets.
    """
    return Path(db_path).stat().st_size if os.path.exists(db_path) else 0


def format_db_size(size_bytes: int) -> str:
    """
    Formate une taille en octets en chaine lisible (KB, MB, GB).
    """
    units = ["octets", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    idx = 0
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024
        idx += 1
    if idx == 0:
        return f"{int(size)} {units[idx]}"
    return f"{size:.1f} {units[idx]}"


def ensure_import_history_table(conn) -> None:
    """
    Crée la table import_history si elle n'existe pas encore.
    """
    cur = conn.cursor()
    cur.execute(
        """
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
    )
    conn.commit()


def run_content_cleanup(dry_run: bool = False) -> dict:
    """
    Lance le nettoyage des dossiers de contenu orphelins
    (packs/modules/lessons sans correspondance DB).

    Retourne le dict de stats renvoyé par cleanup_orphan_content_folders.
    """
    return cleanup_orphan_content_folders(dry_run=dry_run)


def run_content_sync() -> None:
    """
    Lance la synchronisation de l'arborescence de contenu local
    à partir des tables tutor_*.
    """
    sync_content_folders_from_tutor()
