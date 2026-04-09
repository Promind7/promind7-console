"""
Service Team.

Gere les membres de l'equipe ProMind7. Aujourd'hui, l'ajout et la lecture
des membres se font via des requetes directes dans promind7_console.py
et la table est initialise dans ensure_team_schema(). Cette couche
abstraira ces operations.
"""


def list_members(conn):
    """Retourne la liste des membres de l'equipe."""
    return get_all_team_members(conn)


def add_member(conn, name: str):
    """Ajoute un membre (insert or ignore)."""
    # Compat: delegue vers add_team_member en ignorant l'argument role.
    return add_team_member(name=name, role=None, conn=conn)


def get_all_team_members(conn):
    """
    Retourne la liste des membres de l'equipe ProMind7.

    Args:
        conn: connexion SQLite ouverte.

    Returns:
        list[dict]: membres avec id et name.
    """
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM team_members ORDER BY name COLLATE NOCASE;")
    rows = cur.fetchall()
    return [{"id": r["id"], "name": r["name"]} for r in rows]


def add_team_member(name: str, role: str, conn):
    """
    Ajoute un membre (INSERT OR IGNORE) dans team_members.

    Args:
        name: nom du membre.
        role: role du membre (non persiste pour l'instant, schema actuel sans colonne role).
        conn: connexion SQLite ouverte.
    """
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO team_members (name) VALUES (?);",
        (name.strip(),),
    )
    conn.commit()


def supprimer_membre_team(member_id: int, conn=None):
    """
    Supprime un membre de l'equipe s'il n'a pas de taches assignees.

    Args:
        member_id: identifiant du membre dans team_members.
        conn: connexion SQLite ouverte (optionnel). Si None, une connexion est ouverte/fermee ici.

    Returns:
        bool: True si la suppression a ete effectuee, False si des taches existent.

    Exceptions:
        ValueError: si le membre est introuvable.
    """
    from db import delete_team_member, get_connection

    owns_conn = False
    if conn is None:
        conn = get_connection()
        owns_conn = True

    try:
        return delete_team_member(member_id, conn)
    finally:
        if owns_conn:
            conn.close()

