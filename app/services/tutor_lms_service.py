
"""
Service Tutor LMS.

Centralise l'import Tutor LMS (export ZIP) et l'acces lecture aux cours,
modules et lecons. Cette couche remplace les requetes SQL inline et le
parsing de meta_json dans l'UI.
"""

import json
from pathlib import Path

from db import get_db_path, get_connection
from services.admin_service import ensure_import_history_table, log_import_result
from import_tutor_from_zip import import_from_zip_folder
from services.catalog_sync_service import sync_internal_catalog_from_tutor
from services.content_service import sync_content_folders_from_db


def _compute_path_size(path: Path) -> int:
    """Retourne la taille d'un fichier ou d'un dossier (somme recursive)."""
    try:
        if path.is_file():
            return path.stat().st_size
        if path.is_dir():
            total = 0
            for item in path.rglob("*"):
                try:
                    if item.is_file():
                        total += item.stat().st_size
                except Exception:
                    # Ignore les fichiers inaccessibles pour ne pas bloquer
                    continue
            return total
    except Exception:
        return 0
    return 0


def _resolve_import_size(export_root: str, initial_size: int) -> int:
    """
    Renvoie la taille de l'import (dossier ou fichier). Si le calcul initial
    retourne 0, on retente avec un nouveau calcul puis on tombe en dernier
    recours sur la taille actuelle de la base SQLite pour eviter un 0 trompeur.
    """
    if initial_size > 0:
        return initial_size

    path = Path(export_root)
    retry_size = _compute_path_size(path)
    if retry_size > 0:
        return retry_size

    try:
        db_path = get_db_path()
        db_size = Path(db_path).stat().st_size
        return db_size
    except Exception:
        return 0


class ImportResult(tuple):
    """Tuple (nb_courses, nb_modules, nb_lessons) enrichi avec un resume et le status."""

    def __new__(cls, nb_courses, nb_modules, nb_lessons, status: str = "success"):
        obj = super().__new__(cls, (nb_courses, nb_modules, nb_lessons))
        obj.status = status
        obj.summary = {
            "status": status,
            "nb_courses": nb_courses,
            "nb_modules": nb_modules,
            "nb_lessons": nb_lessons,
        }
        return obj


def _safe_log_import_result(
    conn,
    zip_name: str,
    zip_size: int,
    nb_courses: int | None,
    nb_modules: int | None,
    nb_lessons: int | None,
    status: str,
    error_message: str | None,
):
    """
    Enregistre le resultat d'import dans import_history sans bloquer l'import
    principal si la journalisation rencontre une erreur.
    """
    local_conn = conn
    created_conn = False
    try:
        if local_conn is None:
            local_conn = get_connection()
            created_conn = True
        ensure_import_history_table(local_conn)
        log_import_result(
            local_conn,
            zip_name=zip_name,
            zip_size=zip_size,
            nb_courses=nb_courses,
            nb_modules=nb_modules,
            nb_lessons=nb_lessons,
            status=status,
            error_message=error_message,
        )
    except Exception:
        # On evite de bloquer l'import si la journalisation echoue
        pass
    finally:
        if created_conn and local_conn:
            local_conn.close()


def import_tutor_zip_folder(export_root: str, conn=None, *, log_result: bool = True):
    """
    Import Tutor LMS depuis un dossier ZIP décompressé,
    puis synchronisation du catalogue interne ProMind7 et
    création des dossiers de contenu.
    """
    zip_path = Path(export_root)
    courses_dir = zip_path / "courses"
    if not courses_dir.is_dir():
        raise FileNotFoundError(
            f"Dossier 'courses' introuvable dans {zip_path}. "
            "Placez l'export Tutor LMS décompressé dans le dossier source détecté "
            "(PROMIND7_TUTOR_LMS_ROOT, 04-tutorLMS ou tutor_lms) avec un sous-dossier courses/."
        )
    zip_name = zip_path.name
    zip_size = _compute_path_size(zip_path)

    nb_courses = None
    nb_modules = None
    nb_lessons = None
    status = "success"
    error_message = None

    try:
        # 1) Import brut Tutor LMS -> tables tutor_*
        nb_courses, nb_modules, nb_lessons = import_from_zip_folder(export_root)

        # 2) Synchronisation du catalogue interne (courses / parcours internes / modules / leçons)
        #    puis création des dossiers de contenu dans content/.
        try:
            sync_internal_catalog_from_tutor(conn=conn)
            sync_content_folders_from_db()
        except Exception as sync_err:
            # Cette étape ne doit pas empêcher de considérer l'import comme réussi.
            print(f"[TutorLMS] Warning: internal catalog sync failed: {sync_err}")

        return ImportResult(nb_courses, nb_modules, nb_lessons, status=status)

    except Exception as e:
        status = "error"
        error_message = str(e)
        raise
    finally:
        if log_result:
            zip_size_resolved = _resolve_import_size(export_root, zip_size)
            _safe_log_import_result(
                conn,
                zip_name=zip_name,
                zip_size=zip_size_resolved,
                nb_courses=nb_courses,
                nb_modules=nb_modules,
                nb_lessons=nb_lessons,
                status=status,
                error_message=error_message,
            )


