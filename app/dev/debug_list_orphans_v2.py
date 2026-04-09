from pathlib import Path

from db import get_connection
from services.content_service import (
    get_content_root,
    build_pack_dir_name,
    build_module_dir_name,
    build_lesson_dir_name,
    extract_id_from_name,
)


def main() -> None:
    root: Path = get_content_root()
    print("CONTENT ROOT:", root)

    conn = get_connection()
    try:
        cur = conn.cursor()

        # IDs + noms officiels depuis Tutor
        cur.execute("SELECT tutor_id, title FROM tutor_courses;")
        courses = cur.fetchall()
        course_ids = {row["tutor_id"] for row in courses}
        official_packs = {
            row["tutor_id"]: build_pack_dir_name(row["tutor_id"], row["title"] or f"Cours {row['tutor_id']}")
            for row in courses
        }

        cur.execute("SELECT tutor_id, title, course_tutor_id FROM tutor_modules;")
        modules = cur.fetchall()
        module_ids = {row["tutor_id"] for row in modules}
        official_modules = {
            row["tutor_id"]: build_module_dir_name(row["tutor_id"], row["title"] or f"Module {row['tutor_id']}")
            for row in modules
        }
        module_course_map = {row["tutor_id"]: row["course_tutor_id"] for row in modules}

        cur.execute("SELECT tutor_id, title, module_tutor_id FROM tutor_lessons;")
        lessons = cur.fetchall()
        lesson_ids = {row["tutor_id"] for row in lessons}
        official_lessons = {
            row["tutor_id"]: build_lesson_dir_name(row["tutor_id"], row["title"] or f"Lecon {row['tutor_id']}")
            for row in lessons
        }
        lesson_module_map = {row["tutor_id"]: row["module_tutor_id"] for row in lessons}

    finally:
        conn.close()

    orphan_packs = []
    orphan_modules = []
    orphan_lessons = []

    # Packs
    for pack_path in root.iterdir():
        if not pack_path.is_dir():
            continue

        pack_name = pack_path.name
        course_id = extract_id_from_name(pack_name)
        if course_id is None:
            continue

        if course_id not in course_ids:
            orphan_packs.append((pack_name, "ID inconnu en base"))
            continue

        official = official_packs.get(course_id)
        if official and pack_name != official:
            orphan_packs.append((pack_name, f"nom != officiel ({official})"))

        # Modules
        for module_path in pack_path.iterdir():
            if not module_path.is_dir():
                continue

            module_name = module_path.name
            module_id = extract_id_from_name(module_name)
            if module_id is None:
                continue

            if module_id not in module_ids:
                orphan_modules.append((pack_name, module_name, "ID inconnu en base"))
                continue

            if module_course_map.get(module_id) not in {course_id}:
                orphan_modules.append((pack_name, module_name, "module rattache a un autre cours"))
                continue

            official_mod = official_modules.get(module_id)
            if official_mod and module_name != official_mod:
                orphan_modules.append((pack_name, module_name, f"nom != officiel ({official_mod})"))

            # Leçons
            for lesson_path in module_path.iterdir():
                if not lesson_path.is_dir():
                    continue

                lesson_name = lesson_path.name
                lesson_id = extract_id_from_name(lesson_name)
                if lesson_id is None:
                    continue

                if lesson_id not in lesson_ids:
                    orphan_lessons.append(
                        (pack_name, module_name, lesson_name, "ID inconnu en base")
                    )
                    continue

                if lesson_module_map.get(lesson_id) not in {module_id}:
                    orphan_lessons.append(
                        (pack_name, module_name, lesson_name, "lecon rattachee a un autre module")
                    )
                    continue

                official_les = official_lessons.get(lesson_id)
                if official_les and lesson_name != official_les:
                    orphan_lessons.append(
                        (pack_name, module_name, lesson_name, f"nom != officiel ({official_les})")
                    )

    print("\nPacks orphelins / obsoletes :")
    if not orphan_packs:
        print("  Aucun")
    else:
        for name, reason in orphan_packs:
            print(f"  - {name}  -> {reason}")

    print("\nModules orphelins / obsoletes :")
    if not orphan_modules:
        print("  Aucun")
    else:
        for pack_name, module_name, reason in orphan_modules:
            print(f"  - {pack_name} / {module_name}  -> {reason}")

    print("\nLecons orphelines / obsoletes :")
    if not orphan_lessons:
        print("  Aucun")
    else:
        for pack_name, module_name, lesson_name, reason in orphan_lessons:
            print(
                f"  - {pack_name} / {module_name} / {lesson_name}  -> {reason}"
            )


if __name__ == "__main__":
    main()
