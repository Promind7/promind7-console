
import json
from typing import Set

from db.connection import get_connection

# =========================================================
# ============ IMPORT TUTOR LMS (tables tutor_*) ==========
# =========================================================
def upsert_tutor_course_from_export(course_obj: dict):
    """
    Insere / met a jour un cours Tutor LMS dans tutor_courses.
    Appelee avec l'objet 'course' complet depuis import_tutor_from_zip.py.
    """
    conn = get_connection()
    cur = conn.cursor()

    tutor_id = course_obj.get("ID")
    title = course_obj.get("post_title")
    status = course_obj.get("post_status")
    created_at = course_obj.get("post_date") or course_obj.get("post_date_gmt")
    updated_at = course_obj.get("post_modified") or course_obj.get("post_modified_gmt")

    categories_json = None
    tags_json = None

    terms = course_obj.get("terms") or {}
    cats = terms.get("course-category") or terms.get("category")
    tags = terms.get("course-tag") or terms.get("post_tag")
    if cats:
        categories_json = json.dumps(cats, ensure_ascii=False)
    if tags:
        tags_json = json.dumps(tags, ensure_ascii=False)

    raw_json = json.dumps(course_obj, ensure_ascii=False)

    cur.execute(
        """
        INSERT INTO tutor_courses (
            tutor_id, title, status, created_at, updated_at,
            categories_json, tags_json, raw_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(tutor_id) DO UPDATE SET
            title = excluded.title,
            status = excluded.status,
            created_at = excluded.created_at,
            updated_at = excluded.updated_at,
            categories_json = excluded.categories_json,
            tags_json = excluded.tags_json,
            raw_json = excluded.raw_json;
        """,
        (tutor_id, title, status, created_at, updated_at,
         categories_json, tags_json, raw_json),
    )

    conn.commit()
    conn.close()


def upsert_tutor_module_from_export(module_obj: dict, course_tutor_id: int):
    """Insere / met a jour un module Tutor LMS dans tutor_modules."""
    conn = get_connection()
    cur = conn.cursor()

    tutor_id = module_obj.get("ID")
    title = module_obj.get("post_title")
    status = module_obj.get("post_status")
    order_index = module_obj.get("menu_order")
    raw_json = json.dumps(module_obj, ensure_ascii=False)

    cur.execute(
        """
        INSERT INTO tutor_modules (
            tutor_id, course_tutor_id, title, status, order_index, raw_json
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(tutor_id) DO UPDATE SET
            course_tutor_id = excluded.course_tutor_id,
            title = excluded.title,
            status = excluded.status,
            order_index = excluded.order_index,
            raw_json = excluded.raw_json;
        """,
        (tutor_id, course_tutor_id, title, status, order_index, raw_json),
    )

    conn.commit()
    conn.close()


def upsert_tutor_lesson_from_export(
    lesson_obj: dict,
    course_tutor_id: int,
    module_tutor_id: int,
):
    """Insere / met a jour une lecon Tutor LMS dans tutor_lessons."""
    conn = get_connection()
    cur = conn.cursor()

    tutor_id = lesson_obj.get("ID")
    title = lesson_obj.get("post_title")
    status = lesson_obj.get("post_status")
    order_index = lesson_obj.get("menu_order")

    meta = lesson_obj.get("meta") or {}
    meta_json = json.dumps(meta, ensure_ascii=False)
    raw_json = json.dumps(lesson_obj, ensure_ascii=False)

    cur.execute(
        """
        INSERT INTO tutor_lessons (
            tutor_id, course_tutor_id, module_tutor_id,
            title, status, order_index, meta_json, raw_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(tutor_id) DO UPDATE SET
            course_tutor_id = excluded.course_tutor_id,
            module_tutor_id = excluded.module_tutor_id,
            title = excluded.title,
            status = excluded.status,
            order_index = excluded.order_index,
            meta_json = excluded.meta_json,
            raw_json = excluded.raw_json;
        """,
        (
            tutor_id,
            course_tutor_id,
            module_tutor_id,
            title,
            status,
            order_index,
            meta_json,
            raw_json,
        ),
    )

    conn.commit()
    conn.close()


def prune_tutor_mirror_to_imported_course_ids(kept_course_tutor_ids: Set[int]) -> dict:
    """
    Supprime les lignes ``tutor_*`` pour les cours qui ne sont plus présents dans
    l'export importé (dossiers sous ``courses/``).

    Sans effet si ``kept_course_tutor_ids`` est vide (aucun cours lu = pas de purge).
    Ordre : enrollments → lessons → modules → courses.
    """
    if not kept_course_tutor_ids:
        return {
            "skipped": True,
            "removed_courses": 0,
            "removed_modules": 0,
            "removed_lessons": 0,
            "removed_enrollments": 0,
        }

    conn = get_connection()
    cur = conn.cursor()
    placeholders = ",".join("?" * len(kept_course_tutor_ids))
    params = list(kept_course_tutor_ids)

    cur.execute(
        f"DELETE FROM tutor_enrollments WHERE course_tutor_id NOT IN ({placeholders})",
        params,
    )
    removed_enrollments = cur.rowcount

    cur.execute(
        f"DELETE FROM tutor_lessons WHERE course_tutor_id NOT IN ({placeholders})",
        params,
    )
    removed_lessons = cur.rowcount

    cur.execute(
        f"DELETE FROM tutor_modules WHERE course_tutor_id NOT IN ({placeholders})",
        params,
    )
    removed_modules = cur.rowcount

    cur.execute(
        f"DELETE FROM tutor_courses WHERE tutor_id NOT IN ({placeholders})",
        params,
    )
    removed_courses = cur.rowcount

    conn.commit()
    conn.close()

    return {
        "skipped": False,
        "removed_courses": removed_courses,
        "removed_modules": removed_modules,
        "removed_lessons": removed_lessons,
        "removed_enrollments": removed_enrollments,
    }