def get_all_courses(conn=None):
    """
    Renvoie la liste des cours (parcours Tutor LMS) en base.

    Args:
        conn: connexion SQLite ouverte (optionnelle).
    """
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT tutor_id, title, status, created_at, updated_at,
                   categories_json, tags_json
            FROM tutor_courses
            ORDER BY title COLLATE NOCASE;
            """
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            cats = None
            tags = None
            try:
                if r["categories_json"]:
                    cats = json.loads(r["categories_json"])
                if r["tags_json"]:
                    tags = json.loads(r["tags_json"])
            except Exception:
                cats = None
                tags = None
            result.append(
                {
                    "tutor_id": r["tutor_id"],
                    "title": r["title"],
                    "status": r["status"],
                    "created_at": r["created_at"],
                    "updated_at": r["updated_at"],
                    "categories": cats,
                    "tags": tags,
                }
            )
        return result
    finally:
        if close_conn:
            conn.close()


def get_course_details(course_id: int, conn=None):
    """
    Renvoie le detail d'un cours Tutor LMS par tutor_id.

    Args:
        course_id: identifiant tutor_id.
        conn: connexion SQLite ouverte (optionnelle).
    """
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT tutor_id, title, status, created_at, updated_at,
                   categories_json, tags_json
            FROM tutor_courses
            WHERE tutor_id = ?
            LIMIT 1;
            """,
            (course_id,),
        )
        r = cur.fetchone()
        if not r:
            return None
        cats = None
        tags = None
        try:
            if r["categories_json"]:
                cats = json.loads(r["categories_json"])
            if r["tags_json"]:
                tags = json.loads(r["tags_json"])
        except Exception:
            cats = None
            tags = None
        return {
            "tutor_id": r["tutor_id"],
            "title": r["title"],
            "status": r["status"],
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
            "categories": cats,
            "tags": tags,
        }
    finally:
        if close_conn:
            conn.close()


def get_modules_for_course(course_id: int, conn=None):
    """
    Renvoie les modules d'un cours Tutor LMS.

    Args:
        course_id: identifiant tutor_id du cours.
        conn: connexion SQLite ouverte (optionnelle).
    """
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT tutor_id, title, status
            FROM tutor_modules
            WHERE course_tutor_id = ?
            ORDER BY order_index;
            """,
            (course_id,),
        )
        rows = cur.fetchall()
        return [
            {"tutor_id": r["tutor_id"], "title": r["title"], "status": r["status"]}
            for r in rows
        ]
    finally:
        if close_conn:
            conn.close()


def get_lessons_for_module(module_id: int, conn=None):
    """
    Renvoie les lecons d'un module, avec parsing de meta_json.

    Args:
        module_id: identifiant tutor_id du module.
        conn: connexion SQLite ouverte (optionnelle).
    """
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT tutor_id, title, status, meta_json
            FROM tutor_lessons
            WHERE module_tutor_id = ?
            ORDER BY order_index;
            """,
            (module_id,),
        )
        rows = cur.fetchall()
        lessons = []
        for r in rows:
            lesson_type = None
            duration = None
            try:
                if r["meta_json"]:
                    meta = json.loads(r["meta_json"])
                    lesson_type = meta.get("lesson_type") or meta.get("type")
                    duration = meta.get("duration") or meta.get("video_duration")
            except Exception:
                lesson_type = None
                duration = None
            lessons.append(
                {
                    "tutor_id": r["tutor_id"],
                    "title": r["title"],
                    "status": r["status"],
                    "lesson_type": lesson_type,
                    "duration": duration,
                }
            )
        return lessons
    finally:
        if close_conn:
            conn.close()
