"""
Service Taches.

Centralise la creation, la lecture, la mise a jour et la suppression
des taches ainsi que leurs liaisons (pack/module/lecon/quiz, assignee).
La logique etait dans promind7_console.py et db_promind7.py ; elle est
regroupee ici pour etre consommee par l'UI.
"""

from db import (
    add_task as db_add_task,
    list_tasks as db_list_tasks,
    update_task_status as db_update_task_status,
    update_task as db_update_task,
    delete_task as db_delete_task,
    get_connection,
)


def get_all_tasks(conn, include_done: bool = False):
    """
    Retourne la liste des taches avec details (module/lecon/quiz).

    Args:
        conn: connexion SQLite ouverte.
        include_done: inclure ou non les taches en statut done.
    """
    return db_list_tasks(include_done=include_done)


def get_tasks_by_member(member_id: int, conn):
    """
    Retourne les taches assignees a un membre donne (par son id).

    Args:
        member_id: identifiant du membre (table team_members).
        conn: connexion SQLite ouverte.

    Note:
        L'assignee est stocke sous forme de nom dans tasks.assignee.
        On recupere le nom a partir de l'id et on filtre.
    """
    cur = conn.cursor()
    cur.execute("SELECT name FROM team_members WHERE id = ?;", (member_id,))
    row = cur.fetchone()
    if not row:
        return []
    member_name = row["name"]

    cur.execute(
        """
        SELECT id, title, status, priority, pack_code
        FROM tasks
        WHERE assignee = ?
        ORDER BY status, priority DESC, created_at DESC;
        """,
        (member_name,),
    )
    rows = cur.fetchall()
    return [
        {
            "id": r["id"],
            "title": r["title"],
            "status": r["status"],
            "priority": r["priority"],
            "pack_code": r["pack_code"],
        }
        for r in rows
    ]


def add_task(data: dict, conn) -> int:
    """
    Cree une tache et renvoie son id.

    Args:
        data: dictionnaire contenant titre, description, priority,
              due_date, pack_code, module_id, lesson_id, quiz_id, assignee, status.
        conn: connexion SQLite ouverte.
    """
    # db_add_task ne retourne pas l'id, on l'obtient ensuite.
    db_add_task(
        title=data.get("title"),
        description=data.get("description"),
        priority=data.get("priority"),
        due_date=data.get("due_date"),
        pack_code=data.get("pack_code"),
        module_id=data.get("module_id"),
        lesson_id=data.get("lesson_id"),
        quiz_id=data.get("quiz_id"),
        assignee=data.get("assignee"),
    )
    cur = conn.cursor()
    cur.execute("SELECT MAX(id) AS max_id FROM tasks;")
    row = cur.fetchone()
    new_id = row["max_id"] if row else None

    # si statut specifie, on le met a jour
    status = data.get("status")
    if status and new_id is not None:
        db_update_task_status(new_id, status)
    return new_id


def update_task_status(task_id: int, status: str, conn) -> None:
    """
    Met a jour le statut d'une tache.

    Args:
        task_id: identifiant de la tache.
        status: nouveau statut (todo/in_progress/done).
        conn: connexion SQLite ouverte.
    """
    db_update_task_status(task_id, status)


def update_task(task_id: int, fields: dict, conn) -> None:
    """
    Met a jour des champs d'une tache.

    Args:
        task_id: identifiant de la tache.
        fields: dict pouvant contenir title, description, priority, assignee, pack_code.
        conn: connexion SQLite ouverte.
    """
    db_update_task(
        task_id=task_id,
        title=fields.get("title"),
        description=fields.get("description"),
        priority=fields.get("priority"),
        assignee=fields.get("assignee"),
        pack_code=fields.get("pack_code"),
    )


def delete_task(task_id: int, conn) -> None:
    """
    Supprime une tache.

    Args:
        task_id: identifiant de la tache.
        conn: connexion SQLite ouverte.
    """
    db_delete_task(task_id)

