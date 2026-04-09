import contextlib
import unicodedata
import re
from db.connection import get_connection

# Synchronisation Tutor LMS -> interne :
# - tutor_courses -> courses + packs (codes alignés sur un slug stable du titre ou code existant)
# - tutor_modules -> modules (upsert par tutor_id)
# - tutor_lessons -> lessons (upsert par tutor_id)


def slugify(value: str) -> str:
    """
    Transforme un titre en code "slug" :
    - supprime les accents (Découverte -> Decouverte)
    - met en minuscules
    - remplace les séparateurs interdits par des underscores
    - conserve uniquement [a-z0-9_]
    - retire un éventuel préfixe "pack_" pour éviter "pack_pack_..."
    """
    if not value:
        return "pack"

    # Normalisation unicode -> suppression des accents
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")

    value = value.lower()
    value = re.sub(r"[\\/:*?\"<>|]", " ", value)
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = value.strip("_")
    if value.startswith("pack_"):
        value = value[len("pack_"):]
    return value or "pack"


def compute_pack_code_from_title(title: str) -> str:
    """
    Calcule un code de pack stable à partir d'un titre Tutor LMS :
    - accents supprimés (NFKD + ASCII)
    - minuscules
    - séparateurs interdits -> underscore
    - uniquement [a-z0-9_]
    - pas de préfixe "pack_"
    """
    base = title or "pack"
    base = unicodedata.normalize("NFKD", base)
    base = base.encode("ascii", "ignore").decode("ascii")
    base = base.lower()
    base = re.sub(r"[\\/:*?\"<>|]", " ", base)
    base = re.sub(r"[^a-z0-9]+", "_", base)
    base = base.strip("_")
    return base or "pack"


def _get_connection(conn=None):
    """
    Utility interne :
    - Si une connexion est fournie, on la réutilise sans la fermer.
    - Sinon, on ouvre une connexion temporaire avec fermeture automatique.
    """
    if conn is not None:
        @contextlib.contextmanager
        def _ctx():
            yield conn
        return _ctx()

    @contextlib.contextmanager
    def _ctx():
        local = get_connection()
        try:
            yield local
        finally:
            local.close()
    return _ctx()


def sync_internal_catalog_from_tutor(conn=None) -> None:
    """
    Synchronise les tables internes :
        - courses
        - packs
        - modules
        - lessons

    À partir des tables :
        - tutor_courses
        - tutor_modules
        - tutor_lessons

    Cette fonction ne supprime rien : elle fait des upserts
    basés sur le champ tutor_id (UNIQUE) des tables internes.
    """
    with _get_connection(conn) as db:
        cur = db.cursor()

        # 1) COURSES + PACKS à partir de tutor_courses
        cur.execute(
            """
            SELECT tutor_id, title
            FROM tutor_courses
            ORDER BY tutor_id;
            """
        )
        tutor_courses = cur.fetchall()

        for row in tutor_courses:
            tutor_id = row["tutor_id"]
            title = row["title"] or f"Course {tutor_id}"
            candidate_code = compute_pack_code_from_title(title)

            # On privilégie les codes déjà existants : pack par titre, puis course existante, sinon slug candidat.
            cur.execute(
                """
                SELECT code
                FROM packs
                WHERE lower(title) = lower(?)
                LIMIT 1;
                """,
                (title,),
            )
            pack_match = cur.fetchone()
            pack_code_from_title = pack_match["code"] if pack_match else None

            cur.execute(
                """
                SELECT code
                FROM courses
                WHERE tutor_id = ?
                LIMIT 1;
                """,
                (tutor_id,),
            )
            course_match = cur.fetchone()
            existing_course_code = course_match["code"] if course_match and course_match["code"] else None

            pack_code = pack_code_from_title or existing_course_code or candidate_code

            # Table courses interne
            cur.execute(
                """
                INSERT INTO courses (tutor_id, code, title, description)
                VALUES (?, ?, ?, NULL)
                ON CONFLICT(tutor_id)
                DO UPDATE SET
                    code = excluded.code,
                    title = excluded.title;
                """,
                (tutor_id, pack_code, title),
            )

            # Table packs interne
            cur.execute(
                """
                INSERT INTO packs (code, title, description)
                VALUES (?, ?, NULL)
                ON CONFLICT(code)
                DO UPDATE SET
                    title = excluded.title;
                """,
                (pack_code, title),
            )

        # 2) MODULES internes à partir de tutor_modules
        cur.execute(
            """
            SELECT tutor_id, course_tutor_id, title, order_index
            FROM tutor_modules
            ORDER BY course_tutor_id, order_index;
            """
        )
        tutor_modules = cur.fetchall()

        for row in tutor_modules:
            tutor_id = row["tutor_id"]
            course_tutor_id = row["course_tutor_id"]
            title = row["title"] or f"Module {tutor_id}"
            module_code = f"M{tutor_id}"

            cur.execute(
                """
                INSERT INTO modules (
                    id,
                    tutor_id,
                    course_tutor_id,
                    module_code,
                    title,
                    description
                )
                SELECT
                    (SELECT id FROM modules WHERE tutor_id = ?),
                    ?, ?, ?, ?, NULL
                WHERE NOT EXISTS (
                    SELECT 1 FROM modules WHERE tutor_id = ?
                );
                """,
                (tutor_id, tutor_id, course_tutor_id, module_code, title, tutor_id),
            )

            # Upsert via tutor_id (pour SQLite anciennes versions qui gèrent mal "excluded")
            cur.execute(
                """
                UPDATE modules
                SET course_tutor_id = ?,
                    module_code = ?,
                    title = ?
                WHERE tutor_id = ?;
                """,
                (course_tutor_id, module_code, title, tutor_id),
            )

        # 3) LEÇONS internes à partir de tutor_lessons
        cur.execute(
            """
            SELECT tutor_id, module_tutor_id, title, order_index
            FROM tutor_lessons
            ORDER BY module_tutor_id, order_index;
            """
        )
        tutor_lessons = cur.fetchall()

        for row in tutor_lessons:
            tutor_id = row["tutor_id"]
            module_tutor_id = row["module_tutor_id"]
            title = row["title"] or f"Lesson {tutor_id}"
            lesson_code = f"L{tutor_id}"

            cur.execute(
                """
                INSERT INTO lessons (
                    id,
                    tutor_id,
                    module_tutor_id,
                    lesson_code,
                    title,
                    content
                )
                SELECT
                    (SELECT id FROM lessons WHERE tutor_id = ?),
                    ?, ?, ?, ?, NULL
                WHERE NOT EXISTS (
                    SELECT 1 FROM lessons WHERE tutor_id = ?
                );
                """,
                (tutor_id, tutor_id, module_tutor_id, lesson_code, title, tutor_id),
            )

            cur.execute(
                """
                UPDATE lessons
                SET module_tutor_id = ?,
                    lesson_code = ?,
                    title = ?
                WHERE tutor_id = ?;
                """,
                (module_tutor_id, lesson_code, title, tutor_id),
            )

        db.commit()
