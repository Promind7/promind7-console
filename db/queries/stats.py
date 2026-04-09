
from db.connection import get_connection
import consts

def _get_placeholders(values):
    return ",".join(["?"] * len(values))

# =========================================================
# ====================   DASHBOARD   ======================
# =========================================================
def count_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tutor_courses")
    c = cur.fetchone()[0]
    conn.close()
    return c


def count_modules():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tutor_modules")
    c = cur.fetchone()[0]
    conn.close()
    return c


def count_lessons():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tutor_lessons")
    c = cur.fetchone()[0]
    conn.close()
    return c


def count_quizzes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM quizzes;")
    c = cur.fetchone()["c"]
    conn.close()
    return c


def count_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM students;")
    c = cur.fetchone()["c"]
    conn.close()
    return c


def count_active_learners():
    """
    Nombre d'apprenants ayant au moins une inscription active (non annulée)
    dans la table interne enrollments.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    placeholders = _get_placeholders(consts.ENROLLMENT_STATUS_CANCELLED_VALUES)
    params = list(consts.ENROLLMENT_STATUS_CANCELLED_VALUES)

    query = f"""
        SELECT COUNT(DISTINCT s.id) AS c
        FROM students s
        JOIN enrollments e
            ON e.student_id = s.id
        WHERE e.status IS NULL
           OR LOWER(TRIM(CAST(e.status AS TEXT))) NOT IN ({placeholders});
        """

    cur.execute(query, params)
    
    row = cur.fetchone()
    conn.close()
    return row["c"] if row and row["c"] is not None else 0


def count_total_tutor_enrollments():
    """
    Nombre total d'inscriptions Tutor LMS terminées (tutor_enrollments).
    """
    conn = get_connection()
    cur = conn.cursor()
    
    placeholders = _get_placeholders(consts.ENROLLMENT_STATUS_COMPLETED_VALUES)
    params = list(consts.ENROLLMENT_STATUS_COMPLETED_VALUES)

    query = f"""
        SELECT COUNT(*) AS c
        FROM tutor_enrollments
        WHERE
            status IS NOT NULL
            AND LOWER(status) IN ({placeholders});
        """

    cur.execute(query, params)
    
    row = cur.fetchone()
    conn.close()
    return row["c"] if row and row["c"] is not None else 0


def count_open_tasks():
    """
    Nombre de tâches non terminées.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM tasks WHERE status != ?;", (consts.TASK_STATUS_DONE,))
    row = cur.fetchone()
    conn.close()
    return row["c"] if row and row["c"] is not None else 0


def count_high_priority_open_tasks():
    """
    Nombre de tâches non terminées avec priorité 'haute' (ou équivalent).
    """
    conn = get_connection()
    cur = conn.cursor()
    
    placeholders = _get_placeholders(consts.TASK_PRIORITY_HIGH_VALUES)
    # Params: status, then priorities
    params = [consts.TASK_STATUS_DONE] + list(consts.TASK_PRIORITY_HIGH_VALUES)

    query = f"""
        SELECT COUNT(*) AS c
        FROM tasks
        WHERE status != ?
          AND LOWER(priority) IN ({placeholders})
        """
    
    cur.execute(query, params)
    
    row = cur.fetchone()
    conn.close()
    return row["c"] if row and row["c"] is not None else 0


def count_tasks(status=None):
    conn = get_connection()
    cur = conn.cursor()

    if status:
        cur.execute("SELECT COUNT(*) AS n FROM tasks WHERE status = ?;", (status,))
    else:
        cur.execute("SELECT COUNT(*) AS n FROM tasks;")

    n = cur.fetchone()["n"]
    conn.close()
    return n
