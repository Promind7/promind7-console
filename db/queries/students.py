
import sqlite3
from db.connection import get_connection
import consts

def _get_placeholders(values):
    return ",".join(["?"] * len(values))


def _enrollment_not_cancelled_sql(status_column: str) -> tuple[str, list]:
    """
    Inscriptions à afficher comme « présentes dans Tutor » : toutes sauf statuts annulés.
    Les statuts NULL ou inconnus sont conservés (export hétérogène).
    """
    ph = _get_placeholders(consts.ENROLLMENT_STATUS_CANCELLED_VALUES)
    sql = (
        f"( {status_column} IS NULL OR "
        f"LOWER(TRIM(CAST({status_column} AS TEXT))) NOT IN ({ph}) )"
    )
    return sql, list(consts.ENROLLMENT_STATUS_CANCELLED_VALUES)


def list_students():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            tutor_user_id,
            name,
            email,
            phone,
            birthdate,
            school,
            level,
            parent_name,
            parent_phone,
            parent_email,
            profile
        FROM students
        ORDER BY name ASC;
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "tutor_user_id": r["tutor_user_id"],
            "name": r["name"],
            "email": r["email"],
            "phone": r["phone"],
            "birthdate": r["birthdate"],
            "school": r["school"],
            "level": r["level"],
            "parent_name": r["parent_name"],
            "parent_phone": r["parent_phone"],
            "parent_email": r["parent_email"],
            "profile": r["profile"],
        }
        for r in rows
    ]


def list_students_with_packs():
    """
    Retourne les étudiants qui ont au moins une inscription active
    dans la table enrollments (au moins un pack non annulé).
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    placeholders = _get_placeholders(consts.ENROLLMENT_STATUS_CANCELLED_VALUES)
    params = list(consts.ENROLLMENT_STATUS_CANCELLED_VALUES)

    query = f"""
        SELECT DISTINCT
            s.id,
            s.tutor_user_id,
            s.name,
            s.email,
            s.phone,
            s.birthdate,
            s.school,
            s.level,
            s.parent_name,
            s.parent_phone,
            s.parent_email,
            s.profile
        FROM students AS s
        JOIN enrollments AS e
            ON e.student_id = s.id
        WHERE
            e.status IS NULL
            OR LOWER(e.status) NOT IN ({placeholders})
        ORDER BY s.name ASC;
        """

    cur.execute(query, params)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "tutor_user_id": r["tutor_user_id"],
            "name": r["name"],
            "email": r["email"],
            "phone": r["phone"],
            "birthdate": r["birthdate"],
            "school": r["school"],
            "level": r["level"],
            "parent_name": r["parent_name"],
            "parent_phone": r["parent_phone"],
            "parent_email": r["parent_email"],
            "profile": r["profile"],
        }
        for r in rows
    ]


def list_students_without_packs():
    """
    Retourne les étudiants qui n'ont AUCUNE inscription active
    dans la table enrollments (cibles pour proposer des packs).
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    placeholders = _get_placeholders(consts.ENROLLMENT_STATUS_CANCELLED_VALUES)
    params = list(consts.ENROLLMENT_STATUS_CANCELLED_VALUES)

    query = f"""
        SELECT
            s.id,
            s.tutor_user_id,
            s.name,
            s.email,
            s.phone,
            s.birthdate,
            s.school,
            s.level,
            s.parent_name,
            s.parent_phone,
            s.parent_email,
            s.profile
        FROM students AS s
        LEFT JOIN enrollments AS e
            ON e.student_id = s.id
           AND (
                e.status IS NULL
                OR LOWER(e.status) NOT IN ({placeholders})
           )
        WHERE e.student_id IS NULL
        ORDER BY s.name ASC;
        """

    cur.execute(query, params)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "tutor_user_id": r["tutor_user_id"],
            "name": r["name"],
            "email": r["email"],
            "phone": r["phone"],
            "birthdate": r["birthdate"],
            "school": r["school"],
            "level": r["level"],
            "parent_name": r["parent_name"],
            "parent_phone": r["parent_phone"],
            "parent_email": r["parent_email"],
            "profile": r["profile"],
        }
        for r in rows
    ]


