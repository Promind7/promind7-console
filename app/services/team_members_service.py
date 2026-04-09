from typing import List, Dict, Optional

from db import (
    list_team_members as db_list_team_members,
    get_team_member as db_get_team_member,
    get_team_member_by_name as db_get_team_member_by_name,
    create_team_member as db_create_team_member,
    update_team_member as db_update_team_member,
    delete_team_member as db_delete_team_member,
    get_connection,
)


def list_team_members() -> List[Dict]:
    return db_list_team_members()


def get_team_member(member_id: int) -> Optional[Dict]:
    return db_get_team_member(member_id)


def get_team_member_by_name(name: str) -> Optional[Dict]:
    return db_get_team_member_by_name(name)


def create_member(
    first_name: str,
    last_name: str,
    email: Optional[str],
    phone: Optional[str],
    role: Optional[str],
    birthdate: Optional[str],
    bio: Optional[str],
) -> None:
    db_create_team_member(first_name, last_name, email, phone, role, birthdate, bio)


def update_member(
    member_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    role: Optional[str] = None,
    birthdate: Optional[str] = None,
    bio: Optional[str] = None,
) -> None:
    db_update_team_member(
        member_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        role=role,
        birthdate=birthdate,
        bio=bio,
    )


def delete_member(member_id: int) -> bool:
    """
    Deletes a team member using the existing DB logic.

    Returns:
        True  -> member deleted from team_members
        False -> member still has tasks assigned (no deletion)
    Raises:
        ValueError if member does not exist.
    """
    conn = get_connection()
    try:
        deleted = db_delete_team_member(member_id, conn)
    finally:
        conn.close()
    return deleted
