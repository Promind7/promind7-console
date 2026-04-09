import os
import sys
import json
from pathlib import Path

_app = Path(__file__).resolve().parent
_repo = _app.parent
for _p in (_app, _repo):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from db import (
    init_db,
    get_connection,
    upsert_tutor_course_from_export,
    upsert_tutor_module_from_export,
    upsert_tutor_lesson_from_export,
    prune_tutor_mirror_to_imported_course_ids,
    sync_learners_from_tutor_enrollments_mirror,
)
from services.content_service import sync_content_folders_from_db


def _clear_tutor_enrollments_for_course(course_tutor_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM tutor_enrollments WHERE course_tutor_id = ?;",
        (course_tutor_id,),
    )
    conn.commit()
    conn.close()


def _save_enrollments_for_course(course_tutor_id: int, enroll_list):
    """
    Insère / remplace les lignes brutes dans tutor_enrollments pour un cours.
    La table interne students/enrollments est reconstruite en fin d'import global
    (sync_learners_from_tutor_enrollments_mirror) pour rester alignée sur le miroir.
    """
    if not enroll_list:
        _clear_tutor_enrollments_for_course(course_tutor_id)
        return 0

    rows_to_insert = []

    for e in enroll_list:
        if not isinstance(e, dict):
            continue

        enrollment = e.get("enrollment") or {}
        student = e.get("student") or None

        enrolled_at = (
            enrollment.get("post_date")
            or enrollment.get("post_date_gmt")
            or enrollment.get("post_modified")
        )
        status = enrollment.get("post_status")

        student_name = None
        student_email = None
        student_username = None

        if isinstance(student, dict) and student:
            sdata = student.get("data") or student

            student_name = (
                sdata.get("display_name")
                or sdata.get("user_nicename")
                or sdata.get("user_login")
            )
            student_email = sdata.get("user_email")
            student_username = sdata.get("user_login")

        if not student_name:
            author_id = enrollment.get("post_author")
            if author_id is not None:
                student_username = student_username or str(author_id)
                student_name = f"User #{author_id}"

        raw_json = json.dumps(e, ensure_ascii=False)

        # Miroir ProMind7 = export Tutor : toute inscription avec identité exploitable
        # (email et/ou nom) alimente students + enrollments — pas seulement « terminé + email »,
        # pour que local, Cloud et dépôt Git reflètent le même export après réimport.
        if student_email:
            student_email = str(student_email).strip() or None
        if student_name:
            student_name = str(student_name).strip() or None
        # students / enrollments : voir sync_learners_from_tutor_enrollments_mirror()

        # Ligne brute dans tutor_enrollments
        rows_to_insert.append(
            (
                course_tutor_id,
                student_name,
                student_email,
                student_username,
                enrolled_at,
                status,
                raw_json,
            )
        )

    if not rows_to_insert:
        _clear_tutor_enrollments_for_course(course_tutor_id)
        return 0

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tutor_enrollments WHERE course_tutor_id = ?;",
        (course_tutor_id,),
    )

    for params in rows_to_insert:
        cur.execute(
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
            params,
        )

    conn.commit()
    conn.close()

    return len(rows_to_insert)


