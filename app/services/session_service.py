"""
Service Sessions / Calendrier.

Gere la creation, la liste, la consultation et l'annulation des sessions,
en orchestrant la base et l'integration Google Calendar.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from db.connection import get_connection
from integrations import google_calendar_client
from services.log_service import log_error, log_info


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def _fetch_members(conn, member_ids: List[int]) -> List[Dict]:
    if not member_ids:
        return []
    placeholders = ",".join(["?"] * len(member_ids))
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT id, name, email
        FROM team_members
        WHERE id IN ({placeholders});
        """,
        member_ids,
    )
    rows = cur.fetchall()
    return [
        {"id": r["id"], "name": r["name"], "email": r["email"]} for r in rows
    ]


def _fetch_learners(conn, learner_ids: List[int]) -> List[Dict]:
    if not learner_ids:
        return []
    placeholders = ",".join(["?"] * len(learner_ids))
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT id, name, email
        FROM students
        WHERE id IN ({placeholders});
        """,
        learner_ids,
    )
    rows = cur.fetchall()
    return [
        {"id": r["id"], "name": r["name"], "email": r["email"]} for r in rows
    ]


def _attach_participants(conn, session_ids: List[int]) -> Dict[int, Dict[str, list]]:
    """
    Charge les participants pour une liste de sessions.
    Retourne un dict {session_id: {"members": [...], "learners": [...]}}.
    """
    if not session_ids:
        return {}

    placeholders = ",".join(["?"] * len(session_ids))
    cur = conn.cursor()

    # Membres
    cur.execute(
        f"""
        SELECT sm.session_id, tm.id AS member_id, tm.name, tm.email
        FROM session_members sm
        JOIN team_members tm ON tm.id = sm.member_id
        WHERE sm.session_id IN ({placeholders});
        """,
        session_ids,
    )
    members_map: Dict[int, List[Dict]] = {}
    for row in cur.fetchall():
        sid = row["session_id"]
        members_map.setdefault(sid, []).append(
            {
                "id": row["member_id"],
                "name": row["name"],
                "email": row["email"],
            }
        )

    # Apprenants
    cur.execute(
        f"""
        SELECT sl.session_id, s.id AS learner_id, s.name, s.email
        FROM session_learners sl
        JOIN students s ON s.id = sl.learner_id
        WHERE sl.session_id IN ({placeholders});
        """,
        session_ids,
    )
    learners_map: Dict[int, List[Dict]] = {}
    for row in cur.fetchall():
        sid = row["session_id"]
        learners_map.setdefault(sid, []).append(
            {
                "id": row["learner_id"],
                "name": row["name"],
                "email": row["email"],
            }
        )

    result: Dict[int, Dict[str, list]] = {}
    for sid in session_ids:
        result[sid] = {
            "members": members_map.get(sid, []),
            "learners": learners_map.get(sid, []),
        }
    return result


def list_packs(db=None) -> List[Dict]:
    """
    Retourne les packs disponibles (tutor_courses en priorite, sinon table packs).
    """
    conn = db or get_connection()
    owns_conn = db is None
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT tutor_id AS id, COALESCE(title, CAST(tutor_id AS TEXT)) AS name
            FROM tutor_courses
            ORDER BY title COLLATE NOCASE;
            """
        )
        rows = cur.fetchall()
        if rows:
            return [{"id": r["id"], "name": r["name"]} for r in rows]

        cur.execute(
            """
            SELECT id AS id, COALESCE(title, code) AS name
            FROM packs
            ORDER BY name COLLATE NOCASE;
            """
        )
        rows = cur.fetchall()
        return [{"id": r["id"], "name": r["name"]} for r in rows]
    finally:
        if owns_conn:
            conn.close()


