
from .connection import get_connection, get_db_path
from .schema import init_db

from .queries.content import (
    upsert_tutor_course_from_export,
    upsert_tutor_module_from_export,
    upsert_tutor_lesson_from_export,
    prune_tutor_mirror_to_imported_course_ids,
    list_parcours_for_tasks,
    list_packs,
    list_modules,
    list_lessons,
    list_quizzes,
    search_in_packs,
)

from .queries.students import (
    list_students,
    list_students_with_packs,
    list_students_without_packs,
    get_student,
    update_student_profile,
    list_student_enrollments,
    list_active_students,
    list_student_enrollments_from_tutor,
    list_course_learners,
    list_pack_enrollment_stats,
    list_enrollment_timeline,
    list_risky_learners,
    upsert_student_from_tutor,
    upsert_enrollment_for_student_identity,
    sync_learners_from_tutor_enrollments_mirror,
    search_in_students,
)

from .queries.tasks import (
    add_task,
    list_tasks,
    list_task_stats_by_pack,
    update_task_status,
    update_task,
    delete_task,
    resolve_pack_label,
)

from .queries.team import (
    list_team_members,
    get_team_member,
    get_team_member_by_name,
    update_team_member_bio,
    create_team_member,
    update_team_member,
    delete_team_member,
)

from .queries.stats import (
    count_courses,
    count_modules,
    count_lessons,
    count_quizzes,
    count_students,
    count_active_learners,
    count_total_tutor_enrollments,
    count_open_tasks,
    count_high_priority_open_tasks,
    count_tasks,
)
