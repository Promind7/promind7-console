
import sqlite3
from db.connection import get_connection

# ---------------------------------------------------------
# GESTION DES MEMBRES (team_members)
# ---------------------------------------------------------
def list_team_members():
    """
    Returns all team members with profile fields.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            id,
            name,
            first_name,
            last_name,
            email,
            phone,
            role,
            birthdate,
            bio
        FROM team_members
        ORDER BY name ASC;
        """
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r["id"],
            "name": r["name"],
            "first_name": r["first_name"],
            "last_name": r["last_name"],
            "email": r["email"],
            "phone": r["phone"],
            "role": r["role"],
            "birthdate": r["birthdate"],
            "bio": r["bio"],
        }
        for r in rows
    ]


def get_team_member(member_id: int):
    """
    Returns a team member by id.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            id,
            name,
            first_name,
            last_name,
            email,
            phone,
            role,
            birthdate,
            bio
        FROM team_members
        WHERE id = ?;
        """,
        (member_id,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row["id"],
        "name": row["name"],
        "first_name": row["first_name"],
        "last_name": row["last_name"],
        "email": row["email"],
        "phone": row["phone"],
        "role": row["role"],
        "birthdate": row["birthdate"],
        "bio": row["bio"],
    }


def get_team_member_by_name(name: str):
    """
    Returns a single team member by name, including bio.
    Used by the Tasks UI when we only know the assignee name from tasks.assignee.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            id,
            name,
            first_name,
            last_name,
            email,
            phone,
            role,
            birthdate,
            bio
        FROM team_members
        WHERE name = ?;
        """,
        (name,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row["id"],
        "name": row["name"],
        "first_name": row["first_name"] if "first_name" in row.keys() else None,
        "last_name": row["last_name"] if "last_name" in row.keys() else None,
        "email": row["email"] if "email" in row.keys() else None,
        "phone": row["phone"] if "phone" in row.keys() else None,
        "role": row["role"] if "role" in row.keys() else None,
        "birthdate": row["birthdate"] if "birthdate" in row.keys() else None,
        "bio": row["bio"],
    }


def update_team_member_bio(member_id: int, bio: str):
    """
    Updates the bio of a team member.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE team_members
        SET bio = ?
        WHERE id = ?;
        """,
        (bio, member_id),
    )
    conn.commit()
    conn.close()


def create_team_member(
    first_name: str,
    last_name: str,
    email: str | None,
    phone: str | None,
    role: str | None,
    birthdate: str | None,
    bio: str | None,
):
    """
    Creates a new team member.
    'name' is stored as "first_name last_name".
    """
    full_name = ((first_name or "").strip() + " " + (last_name or "").strip()).strip()
    if not full_name:
        full_name = None

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO team_members (
            name, first_name, last_name, email, phone, role, birthdate, bio
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (full_name, first_name, last_name, email, phone, role, birthdate, bio),
    )
    conn.commit()
    conn.close()


def update_team_member(
    member_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    role: str | None = None,
    birthdate: str | None = None,
    bio: str | None = None,
):
    """
    Updates an existing team member.
    Keeps 'name' in sync with first_name + last_name if they change.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT first_name, last_name
        FROM team_members
        WHERE id = ?;
        """,
        (member_id,),
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return

    current_first = row["first_name"]
    current_last = row["last_name"]

    new_first = first_name if first_name is not None else current_first
    new_last = last_name if last_name is not None else current_last
    full_name = ((new_first or "").strip() + " " + (new_last or "").strip()).strip()
    if not full_name:
        full_name = None

    cur.execute(
        """
        UPDATE team_members
        SET
            name = COALESCE(?, name),
            first_name = COALESCE(?, first_name),
            last_name = COALESCE(?, last_name),
            email = COALESCE(?, email),
            phone = COALESCE(?, phone),
            role = COALESCE(?, role),
            birthdate = COALESCE(?, birthdate),
            bio = COALESCE(?, bio)
        WHERE id = ?;
        """,
        (
            full_name,
            first_name,
            last_name,
            email,
            phone,
            role,
            birthdate,
            bio,
            member_id,
        ),
    )
    conn.commit()
    conn.close()


def delete_team_member(member_id: int, conn):
    """
    Supprime un membre de l'equipe s'il n'a aucune tache assignee.

    Args:
        member_id: identifiant du membre dans team_members.
        conn: connexion SQLite ouverte (non fermee par cette fonction).

    Returns:
        bool: True si le membre a ete supprime, False s'il possede encore des taches.

    Raises:
        ValueError: si le membre n'existe pas.
    """
    cur = conn.cursor()

    cur.execute("SELECT name FROM team_members WHERE id = ?;", (member_id,))
    row = cur.fetchone()
    if not row:
        raise ValueError("Membre introuvable.")

    member_name = row["name"] if isinstance(row, sqlite3.Row) else row[0]

    cur.execute("SELECT COUNT(*) AS c FROM tasks WHERE assignee = ?;", (member_name,))
    count_row = cur.fetchone()
    count = count_row["c"] if count_row else 0
    if count > 0:
        return False

    cur.execute("DELETE FROM team_members WHERE id = ?;", (member_id,))
    conn.commit()
    return True