def import_from_zip_folder(export_root: str):
    """
    Parcourt un dossier d'export Tutor LMS décompressé et remplit la base locale.
    export_root doit contenir un sous-dossier 'courses'.
    """
    print("=== DÉMARRAGE IMPORT TUTOR LMS ===")
    print(f"- Dossier racine export : {export_root}")

    init_db()

    courses_dir = os.path.join(export_root, "courses")
    if not os.path.isdir(courses_dir):
        print(f"[ERREUR] Dossier 'courses' introuvable dans : {export_root}")
        return 0, 0, 0

    total_courses = 0
    total_modules = 0
    total_lessons = 0
    total_enrollments = 0
    imported_course_tutor_ids: set[int] = set()

    for entry in os.listdir(courses_dir):
        course_folder = os.path.join(courses_dir, entry)
        if not os.path.isdir(course_folder):
            continue

        main_json_path = os.path.join(course_folder, f"{entry}.json")
        if not os.path.isfile(main_json_path):
            continue

        print(f"\n--> Cours dossier {entry}")
        print(f"    Fichier cours : {main_json_path}")

        # Lecture du fichier cours
        try:
            with open(main_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"    [WARN] Impossible de lire {main_json_path} : {e}")
            continue

        try:
            blocks = data.get("data") or []
            course_block = None
            for b in blocks:
                if b.get("content_type") == "courses":
                    course_block = b
                    break

            if course_block is None:
                print(f"    [WARN] Aucun bloc 'courses' dans {main_json_path}")
                continue

            course_obj = course_block["data"]["course"]
        except Exception as e:
            print(f"    [WARN] Format inattendu dans {main_json_path} : {e}")
            continue

        try:
            course_tutor_id = int(course_obj.get("ID"))
        except (TypeError, ValueError):
            print("    [WARN] Cours sans ID numérique valide, ignoré")
            continue

        # 1) Upsert du cours
        upsert_tutor_course_from_export(course_obj)
        imported_course_tutor_ids.add(course_tutor_id)
        total_courses += 1

        print(f"    [OK] Cours importé : {course_obj.get('post_title')} (ID={course_tutor_id})")

        # 2) Modules + leçons
        contents = course_obj.get("contents") or []
        print(f"    - Modules trouvés : {len(contents)}")

        for module in contents:
            module_tutor_id = module.get("ID")
            if module_tutor_id is None:
                print("      [WARN] Module sans ID, ignoré")
                continue

            upsert_tutor_module_from_export(module, course_tutor_id)
            total_modules += 1
            print(f"      [OK] Module : {module.get('post_title')}")

            children = module.get("children") or []
            print(f"      - Leçons dans ce module : {len(children)}")

            for lesson in children:
                upsert_tutor_lesson_from_export(
                    lesson,
                    course_tutor_id=course_tutor_id,
                    module_tutor_id=module_tutor_id,
                )
                total_lessons += 1

        # 3) Inscriptions (enrollments.json)
        enroll_path = os.path.join(course_folder, "enrollments.json")
        if os.path.isfile(enroll_path):
            print(f"    Fichier enrollments : {enroll_path}")
            try:
                with open(enroll_path, "r", encoding="utf-8") as f:
                    enroll_data = json.load(f)
            except Exception as e:
                print(f"    [WARN] Impossible de lire {enroll_path} : {e}")
                enroll_data = None

            if enroll_data:
                try:
                    blocks = enroll_data.get("data") or []
                    enroll_list = None
                    for b in blocks:
                        data_block = b.get("data") or {}
                        if isinstance(data_block, dict) and "enrollments" in data_block:
                            enroll_list = data_block["enrollments"]
                            break

                    if isinstance(enroll_list, list):
                        imported = _save_enrollments_for_course(course_tutor_id, enroll_list)
                        total_enrollments += imported
                        print(f"    [OK] Inscriptions enregistrées : {imported}")
                    else:
                        print("    (Aucune inscription dans ce fichier enrollments.json)")
                        _clear_tutor_enrollments_for_course(course_tutor_id)
                except Exception as e:
                    print(f"    [WARN] Problème de parsing enrollments.json : {e}")
        else:
            print("    (Pas de fichier enrollments.json pour ce cours)")
            _clear_tutor_enrollments_for_course(course_tutor_id)

    if imported_course_tutor_ids:
        pr = prune_tutor_mirror_to_imported_course_ids(imported_course_tutor_ids)
        if not pr["skipped"] and (
            pr["removed_courses"]
            or pr["removed_modules"]
            or pr["removed_lessons"]
            or pr["removed_enrollments"]
        ):
            print(
                "\n[prune] Cours Tutor absents du dossier export : supprimés de la base — "
                f"{pr['removed_courses']} cours, {pr['removed_modules']} modules, "
                f"{pr['removed_lessons']} leçons, {pr['removed_enrollments']} lignes tutor_enrollments."
            )

    # Alignement strict apprenants / inscriptions internes sur tutor_enrollments
    try:
        print("[learners] Synchronisation students + enrollments depuis tutor_enrollments…")
        sync_learners_from_tutor_enrollments_mirror()
    except Exception as e:
        print(f"[learners] [WARN] Synchronisation apprenants : {e}")

    print("\n=== IMPORT TERMINÉ ===")
    print(f"- Cours       : {total_courses}")
    print(f"- Modules     : {total_modules}")
    print(f"- Leçons      : {total_lessons}")
    print(f"- Inscriptions: {total_enrollments}")

    # Synchronisation des dossiers de contenu (packs/modules/leçons)
    try:
        print("[content] Synchronisation des dossiers de contenu à partir de la base...")
        sync_content_folders_from_db()
    except Exception as e:
        # On ne casse pas l'import en cas d'erreur de contenu,
        # on affiche seulement un avertissement.
        print(f"[content] [WARN] Erreur lors de la synchronisation des dossiers de contenu : {e}")

    return total_courses, total_modules, total_lessons


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Utilisation : python import_tutor_from_zip.py <chemin_dossier_export>")
        print("Exemple : python app/import_tutor_from_zip.py D:\\Promind7\\IA\\V2\\tutor_lms")
        sys.exit(1)

    export_root = sys.argv[1]
    if not os.path.isdir(export_root):
        print(f"âŒ Dossier inexistant : {export_root}")
        sys.exit(1)

    import_from_zip_folder(export_root)



