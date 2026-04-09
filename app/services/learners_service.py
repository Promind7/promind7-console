from typing import List, Dict, Optional

from db import (
    list_students as db_list_students,
    get_student as db_get_student,
    list_student_enrollments_from_tutor as db_list_student_enrollments,
    update_student_profile as db_update_student_profile,
    list_course_learners as db_list_course_learners,
    list_pack_enrollment_stats as db_list_pack_enrollment_stats,
)


def list_students() -> List[Dict]:
    return db_list_students()


def get_student(student_id: int) -> Optional[Dict]:
    return db_get_student(student_id)


def list_student_enrollments(student_id: int) -> List[Dict]:
    return db_list_student_enrollments(student_id)


def update_profile(
    student_id: int,
    phone: Optional[str] = None,
    birthdate: Optional[str] = None,
    school: Optional[str] = None,
    level: Optional[str] = None,
    parent_name: Optional[str] = None,
    parent_phone: Optional[str] = None,
    parent_email: Optional[str] = None,
    profile: Optional[str] = None,
) -> None:
    db_update_student_profile(
        student_id=student_id,
        phone=phone,
        birthdate=birthdate,
        school=school,
        level=level,
        parent_name=parent_name,
        parent_phone=parent_phone,
        parent_email=parent_email,
        profile=profile,
    )


def list_course_learners(course_tutor_id: int) -> List[Dict]:
    return db_list_course_learners(course_tutor_id)


def list_pack_enrollment_stats() -> List[Dict]:
    """
    Retourne les stats d'inscriptions par pack / cours (via tutor_enrollments).
    """
    return db_list_pack_enrollment_stats()