def get_student(student_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            tutor_user_id,
            name,
            email,
            phone,
            birthdate,
            school,
            level,
            parent_name,
            parent_phone,
            parent_email,
            profile
        FROM students
        WHERE id = ?;
    """, (student_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row["id"],
        "tutor_user_id": row["tutor_user_id"],
        "name": row["name"],
        "email": row["email"],
        "phone": row["phone"],
        "birthdate": row["birthdate"],
        "school": row["school"],
        "level": row["level"],
        "parent_name": row["parent_name"],
        "parent_phone": row["parent_phone"],
        "parent_email": row["parent_email"],
        "profile": row["profile"],
    }


def update_student_profile(
    student_id: int,
    phone: str | None = None,
    birthdate: str | None = None,
    school: str | None = None,
    level: str | None = None,
    parent_name: str | None = None,
    parent_phone: str | None = None,
    parent_email: str | None = None,
    profile: str | None = None,
):
    """
    Met à jour les champs de profil apprenant pour un student donné.
    Ne modifie pas les champs importés (name, email, tutor_user_id).
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE students
        SET
            phone = COALESCE(?, phone),
            birthdate = COALESCE(?, birthdate),
            school = COALESCE(?, school),
            level = COALESCE(?, level),
            parent_name = COALESCE(?, parent_name),
            parent_phone = COALESCE(?, parent_phone),
            parent_email = COALESCE(?, parent_email),
            profile = COALESCE(?, profile)
        WHERE id = ?;
        """,
        (
            phone,
            birthdate,
            school,
            level,
            parent_name,
            parent_phone,
            parent_email,
            profile,
            student_id,
        ),
    )

    conn.commit()
    conn.close()


def list_student_enrollments(student_id: int):
    conn = get_connection()
    cur = conn.cursor()

    nc_sql, nc_params = _enrollment_not_cancelled_sql("e.status")
    params = [student_id] + nc_params

    query = f"""
        SELECT 
            e.id AS enrollment_id,
            e.student_id,
            e.course_tutor_id,
            e.enrolled_at,
            e.status,
            c.code AS course_code,
            c.title AS course_title
        FROM enrollments e
        LEFT JOIN courses c ON c.tutor_id = e.course_tutor_id
        WHERE e.student_id = ?
          AND {nc_sql}
        ORDER BY enrolled_at DESC;
    """

    cur.execute(query, params)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "enrollment_id": r["enrollment_id"],
            "student_id": r["student_id"],
            "course_tutor_id": r["course_tutor_id"],
            "course_code": r["course_code"],
            "course_title": r["course_title"],
            "enrolled_at": r["enrolled_at"],
            "status": r["status"],
        }
        for r in rows
    ]


def list_active_students():
    """
    Étudiants ayant au moins une inscription non annulée (table interne enrollments,
    alimentée par l'import Tutor).
    """
    conn = get_connection()
    cur = conn.cursor()

    nc_sql, nc_params = _enrollment_not_cancelled_sql("e.status")

    query = f"""
        SELECT DISTINCT
            s.id,
            s.tutor_user_id,
            s.name,
            s.email,
            s.phone,
            s.birthdate,
            s.school,
            s.level,
            s.parent_name,
            s.parent_phone,
            s.parent_email,
            s.profile
        FROM students AS s
        JOIN enrollments AS e ON e.student_id = s.id
        WHERE {nc_sql}
        ORDER BY s.name ASC;
    """

    cur.execute(query, nc_params)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "tutor_user_id": r["tutor_user_id"],
            "name": r["name"],
            "email": r["email"],
            "phone": r["phone"],
            "birthdate": r["birthdate"],
            "school": r["school"],
            "level": r["level"],
            "parent_name": r["parent_name"],
            "parent_phone": r["parent_phone"],
            "parent_email": r["parent_email"],
            "profile": r["profile"],
        }
        for r in rows
    ]


def list_student_enrollments_from_tutor(student_id: int):
    """
    Version robuste de list_student_enrollments:
    - lit les inscriptions dans tutor_enrollments,
    - s'appuie sur l'email / le nom de students,
    - joint avec courses (packs ProMind7) + tutor_courses (miroir Tutor LMS)
      pour récupérer code & titre du cours.

    Retourne la même structure que list_student_enrollments.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT name, email
        FROM students
        WHERE id = ?;
        """,
        (student_id,),
    )
    stu = cur.fetchone()
    if not stu:
        conn.close()
        return []

    student_name = stu["name"]
    student_email = stu["email"]

    params = []
    where_clauses = []

    if student_email:
        where_clauses.append("te.student_email = ?")
        params.append(student_email)

    if student_name and not student_email:
        where_clauses.append("te.student_name = ?")
        params.append(student_name)

    if not where_clauses:
        conn.close()
        return []

    where_sql = " OR ".join(where_clauses)

    nc_sql, nc_params = _enrollment_not_cancelled_sql("te.status")
    params.extend(nc_params)

    query = f"""
        SELECT
            te.id              AS enrollment_id,
            te.course_tutor_id AS course_tutor_id,
            te.enrolled_at     AS enrolled_at,
            te.status          AS status,
            c.code             AS course_code,
            COALESCE(c.title, tc.title) AS course_title
        FROM tutor_enrollments te
        LEFT JOIN courses c
            ON c.tutor_id = te.course_tutor_id
        LEFT JOIN tutor_courses tc
            ON tc.tutor_id = te.course_tutor_id
        WHERE ({where_sql})
          AND {nc_sql}
        ORDER BY te.enrolled_at DESC;
        """

    cur.execute(query, params)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "enrollment_id": r["enrollment_id"],
            "student_id": student_id,
            "course_tutor_id": r["course_tutor_id"],
            "course_code": r["course_code"],
            "course_title": r["course_title"],
            "enrolled_at": r["enrolled_at"],
            "status": r["status"],
        }
        for r in rows
    ]


def list_course_learners(course_tutor_id: int):
    """
    Retourne la liste des apprenants inscrits à un cours / pack donné,
    basée sur la table interne enrollments.

    Chaque entrée contient:
    - student_id
    - name
    - email
    - enrolled_at
    - status
    """
    conn = get_connection()
    cur = conn.cursor()

    nc_sql, nc_params = _enrollment_not_cancelled_sql("e.status")
    params = [course_tutor_id] + nc_params

    query = f"""
        SELECT
            s.id   AS student_id,
            s.name AS name,
            s.email AS email,
            e.enrolled_at AS enrolled_at,
            e.status AS status
        FROM enrollments e
        JOIN students s ON s.id = e.student_id
        WHERE e.course_tutor_id = ?
          AND {nc_sql}
        ORDER BY s.name ASC;
        """

    cur.execute(query, params)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "student_id": r["student_id"],
            "name": r["name"],
            "email": r["email"],
            "enrolled_at": r["enrolled_at"],
            "status": r["status"],
        }
        for r in rows
    ]


def list_pack_enrollment_stats():
    """
    Statistiques d'inscriptions par pack / cours Tutor LMS.

    - Base : table tutor_courses (tous les cours importés depuis Tutor LMS).
    - On compte les inscriptions dans tutor_enrollments.
    - On exclut les inscriptions annulées ; email ou nom requis pour compter une ligne.
    - On affiche tous les packs, même sans inscrits (valeur 0).
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    nc_sql, nc_params = _enrollment_not_cancelled_sql("status")

    query = f'''
        WITH enroll_stats AS (
            SELECT
                course_tutor_id,
                COUNT(*) AS enrollments
            FROM tutor_enrollments
            WHERE {nc_sql}
              AND (
                (student_email IS NOT NULL AND TRIM(student_email) <> '')
                OR (student_name IS NOT NULL AND TRIM(student_name) <> '')
              )
            GROUP BY course_tutor_id
        )
        SELECT
            COALESCE(c.tutor_id, tc.tutor_id) AS course_tutor_id,
            c.code AS course_code,
            COALESCE(c.title, tc.title, "Cours sans titre") AS course_title,
            COALESCE(es.enrollments, 0) AS enrollments
        FROM tutor_courses tc
        LEFT JOIN courses c
            ON c.tutor_id = tc.tutor_id
        LEFT JOIN enroll_stats es
            ON es.course_tutor_id = tc.tutor_id
        ORDER BY c.code ASC, course_tutor_id ASC;
        '''

    cur.execute(query, nc_params)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "course_tutor_id": r["course_tutor_id"],
            "course_code": r["course_code"],
            "course_title": r["course_title"],
            "enrollments": r["enrollments"],
        }
        for r in rows
    ]


