"""
Service de synchronisation V3 API Tutor LMS (désactivé côté UI).
NOTE : L'import apprenants officiel reste le ZIP (V2).
Ce module est conservé pour de futures évolutions (V3.1).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from db import (
    get_connection,
    upsert_student_from_tutor,
    upsert_enrollment_for_student_identity,
)
from integrations.tutor_api_client import fetch_enrollments_since
from services.log_service import log_error, log_info, log_warn


@dataclass
class SyncResult:
    total_fetched: int = 0
    created_count: int = 0
    updated_count: int = 0
    skipped_count: int = 0
    errors: List[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_seconds: float = 0.0


def _normalize_enrollment(raw: Dict) -> Optional[Dict]:
    """
    Converge l'objet enrollment API vers la structure attendue par l'import ZIP :
    - course_tutor_id : ID du cours Tutor (course_id / course)
    - status / enrolled_at : champs dates/statuts bruts
    - student_* : nom/email/username, tutor_user_id
    Ingestion brute : aucun filtre métier (completed, pack...) ici.
    """
    enrollment_part = raw.get("enrollment") or raw.get("data") or raw
    student_part = raw.get("student") or raw.get("user") or raw.get("learner") or raw

    raw_course = (
        enrollment_part.get("course_id")
        or enrollment_part.get("course")
        or enrollment_part.get("course_tutor_id")
        or raw.get("course_id")
        or raw.get("course")
    )
    course_tutor_id = None
    try:
        course_tutor_id = int(raw_course) if raw_course is not None else None
    except (TypeError, ValueError):
        course_tutor_id = raw_course

    status = (
        enrollment_part.get("status")
        or enrollment_part.get("post_status")
        or raw.get("status")
    )

    enrolled_at = (
        enrollment_part.get("enrolled_at")
        or enrollment_part.get("created_at")
        or enrollment_part.get("post_date")
        or enrollment_part.get("post_date_gmt")
        or enrollment_part.get("post_modified")
    )

    tutor_user_id = (
        student_part.get("id")
        or student_part.get("ID")
        or student_part.get("user_id")
        or student_part.get("tutor_user_id")
        or student_part.get("tutor_id")
    )
    email = (
        student_part.get("email")
        or student_part.get("user_email")
        or student_part.get("student_email")
        or enrollment_part.get("student_email")
        or raw.get("student_email")
    )
    name = (
        student_part.get("name")
        or student_part.get("full_name")
        or student_part.get("display_name")
        or student_part.get("user_nicename")
        or student_part.get("user_login")
        or enrollment_part.get("student_name")
        or raw.get("student_name")
    )
    username = (
        student_part.get("username")
        or student_part.get("user_login")
        or student_part.get("user_nicename")
        or student_part.get("student_username")
        or raw.get("student_username")
    )

    if not course_tutor_id:
        return None

    return {
        "course_tutor_id": course_tutor_id,
        "status": status,
        "enrolled_at": enrolled_at,
        "student_name": name.strip() if isinstance(name, str) else None,
        "student_email": email.strip().lower() if isinstance(email, str) and email.strip() else None,
        "student_username": username.strip() if isinstance(username, str) else None,
        "tutor_user_id": int(tutor_user_id) if tutor_user_id not in (None, "") else None,
        "raw": raw,
    }


def _build_existing_maps(cur, tutor_ids: set, emails: set) -> Tuple[Dict, Dict]:
    existing_by_tutor_id: Dict[int, Dict] = {}
    existing_by_email: Dict[str, Dict] = {}

    if tutor_ids:
        placeholders = ",".join(["?"] * len(tutor_ids))
        cur.execute(
            f"""
            SELECT id, tutor_user_id, name, email
            FROM students
            WHERE tutor_user_id IN ({placeholders});
            """,
            list(tutor_ids),
        )
        for row in cur.fetchall():
            existing_by_tutor_id[row["tutor_user_id"]] = {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "tutor_user_id": row["tutor_user_id"],
            }

    if emails:
        placeholders = ",".join(["?"] * len(emails))
        cur.execute(
            f"""
            SELECT id, tutor_user_id, name, email
            FROM students
            WHERE email IN ({placeholders});
            """,
            list(emails),
        )
        for row in cur.fetchall():
            existing_by_email[(row["email"] or "").lower()] = {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "tutor_user_id": row["tutor_user_id"],
            }

    return existing_by_tutor_id, existing_by_email


def sync_learners_from_api(
    since: datetime | None, batch_size: int = 100, dry_run: bool = False
) -> SyncResult:
    # Import API V3 aligne sur l'import ZIP : ingestion brute dans tutor_enrollments.
    # Aucun filtre metier (completed/pack/clients potentiels) n'est applique ici ;
    # ces filtres restent dans les services/onglets en aval.
    result = SyncResult(started_at=datetime.utcnow())

    try:
        enrollments = fetch_enrollments_since(since, page_size=batch_size)
    except Exception as exc:
        log_error(f"[LearnerSync] API fetch failed: {exc}")
        result.errors.append(f"API fetch failed: {exc}")
        result.finished_at = datetime.utcnow()
        result.duration_seconds = (result.finished_at - result.started_at).total_seconds()
        return result

    result.total_fetched = len(enrollments)
    log_info(f"[LearnerSync] API returned {result.total_fetched} enrollments (raw).")

    if not enrollments:
        log_info("[LearnerSync] No enrollments returned by API.")
        result.finished_at = datetime.utcnow()
        result.duration_seconds = (result.finished_at - result.started_at).total_seconds()
        return result

    normalized: List[Dict] = []
    for raw in enrollments:
        norm = _normalize_enrollment(raw) if isinstance(raw, dict) else None
        if norm:
            normalized.append(norm)
        else:
            result.skipped_count += 1
            log_warn("[LearnerSync] Skipped enrollment (missing course_tutor_id).")

    if not normalized:
        result.finished_at = datetime.utcnow()
        result.duration_seconds = (result.finished_at - result.started_at).total_seconds()
        return result

    tutor_ids = {n["tutor_user_id"] for n in normalized if n["tutor_user_id"] is not None}
    emails = {n["student_email"] for n in normalized if n["student_email"] is not None}
    course_ids = {n["course_tutor_id"] for n in normalized}

    try:
        conn = get_connection()
        cur = conn.cursor()

        existing_by_tutor_id, existing_by_email = _build_existing_maps(cur, tutor_ids, emails)

        # Tutor_enrollments ingestion brute
        rows_to_insert: List[Tuple] = []

        for n in normalized:
            raw_json = json.dumps(n["raw"], ensure_ascii=False)
            rows_to_insert.append(
                (
                    n["course_tutor_id"],
                    n["student_name"],
                    n["student_email"],
                    n["student_username"],
                    n["enrolled_at"],
                    n["status"],
                    raw_json,
                )
            )

            # Synchronisation students/enrollments internes : ingestion brute
            # (pas de filtre metier ici). On repose sur upsert_student_from_tutor
            # et upsert_enrollment_for_student_identity, comme pour l'import ZIP.
            email = n["student_email"]
            name = n["student_name"] or n["student_username"]
            username = n["student_username"]

            if not (email or name):
                result.skipped_count += 1
                log_warn("[LearnerSync] Skipped student sync (no name/email).")
                continue

            existing = None
            if n["tutor_user_id"] is not None and n["tutor_user_id"] in existing_by_tutor_id:
                existing = existing_by_tutor_id[n["tutor_user_id"]]
            elif email and email in existing_by_email:
                existing = existing_by_email[email]

            if existing:
                result.updated_count += 1
            else:
                result.created_count += 1

            if not dry_run:
                upsert_student_from_tutor(
                    name=name,
                    email=email,
                    username=username,
                )
                upsert_enrollment_for_student_identity(
                    student_name=name,
                    student_email=email,
                    course_tutor_id=n["course_tutor_id"],
                    enrolled_at=n["enrolled_at"],
                    status=n["status"],
                )

        if not dry_run and rows_to_insert:
            if since is None:
                cur.execute("DELETE FROM tutor_enrollments;")
                log_info("[LearnerSync] Full sync: cleared all tutor_enrollments before insert.")
            else:
                if course_ids:
                    placeholders = ",".join("?" for _ in course_ids)
                    cur.execute(
                        f"DELETE FROM tutor_enrollments WHERE course_tutor_id IN ({placeholders});",
                        list(course_ids),
                    )
                    log_info(
                        f"[LearnerSync] Incremental sync: cleared tutor_enrollments for {len(course_ids)} course(s)."
                    )
            cur.executemany(
                """
                INSERT INTO tutor_enrollments (
                    course_tutor_id,
                    student_name,
                    student_email,
                    student_username,
                    enrolled_at,
                    status,
                    raw_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                rows_to_insert,
            )
            conn.commit()
        elif dry_run:
            log_info("[LearnerSync] Dry-run enabled: no DB writes performed.")

    except Exception as exc:
        log_error(f"[LearnerSync] DB error: {exc}")
        result.errors.append(f"DB error: {exc}")
        try:
            conn.rollback()
        except Exception:
            pass
    finally:
        try:
            conn.close()
        except Exception:
            pass

    result.finished_at = datetime.utcnow()
    result.duration_seconds = (result.finished_at - (result.started_at or result.finished_at)).total_seconds()

    log_info(
        "[LearnerSync] Finished (fetched=%s, created=%s, updated=%s, skipped=%s, dry_run=%s, duration=%.2fs)"
        % (
            result.total_fetched,
            result.created_count,
            result.updated_count,
            result.skipped_count,
            dry_run,
            result.duration_seconds,
        )
    )

    return result