def list_learners_for_pack(db=None, pack_id: int = 0) -> List[Dict]:
    """
    Retourne les apprenants inscrits a un pack (course_tutor_id = pack_id).
    Filtre les statuts annules/trash.
    """
    if pack_id is None:
        return []
    conn = db or get_connection()
    owns_conn = db is None
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT s.id AS id, s.name AS name, s.email AS email
            FROM enrollments e
            JOIN students s ON s.id = e.student_id
            WHERE e.course_tutor_id = ?
              AND (
                    e.status IS NULL
                 OR LOWER(e.status) NOT IN ('cancel', 'cancelled', 'annule', 'annuler', 'trash')
              )
            ORDER BY s.name COLLATE NOCASE;
            """,
            (pack_id,),
        )
        rows = cur.fetchall()
        return [{"id": r["id"], "name": r["name"], "email": r["email"]} for r in rows]
    finally:
        if owns_conn:
            conn.close()


def _replace_participants(conn, session_id: int, member_ids: List[int], learner_ids: List[int], now: str) -> None:
    cur = conn.cursor()
    cur.execute("DELETE FROM session_members WHERE session_id = ?;", (session_id,))
    cur.execute("DELETE FROM session_learners WHERE session_id = ?;", (session_id,))
    if member_ids:
        cur.executemany(
            """
            INSERT INTO session_members (session_id, member_id, created_at)
            VALUES (?, ?, ?);
            """,
            [(session_id, mid, now) for mid in member_ids],
        )
    if learner_ids:
        cur.executemany(
            """
            INSERT INTO session_learners (session_id, learner_id, created_at)
            VALUES (?, ?, ?);
            """,
            [(session_id, lid, now) for lid in learner_ids],
        )


def _validate_inputs(
    title: Optional[str],
    start_at: str,
    end_at: str,
    member_ids: List[int],
    learner_ids: List[int],
    participants_count: Optional[int] = None,
):
    participants_count = (
        len(member_ids) + len(learner_ids) if participants_count is None else participants_count
    )
    if participants_count == 0:
        raise ValueError("Au moins un membre ou un apprenant doit etre selectionne.")
    try:
        start_dt = datetime.fromisoformat(start_at)
        end_dt = datetime.fromisoformat(end_at)
    except Exception as exc:  # noqa: BLE001
        raise ValueError("Dates invalides : utiliser un format ISO.") from exc
    if start_dt >= end_dt:
        raise ValueError("La date de debut doit etre anterieure a la date de fin.")


def create_session(
    db=None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    start_at: str = "",
    end_at: str = "",
    member_ids: Optional[List[int]] = None,
    learner_ids: Optional[List[int]] = None,
    create_google_event: bool = True,
    pack_id: Optional[int] = None,
) -> Dict:
    """
    Cree une session et, optionnellement, un evenement Google Calendar.
    Retourne le dict complet de la session.
    """
    member_ids = member_ids or []
    provided_learner_ids = learner_ids or []
    conn = db or get_connection()
    owns_conn = db is None
    try:
        resolved_learner_ids = list(provided_learner_ids)
        if not resolved_learner_ids and pack_id is not None:
            try:
                pack_learners = list_learners_for_pack(conn, pack_id)
                resolved_learner_ids = [l["id"] for l in pack_learners]
            except Exception as exc:  # noqa: BLE001
                log_error(f"[SessionService] Failed to load pack learners: {exc}")

        participants_count = len(member_ids) + len(resolved_learner_ids)
        _validate_inputs(
            title,
            start_at,
            end_at,
            member_ids,
            resolved_learner_ids,
            participants_count=participants_count,
        )
        now = _now_iso()
        # Recuperation des participants pour emails + description
        participant_conn = conn
        members = _fetch_members(participant_conn, member_ids)
        learners = _fetch_learners(participant_conn, resolved_learner_ids)

        session_title = title or f"Session P7 – {len(members)} membre(s) x {len(learners)} apprenant(s)"

        google_event_id = None
        meet_url = None
        if create_google_event:
            attendee_emails = {
                e
                for e in (
                    [m.get("email") for m in members] + [l.get("email") for l in learners]
                )
                if e
            }
            event = google_calendar_client.create_session_event(
                title=session_title,
                description=description,
                start_at=start_at,
                end_at=end_at,
                attendees_emails=list(attendee_emails) if attendee_emails else None,
            )
            if event is None:
                raise ValueError(
                    "Echec lors de la creation de l'evenement Google Calendar. Consultez l'onglet Admin > Logs."
                )
            google_event_id = event.get("event_id")
            meet_url = event.get("meet_url")

        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO sessions (
                title, description, start_at, end_at, status,
                meet_url, google_event_id, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                session_title,
                description,
                start_at,
                end_at,
                "planned",
                meet_url,
                google_event_id,
                now,
                now,
            ),
        )
        session_id = cur.lastrowid

        _replace_participants(conn, session_id, member_ids, resolved_learner_ids, now)
        conn.commit()

        log_info(
            f"[SessionService] Created session {session_id} with "
            f"{len(member_ids)} member(s) and {len(resolved_learner_ids)} learner(s)"
        )

        return {
            "id": session_id,
            "title": session_title,
            "description": description,
            "start_at": start_at,
            "end_at": end_at,
            "status": "planned",
            "meet_url": meet_url,
            "google_event_id": google_event_id,
            "members": members,
            "learners": learners,
        }
    finally:
        if owns_conn:
            conn.close()


def list_sessions(
    db=None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    member_id: Optional[int] = None,
    learner_id: Optional[int] = None,
    status: Optional[str] = None,
) -> List[Dict]:
    conn = db or get_connection()
    owns_conn = db is None
    try:
        query = """
            SELECT DISTINCT s.*
            FROM sessions s
            LEFT JOIN session_members sm ON sm.session_id = s.id
            LEFT JOIN session_learners sl ON sl.session_id = s.id
        """
        where: List[str] = []
        params: List = []

        if date_from:
            where.append("s.start_at >= ?")
            params.append(date_from)
        if date_to:
            where.append("s.start_at <= ?")
            params.append(date_to)
        if status:
            where.append("s.status = ?")
            params.append(status)
        if member_id:
            where.append("sm.member_id = ?")
            params.append(member_id)
        if learner_id:
            where.append("sl.learner_id = ?")
            params.append(learner_id)

        if where:
            query += " WHERE " + " AND ".join(where)

        query += " ORDER BY s.start_at ASC;"

        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        sessions = []
        session_ids = [r["id"] for r in rows]

        # Attach participants
        participants_map = _attach_participants(conn, session_ids)

        for r in rows:
            sid = r["id"]
            participants = participants_map.get(sid, {"members": [], "learners": []})
            sessions.append(
                {
                    "id": sid,
                    "title": r["title"],
                    "description": r["description"],
                    "start_at": r["start_at"],
                    "end_at": r["end_at"],
                    "status": r["status"],
                    "meet_url": r["meet_url"],
                    "google_event_id": r["google_event_id"],
                    "created_at": r["created_at"],
                    "updated_at": r["updated_at"],
                    "members": participants.get("members", []),
                    "learners": participants.get("learners", []),
                }
            )
        return sessions
    finally:
        if owns_conn:
            conn.close()


def get_session(db=None, session_id: int = 0) -> Optional[Dict]:
    conn = db or get_connection()
    owns_conn = db is None
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM sessions
            WHERE id = ?;
            """,
            (session_id,),
        )
        row = cur.fetchone()
        if not row:
            return None

        participants = _attach_participants(conn, [session_id]).get(
            session_id, {"members": [], "learners": []}
        )

        return {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "start_at": row["start_at"],
            "end_at": row["end_at"],
            "status": row["status"],
            "meet_url": row["meet_url"],
            "google_event_id": row["google_event_id"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "members": participants.get("members", []),
            "learners": participants.get("learners", []),
        }
    finally:
        if owns_conn:
            conn.close()


def cancel_session(db=None, session_id: int = 0, cancel_google_event: bool = True) -> bool:
    conn = db or get_connection()
    owns_conn = db is None
    try:
        cur = conn.cursor()
        cur.execute("SELECT google_event_id FROM sessions WHERE id = ?;", (session_id,))
        row = cur.fetchone()
        if not row:
            return False

        google_event_id = row[0]
        if cancel_google_event and google_event_id:
            try:
                google_calendar_client.delete_event(google_event_id)
            except Exception as exc:  # noqa: BLE001
                log_error(f"[SessionService] Google event deletion failed: {exc}")

        cur.execute(
            """
            UPDATE sessions
            SET status = ?, updated_at = ?
            WHERE id = ?;
            """,
            ("cancelled", _now_iso(), session_id),
        )
        conn.commit()
        log_info(f"[SessionService] Cancelled session {session_id}")
        return True
    finally:
        if owns_conn:
            conn.close()


def update_session(
    db=None,
    session_id: int = 0,
    title: str = "",
    description: Optional[str] = None,
    start_at: str = "",
    end_at: str = "",
    member_ids: Optional[List[int]] = None,
    learner_ids: Optional[List[int]] = None,
    with_google_event: bool = True,
) -> Optional[Dict]:
    member_ids = member_ids or []
    learner_ids = learner_ids or []
    _validate_inputs(title, start_at, end_at, member_ids, learner_ids)

    conn = db or get_connection()
    owns_conn = db is None
    try:
        existing = get_session(conn, session_id)
        if not existing:
            return None

        now = _now_iso()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE sessions
            SET title = ?, description = ?, start_at = ?, end_at = ?, updated_at = ?
            WHERE id = ?;
            """,
            (title, description, start_at, end_at, now, session_id),
        )

        _replace_participants(conn, session_id, member_ids, learner_ids, now)
        conn.commit()

        members = _fetch_members(conn, member_ids)
        learners = _fetch_learners(conn, learner_ids)
        google_event_id = existing.get("google_event_id")

        attendee_emails = {
            e
            for e in (
                [m.get("email") for m in members] + [l.get("email") for l in learners]
            )
            if e
        }

        if not with_google_event:
            if google_event_id:
                try:
                    google_calendar_client.delete_event(google_event_id)
                except Exception as exc:  # noqa: BLE001
                    log_error(f"[SessionService] Google event delete failed: {exc}")
            cur.execute(
                """
                UPDATE sessions
                SET google_event_id = NULL, meet_url = NULL, updated_at = ?
                WHERE id = ?;
                """,
                (now, session_id),
            )
            conn.commit()
        else:
            if google_event_id:
                try:
                    update_result = google_calendar_client.update_session_event(
                        event_id=google_event_id,
                        title=title,
                        description=description,
                        start_at=start_at,
                        end_at=end_at,
                        attendees_emails=list(attendee_emails),
                    )
                except Exception as exc:  # noqa: BLE001
                    raise RuntimeError(
                        "Google Calendar update failed"
                    ) from exc
                if not update_result:
                    raise RuntimeError("Google Calendar update failed (no response)")
                meet_url = update_result.get("meet_url") or existing.get("meet_url")
                cur.execute(
                    """
                    UPDATE sessions
                    SET meet_url = ?, updated_at = ?
                    WHERE id = ?;
                    """,
                    (meet_url, _now_iso(), session_id),
                )
                conn.commit()
            else:
                try:
                    create_result = google_calendar_client.create_session_event(
                        title=title,
                        description=description,
                        start_at=start_at,
                        end_at=end_at,
                        attendees_emails=list(attendee_emails),
                    )
                except Exception as exc:  # noqa: BLE001
                    raise RuntimeError(
                        "Google Calendar creation failed"
                    ) from exc
                if not create_result:
                    raise RuntimeError("Google Calendar creation failed (no response)")
                cur.execute(
                    """
                    UPDATE sessions
                    SET google_event_id = ?, meet_url = ?, updated_at = ?
                    WHERE id = ?;
                    """,
                    (
                        create_result.get("event_id"),
                        create_result.get("meet_url"),
                        _now_iso(),
                        session_id,
                    ),
                )
                conn.commit()

        return get_session(conn, session_id)
    finally:
        if owns_conn:
            conn.close()