def list_enrollment_timeline():
    """
    Retourne l'évolution des inscriptions Tutor LMS par jour.
    """
    conn = get_connection()
    cur = conn.cursor()

    nc_sql, nc_params = _enrollment_not_cancelled_sql("status")

    query = f"""
        SELECT
            DATE(enrolled_at) AS d,
            COUNT(*) AS enrollments
        FROM tutor_enrollments
        WHERE
            enrolled_at IS NOT NULL
            AND {nc_sql}
        GROUP BY DATE(enrolled_at)
        ORDER BY DATE(enrolled_at) ASC;
        """

    cur.execute(query, nc_params)

    rows = cur.fetchall()
    conn.close()

    return [
        {"date": r["d"], "enrollments": r["enrollments"]}
        for r in rows
    ]


def list_risky_learners(limit: int = 10):
    """
    Apprenants à surveiller (placeholder) basé sur les statuts des inscriptions.
    """
    conn = get_connection()
    cur = conn.cursor()

    completed_ph = _get_placeholders(consts.ENROLLMENT_STATUS_COMPLETED_VALUES)
    cancelled_ph = _get_placeholders(consts.ENROLLMENT_STATUS_CANCELLED_VALUES)
    
    params = list(consts.ENROLLMENT_STATUS_COMPLETED_VALUES) + list(consts.ENROLLMENT_STATUS_CANCELLED_VALUES) + [limit]

    query = f"""
        SELECT
            s.name AS name,
            s.email AS email,
            COUNT(*) AS total_enrollments,
            SUM(CASE WHEN LOWER(te.status) IN ({completed_ph}) THEN 1 ELSE 0 END) AS completed,
            SUM(CASE WHEN LOWER(te.status) IN ({cancelled_ph}) THEN 1 ELSE 0 END) AS cancelled
        FROM tutor_enrollments te
        LEFT JOIN students s
            ON s.email = te.student_email
        GROUP BY s.name, s.email
        HAVING cancelled > 0 AND completed = 0
        ORDER BY cancelled DESC, total_enrollments DESC
        LIMIT ?;
        """

    cur.execute(query, params)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "name": r["name"],
            "email": r["email"],
            "total_enrollments": r["total_enrollments"],
            "completed": r["completed"],
            "cancelled": r["cancelled"],
        }
        for r in rows
    ]