def prune_orphan_students_after_sync(conn=None) -> int:
    """
    Identifie et supprime les apprenants qui n'ont plus aucune source Tutor LMS
    (aucune entree dans tutor_enrollments). TODO: brancher cette fonction via
    un bouton Admin ou une tache planifiee pour nettoyage durable.
    Retourne le nombre de students supprimes.
    """
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    cur = conn.cursor()

    cur.execute(
        """
        SELECT id FROM students
        WHERE id NOT IN (
            SELECT DISTINCT COALESCE(s.id, e.student_id)
            FROM students s
            LEFT JOIN enrollments e ON e.student_id = s.id
            LEFT JOIN tutor_enrollments te ON te.student_email = s.email
            WHERE te.student_email IS NOT NULL
        );
        """
    )
    to_delete = [row[0] for row in cur.fetchall()]

    if not to_delete:
        if close_conn:
            conn.close()
        return 0

    placeholders = ",".join("?" for _ in to_delete)
    # Suppression des dependances directes connues (enrollments), les autres
    # references applicatives devront etre ajoutees ici si besoin.
    cur.execute(f"DELETE FROM enrollments WHERE student_id IN ({placeholders});", to_delete)
    cur.execute(f"DELETE FROM students WHERE id IN ({placeholders});", to_delete)
    conn.commit()

    if close_conn:
        conn.close()

    return len(to_delete)