# =========================================================
# =========== LISTES / UTILITAIRES POUR LA CONSOLE ========
# =========================================================
def list_parcours_for_tasks(conn):
    """
    Parcours pour l’UI Tâches : source de vérité ``tutor_courses`` (après import LMS).

    Retourne une liste de dicts ``title``, ``pack_code``, ``tutor_id``.
    ``pack_code`` = ``courses.code`` si la synchro catalogue a tourné, sinon ``str(tutor_id)``
    pour que ``list_modules`` puisse résoudre le cours.
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT tc.tutor_id, tc.title, c.code AS course_code
        FROM tutor_courses tc
        LEFT JOIN courses c ON c.tutor_id = tc.tutor_id
        ORDER BY tc.title COLLATE NOCASE;
        """
    )
    rows = cur.fetchall()
    out = []
    for r in rows:
        tid = r["tutor_id"]
        title = r["title"] or f"Cours {tid}"
        code = r["course_code"]
        pack_code = code if code else str(tid)
        out.append({"title": title, "pack_code": pack_code, "tutor_id": tid})
    return out


def list_packs():
    """Liste les packs ProMind7 internes (table packs)."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT code, title, description
        FROM packs
        ORDER BY code ASC;
        """
    )

    rows = cur.fetchall()
    conn.close()

    return [
        {"code": r["code"], "title": r["title"], "description": r["description"]}
        for r in rows
    ]


def list_modules(pack_code):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT m.id, m.tutor_id, m.module_code, m.title, m.description
        FROM modules m
        JOIN courses c ON m.course_tutor_id = c.tutor_id
        WHERE c.code = ? OR CAST(c.tutor_id AS TEXT) = ?
        ORDER BY m.module_code ASC;
        """,
        (pack_code, pack_code),
    )

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "tutor_id": r["tutor_id"],
            "module_code": r["module_code"],
            "title": r["title"],
            "description": r["description"],
        }
        for r in rows
    ]


def list_lessons(module_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM lessons
        WHERE module_tutor_id = (
            SELECT tutor_id FROM modules WHERE id = ?
        )
        ORDER BY lesson_code ASC;
        """,
        (module_id,),
    )

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "tutor_id": r["tutor_id"],
            "lesson_code": r["lesson_code"],
            "title": r["title"],
            "content": r["content"],
        }
        for r in rows
    ]


def list_quizzes(lesson_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM quizzes
        WHERE lesson_tutor_id = (
            SELECT tutor_id FROM lessons WHERE id = ?
        )
        ORDER BY quiz_code ASC;
        """,
        (lesson_id,),
    )

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "tutor_id": r["tutor_id"],
            "quiz_code": r["quiz_code"],
            "title": r["title"],
        }
        for r in rows
    ]


def search_in_packs(keyword: str):
    """
    Utilisé par l'Agent IA pour chercher dans les packs internes (courses).
    """
    conn = get_connection()
    cur = conn.cursor()

    kw = f"%{keyword.lower()}%"

    cur.execute("""
        SELECT code, title, description
        FROM courses
        WHERE LOWER(code) LIKE ? 
           OR LOWER(title) LIKE ? 
           OR LOWER(description) LIKE ?;
    """, (kw, kw, kw))

    rows = cur.fetchall()
    conn.close()

    return [
        {"code": r["code"], "title": r["title"], "description": r["description"]}
        for r in rows
    ]


def get_lesson_hierarchy(lesson_tutor_id: int):
    """
    Récupère la hiérarchie complète (Course > Module > Lesson) pour un ID de leçon donné.
    Utile pour reconstruire le chemin du fichier.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            c.tutor_id as course_id, c.title as course_title,
            m.tutor_id as module_id, m.title as module_title,
            l.tutor_id as lesson_id, l.title as lesson_title
        FROM tutor_lessons l
        JOIN tutor_modules m ON l.module_tutor_id = m.tutor_id
        JOIN tutor_courses c ON l.course_tutor_id = c.tutor_id
        WHERE l.tutor_id = ?
    """, (lesson_tutor_id,))
    
    row = cur.fetchone()
    conn.close()
    
    if row:
        return {
            "course_tutor_id": row["course_id"],
            "course_title": row["course_title"],
            "module_tutor_id": row["module_id"],
            "module_title": row["module_title"],
            "lesson_tutor_id": row["lesson_id"],
            "lesson_title": row["lesson_title"]
        }
    return None