def upsert_student_from_tutor(
    name: str | None,
    email: str | None,
    username: str | None = None,
):
    """
    Crée ou met à jour un étudiant dans la table students à partir
    des données Tutor LMS (nom, email, username).

    Règles :
    - Si email est présent, on l'utilise comme clé principale.
    - Sinon, si pas d'email mais un name, on utilise le name comme clé.
    - tutor_user_id reste éventuellement NULL (on n'a pas toujours l'ID numérique).
    """
    if not (email or name):
        # rien de fiable pour identifier l'étudiant
        return

    conn = get_connection()
    cur = conn.cursor()

    row = None
    if email:
        cur.execute(
            "SELECT id, name, email FROM students WHERE email = ?;",
            (email,),
        )
        row = cur.fetchone()

    if row is None and name:
        cur.execute(
            "SELECT id, name, email FROM students WHERE name = ?;",
            (name,),
        )
        row = cur.fetchone()

    if row is None:
        cur.execute(
            """
            INSERT INTO students (
                tutor_user_id,
                name,
                email,
                phone,
                birthdate,
                school,
                level,
                parent_name,
                parent_phone,
                parent_email,
                profile
            )
            VALUES (?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
            """,
            (None, name, email),
        )
    else:
        current_name = row["name"]
        current_email = row["email"]
        new_name = name or current_name
        new_email = email or current_email
        cur.execute(
            """
            UPDATE students
            SET name = ?, email = ?
            WHERE id = ?;
            """,
            (new_name, new_email, row["id"]),
        )

    conn.commit()
    conn.close()


