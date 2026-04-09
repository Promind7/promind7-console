
from datetime import datetime
import sqlite3
from db.connection import get_connection
import consts

def _get_placeholders(values):
    return ",".join(["?"] * len(values))

# ---------------------------------------------------------
# GESTION DES TÂCHES
# ---------------------------------------------------------
def add_task(title, description, priority, due_date, pack_code,
             module_id, lesson_id, quiz_id, assignee=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        INSERT INTO tasks (
            title, description, priority, status, due_date,
            assignee, pack_code, module_id, lesson_id, quiz_id, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        title, description, priority, consts.TASK_STATUS_TODO, due_date,
        assignee, pack_code, module_id, lesson_id, quiz_id,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def list_tasks(include_done: bool = False):
    """
    Retourne la liste des tâches.

    - include_done=False : uniquement les tâches non terminées (status != 'done')
    - include_done=True  : toutes les tâches
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = """
        SELECT
            t.id,
            t.title,
            t.description,
            t.priority,
            t.status,
            t.due_date,
            t.assignee,
            t.pack_code,
            t.module_id,
            t.lesson_id,
            t.quiz_id,
            t.created_at,

            -- pack_label : titre du pack si on le trouve, sinon code
            COALESCE(c.title, tc.title, t.pack_code) AS pack_label,

            m.title AS module_title,
            l.title AS lesson_title,
            q.title AS quiz_title
        FROM tasks t
        LEFT JOIN courses c
            ON c.code = t.pack_code
               OR CAST(c.tutor_id AS TEXT) = t.pack_code
        LEFT JOIN tutor_courses tc
            ON CAST(tc.tutor_id AS TEXT) = t.pack_code
        LEFT JOIN modules m
            ON t.module_id = m.id
        LEFT JOIN lessons l
            ON t.lesson_id = l.id
        LEFT JOIN quizzes q
            ON t.quiz_id = q.id
    """

    params: list = []

    if not include_done:
        query += " WHERE t.status != ?"
        params.append(consts.TASK_STATUS_DONE)

    query += " ORDER BY t.due_date IS NULL, t.due_date ASC, t.priority DESC;"

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "title": r["title"],
            "description": r["description"],
            "priority": r["priority"],
            "status": r["status"],
            "due_date": r["due_date"],
            "assignee": r["assignee"],
            "pack_label": r["pack_label"],
            "module_id": r["module_id"],
            "lesson_id": r["lesson_id"],
            "quiz_id": r["quiz_id"],
            "created_at": r["created_at"],
            "module_title": r["module_title"],
            "lesson_title": r["lesson_title"],
            "quiz_title": r["quiz_title"],
        }
        for r in rows
    ]


def list_task_stats_by_pack():
    """
    Statistiques de tâches par pack ProMind7.

    Retourne une liste de dicts :
    - pack_code
    - pack_title (titre du pack si trouvé, sinon code ou 'Sans pack')
    - total_tasks : nombre total de tâches liées à ce pack
    - open_tasks  : nombre de tâches non terminées (status != 'done')
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        f"""
        SELECT
            t.pack_code AS pack_code,
            COALESCE(p.title, t.pack_code, 'Sans pack') AS pack_title,
            COUNT(*) AS total_tasks,
            SUM(CASE WHEN t.status != ? THEN 1 ELSE 0 END) AS open_tasks
        FROM tasks t
        LEFT JOIN packs p
            ON p.code = t.pack_code
        GROUP BY t.pack_code, p.title
        ORDER BY p.code ASC, pack_title ASC;
        """,
        (consts.TASK_STATUS_DONE,)
    )

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "pack_code": r["pack_code"],
            "pack_title": r["pack_title"],
            "total_tasks": r["total_tasks"],
            "open_tasks": r["open_tasks"],
        }
        for r in rows
    ]


def update_task_status(task_id, new_status):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status = ?
        WHERE id = ?;
    """, (new_status, task_id))

    conn.commit()
    conn.close()


def update_task(task_id, title=None, description=None,
                priority=None, assignee=None, pack_code=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET
            title = COALESCE(?, title),
            description = COALESCE(?, description),
            priority = COALESCE(?, priority),
            assignee = COALESCE(?, assignee),
            pack_code = COALESCE(?, pack_code)
        WHERE id = ?;
    """, (title, description, priority, assignee, pack_code, task_id))

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))

    conn.commit()
    conn.close()


def resolve_pack_label(pack_code):
    """
    Retourne un libellé lisible pour un code de pack utilisé dans les tâches.

    Stratégie :
    1. Si pack_code correspond à un code interne de packs (table packs.code),
       on retourne packs.title.
    2. Sinon, si pack_code ressemble à un tutor_id (entier),
       on cherche dans tutor_courses / courses pour récupérer le titre.
    3. En dernier recours, on renvoie pack_code converti en str.
    """
    if not pack_code:
        return None

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 1) Essayer via la table packs (code interne : P0, P1, etc.)
    cur.execute(
        "SELECT title FROM packs WHERE code = ? LIMIT 1;",
        (pack_code,),
    )
    row = cur.fetchone()
    if row and row["title"]:
        conn.close()
        return row["title"]

    # 1b) Code interne cours (slug synchro Tutor → table courses)
    cur.execute(
        "SELECT title FROM courses WHERE code = ? LIMIT 1;",
        (pack_code,),
    )
    row = cur.fetchone()
    if row and row["title"]:
        conn.close()
        return row["title"]

    # 2) Essayer via tutor_id (si pack_code est numérique)
    tutor_id = None
    try:
        tutor_id = int(pack_code)
    except (TypeError, ValueError):
        tutor_id = None

    if tutor_id is not None:
        cur.execute(
            """
            SELECT
                COALESCE(c.title, tc.title) AS course_title
            FROM tutor_courses tc
            LEFT JOIN courses c
                ON c.tutor_id = tc.tutor_id
            WHERE tc.tutor_id = ?
            LIMIT 1;
            """,
            (tutor_id,),
        )
        row = cur.fetchone()
        conn.close()
        if row and row["course_title"]:
            return row["course_title"]

    # 3) Fallback : on renvoie le code brut
    conn.close()
    return str(pack_code)
