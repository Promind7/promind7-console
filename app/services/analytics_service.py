"""
Service Analytics.

Centralise les calculs de KPI et les aggregations utilises par le dashboard
(ProMind7). Aucune logique UI/Streamlit ici : chaque fonction retourne des
donnees brutes pretes a etre affichees.
"""


def get_global_kpis(conn) -> dict:
    """
    Calcule les KPI principaux (packs/modules/lecons/apprenants/taches).

    Args:
        conn: connexion SQLite ouverte (db.get_connection()).

    Returns:
        dict avec les cles nb_packs, nb_modules, nb_lessons, nb_learners, nb_tasks.
    """
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS c FROM tutor_courses;")
    nb_packs = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM tutor_modules;")
    nb_modules = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM tutor_lessons;")
    nb_lessons = cur.fetchone()["c"]

    cur.execute(
        """
        SELECT COUNT(DISTINCT
            COALESCE(student_email, student_username, student_name)
        ) AS c
        FROM tutor_enrollments
        WHERE COALESCE(student_email, student_username, student_name) IS NOT NULL;
        """
    )
    row = cur.fetchone()
    nb_learners = row["c"] if row else 0

    cur.execute("SELECT COUNT(*) AS c FROM tasks;")
    nb_tasks = cur.fetchone()["c"]

    return {
        "nb_packs": nb_packs,
        "nb_modules": nb_modules,
        "nb_lessons": nb_lessons,
        "nb_learners": nb_learners,
        "nb_tasks": nb_tasks,
    }


def get_tasks_by_status(conn):
    """
    Retourne les taches regroupees par statut.

    Args:
        conn: connexion SQLite ouverte.

    Returns:
        list[dict]: [{"status": str, "nb": int}, ...]
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT status, COUNT(*) AS nb
        FROM tasks
        GROUP BY status;
        """
    )
    rows = cur.fetchall()
    return [{"status": r["status"], "nb": r["nb"]} for r in rows] if rows else []


def get_tasks_by_priority(conn):
    """
    Retourne les taches regroupees par priorite.
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT priority, COUNT(*) AS nb
        FROM tasks
        GROUP BY priority;
        """
    )
    rows = cur.fetchall()
    return [
        {"priority": (r["priority"] or "normal"), "nb": r["nb"]}
        for r in rows
    ] if rows else []


def get_learners_by_pack(conn):
    """
    Compte les inscriptions par pack/cours Tutor LMS.

    Args:
        conn: connexion SQLite ouverte.

    Returns:
        list[dict]: [{"course_title": str, "course_tutor_id": int, "nb_inscriptions": int}, ...]
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            c.title AS course_title,
            e.course_tutor_id,
            COUNT(*) AS nb_inscriptions
        FROM tutor_enrollments e
        LEFT JOIN tutor_courses c
            ON c.tutor_id = e.course_tutor_id
        GROUP BY e.course_tutor_id
        ORDER BY nb_inscriptions DESC, course_title COLLATE NOCASE;
        """
    )
    rows = cur.fetchall()
    return [
        {
            "course_title": r["course_title"],
            "course_tutor_id": r["course_tutor_id"],
            "nb_inscriptions": r["nb_inscriptions"],
        }
        for r in rows
    ] if rows else []


def get_tasks_by_pack(conn):
    """
    Compte les taches par pack ProMind7 (pack_code ou titre si defini).

    Args:
        conn: connexion SQLite ouverte.

    Returns:
        list[dict]: [{"pack_label": str, "nb_taches": int}, ...]
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            COALESCE(p.title, t.pack_code, 'Non lie') AS pack_label,
            t.pack_code,
            COUNT(*) AS nb_taches
        FROM tasks t
        LEFT JOIN packs p
            ON p.code = t.pack_code
        GROUP BY pack_label, t.pack_code
        ORDER BY nb_taches DESC, pack_label COLLATE NOCASE;
        """
    )
    rows = cur.fetchall()
    return [
        {
            "pack_label": r["pack_label"] or (f"Pack {r['pack_code']}" if r["pack_code"] else "Non lie"),
            "nb_taches": r["nb_taches"],
        }
        for r in rows
    ] if rows else []