def upsert_enrollment_for_student_identity(
    student_name: str | None,
    student_email: str | None,
    course_tutor_id: int,
    enrolled_at: str | None,
    status: str | None,
):
    """
    Crée ou met à jour une inscription dans la table enrollments
    pour un étudiant identifié par email ou nom.

    - Si email est présent, on cherche d'abord par email.
    - Sinon, on cherche par nom.
    - Si aucun student n'est trouvé, on ne fait rien.
    - Si une inscription existe déjà pour (student_id, course_tutor_id),
      on met à jour enrolled_at et status.
    """
    if not (student_email or student_name):
        return

    conn = get_connection()
    cur = conn.cursor()

    row = None
    if student_email:
        cur.execute(
            "SELECT id FROM students WHERE email = ?;",
            (student_email,),
        )
        row = cur.fetchone()

    if row is None and student_name:
        cur.execute(
            "SELECT id FROM students WHERE name = ?;",
            (student_name,),
        )
        row = cur.fetchone()

    if not row:
        conn.close()
        return

    student_id = row["id"]

    # Check existence
    cur.execute(
        """
        SELECT id FROM enrollments
        WHERE student_id = ? AND course_tutor_id = ?;
        """,
        (student_id, course_tutor_id),
    )
    existing_enroll = cur.fetchone()

    if existing_enroll:
        cur.execute(
            """
            UPDATE enrollments
            SET enrolled_at = COALESCE(?, enrolled_at),
                status = COALESCE(?, status)
            WHERE id = ?;
            """,
            (enrolled_at, status, existing_enroll["id"]),
        )
    else:
        cur.execute(
            """
            INSERT INTO enrollments (student_id, course_tutor_id, enrolled_at, status)
            VALUES (?, ?, ?, ?);
            """,
            (student_id, course_tutor_id, enrolled_at, status),
        )

    conn.commit()
    conn.close()


def sync_learners_from_tutor_enrollments_mirror() -> None:
    """
    Après import Tutor : reconstruit ``enrollments`` depuis ``tutor_enrollments``,
    puis supprime les lignes ``students`` sans aucune inscription interne.

    Effet : liste Apprenants = strictement ce que contient l’export (miroir),
    sans supprimer ``promind7.db`` à la main. Les champs de profil ProMind7
    (téléphone, etc.) sont conservés pour les apprenants toujours présents
    dans le miroir (même clé email / nom).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM enrollments;")
    conn.commit()
    conn.close()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT course_tutor_id, student_name, student_email, student_username,
               enrolled_at, status
        FROM tutor_enrollments
        ORDER BY id;
        """
    )
    rows = cur.fetchall()
    conn.close()

    for r in rows:
        email = (r["student_email"] or "").strip() or None
        name = (r["student_name"] or "").strip() or None
        if not (email or name):
            continue
        upsert_student_from_tutor(
            name=name,
            email=email,
            username=r["student_username"],
        )
        upsert_enrollment_for_student_identity(
            student_name=name,
            student_email=email,
            course_tutor_id=r["course_tutor_id"],
            enrolled_at=r["enrolled_at"],
            status=r["status"],
        )

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM students
        WHERE NOT EXISTS (
            SELECT 1 FROM enrollments e WHERE e.student_id = students.id
        );
        """
    )
    conn.commit()
    conn.close()


def search_in_students(keyword: str):
    """
    L’agent IA peut chercher un apprenant.
    """
    conn = get_connection()
    cur = conn.cursor()

    kw = f"%{keyword.lower()}%"

    cur.execute("""
        SELECT id, name, email
        FROM students
        WHERE LOWER(name) LIKE ? 
           OR LOWER(email) LIKE ?;
    """, (kw, kw))

    rows = cur.fetchall()
    conn.close()

    return [
        {"id": r["id"], "name": r["name"], "email": r["email"]}
        for r in rows
    ]
