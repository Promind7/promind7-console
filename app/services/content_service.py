import os
import shutil
import unicodedata
import re
from pathlib import Path
from typing import Optional

from db import get_connection
from services.log_service import log_info, log_warn, log_error


def get_content_root() -> Path:
    """
    Retourne le dossier racine du contenu local Tutor LMS.
    """
    root = Path(os.getenv("PROMIND7_CONTENT_ROOT", "content"))
    root.mkdir(parents=True, exist_ok=True)
    return root


def slugify(value: str) -> str:
    """
    Transforme un titre Tutor LMS en slug de dossier :

    Exemple :
        "Module 1 – Comprendre le marché de l'emploi"
    -> "module_1_comprendre_le_marche_de_l_emploi"
    """
    if not value:
        return ""
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = value.strip("_")
    return value


def build_pack_dir_name(course_tutor_id: int, course_title: str) -> str:
    """
    Dossier pour un cours (pack) Tutor LMS.

    Règle :
        <slug(titre cours)>__<course_tutor_id>
    Exemple :
        "Pack 0 -- Fondations & Prise de conscience"
    -> "pack_0_fondations_prise_de_conscience__29140"
    """
    slug = slugify(course_title)
    if slug:
        return f"{slug}__{course_tutor_id}"
    return str(course_tutor_id)


def build_module_dir_name(module_tutor_id: int, module_title: str) -> str:
    """
    Dossier pour un module Tutor LMS.

    Règle :
        <slug(titre module)>__<module_tutor_id>
    Exemple :
        "Module 1 – Comprendre le marché de l'emploi"
    -> "module_1_comprendre_le_marche_de_l_emploi__123"
    """
    slug = slugify(module_title)
    if slug:
        return f"{slug}__{module_tutor_id}"
    return str(module_tutor_id)


def build_lesson_dir_name(lesson_tutor_id: int, lesson_title: str) -> str:
    """
    Dossier pour une leçon Tutor LMS.

    Règle :
        <slug(titre lecon)>__<lesson_tutor_id>
    Exemple :
        "Leçon 1 – Introduction à Promind7"
    -> "lecon_1_introduction_a_promind7__456"
    """
    slug = slugify(lesson_title)
    if slug:
        return f"{slug}__{lesson_tutor_id}"
    return str(lesson_tutor_id)


def extract_id_from_name(name: str) -> Optional[int]:
    """
    Extrait l'ID à partir d'un nom de dossier du type :
        "<slug>__<id>"
    Peu importe ce qui suit : "__42", "__42 - copie", "__42_old".
    """
    if "__" not in name:
        return None
    _, tail = name.split("__", 1)
    # On prend uniquement la première séquence numérique
    m = re.match(r"(\d+)", tail)
    if not m:
        return None
    return int(m.group(1))


def _ensure_folder(parent_dir: Path, target_name: str, tutor_id: int) -> Path:
    """
    Assure l'existence du dossier avec le bon nom.
    Si un dossier avec le même ID existe déjà mais avec un nom différent, il est renommé.
    Cela préserve le contenu.
    """
    target_path = parent_dir / target_name
    
    # Si le dossier cible exact existe déjà, c'est parfait
    if target_path.exists():
        return target_path

    # Sinon, on cherche s'il existe un dossier avec le même ID
    suffix = f"__{tutor_id}"
    candidate = None
    
    if parent_dir.exists():
        for item in parent_dir.iterdir():
            if item.is_dir() and item.name.endswith(suffix):
                candidate = item
                break
    
    if candidate:
        # On a trouvé un dossier avec le même ID (vieux nom)
        try:
            candidate.rename(target_path)
            log_info(f"Renamed folder: {candidate.name} -> {target_path.name}")
            return target_path
        except Exception as e:
            log_error(f"Failed to rename {candidate} to {target_path}: {e}")
            # Fallback: on retourne l'ancien si on peut pas renommer (ex: fichier ouvert)
            return candidate

    # Si rien trouvé, on crée
    target_path.mkdir(parents=True, exist_ok=True)
    log_info(f"Created folder: {target_path}")
    return target_path


def get_pack_dir(course_tutor_id: int, course_title: str) -> Path:
    root = get_content_root() / "packs"
    root.mkdir(parents=True, exist_ok=True)
    dir_name = build_pack_dir_name(course_tutor_id, course_title)
    return _ensure_folder(root, dir_name, course_tutor_id)


def get_module_dir(
    course_tutor_id: int,
    course_title: str,
    module_tutor_id: int,
    module_title: str,
) -> Path:
    pack_dir = get_pack_dir(course_tutor_id, course_title)
    dir_name = build_module_dir_name(module_tutor_id, module_title)
    return _ensure_folder(pack_dir, dir_name, module_tutor_id)


def get_lesson_dir(
    course_tutor_id: int,
    course_title: str,
    module_tutor_id: int,
    module_title: str,
    lesson_tutor_id: int,
    lesson_title: str,
) -> Path:
    module_dir = get_module_dir(course_tutor_id, course_title, module_tutor_id, module_title)
    dir_name = build_lesson_dir_name(lesson_tutor_id, lesson_title)
    return _ensure_folder(module_dir, dir_name, lesson_tutor_id)


def sync_content_folders_from_tutor() -> None:
    """
    Synchronise l'arborescence content/ à partir des tables tutor_courses,
    tutor_modules et tutor_lessons.

    - Crée les dossiers :
        content/<slug(titre cours)>__<course_tutor_id>/
        content/.../<slug(titre module)>__<module_tutor_id>/
        content/.../<slug(titre lecon)>__<lesson_tutor_id>/
    - Ne supprime rien (le nettoyage est géré par cleanup_orphan_content_folders).
    """
    conn = get_connection()
    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT tutor_id, title
            FROM tutor_courses
            ORDER BY tutor_id;
            """
        )
        courses = cur.fetchall()

        for course in courses:
            course_tutor_id = course["tutor_id"]
            course_title = course["title"] or f"Cours {course_tutor_id}"

            pack_dir = get_pack_dir(course_tutor_id, course_title)

            cur.execute(
                """
                SELECT tutor_id, title
                FROM tutor_modules
                WHERE course_tutor_id = ?
                ORDER BY order_index, tutor_id;
                """,
                (course_tutor_id,),
            )
            modules = cur.fetchall()

            for module in modules:
                module_tutor_id = module["tutor_id"]
                module_title = module["title"] or f"Module {module_tutor_id}"

                module_dir = get_module_dir(
                    course_tutor_id,
                    course_title,
                    module_tutor_id,
                    module_title,
                )

                cur.execute(
                    """
                    SELECT tutor_id, title
                    FROM tutor_lessons
                    WHERE module_tutor_id = ?
                    ORDER BY order_index, tutor_id;
                    """,
                    (module_tutor_id,),
                )
                lessons = cur.fetchall()

                for lesson in lessons:
                    lesson_tutor_id = lesson["tutor_id"]
                    lesson_title = lesson["title"] or f"Lecon {lesson_tutor_id}"

                    get_lesson_dir(
                        course_tutor_id,
                        course_title,
                        module_tutor_id,
                        module_title,
                        lesson_tutor_id,
                        lesson_title,
                    )
    finally:
        conn.close()


def sync_content_folders_from_db() -> None:
    """
    Compatibilité arrière : redirige vers sync_content_folders_from_tutor().
    """
    sync_content_folders_from_tutor()


def cleanup_orphan_content_folders(dry_run: bool = False) -> dict:
    """
    Supprime les dossiers de packs/modules/leçons dont l'ID tutor_id
    n'existe plus dans les tables tutor_courses / tutor_modules / tutor_lessons.

    Convention des noms de dossiers :
        <slug(titre)>__<id>

    dry_run = True : ne supprime rien, retourne uniquement les compteurs.
    """
    root = get_content_root()
    stats = {
        "removed_packs": 0,
        "removed_modules": 0,
        "removed_lessons": 0,
        "dry_run": dry_run,
    }

    if not root.exists():
        return stats

    official_names = {}

    conn = get_connection()
    try:
        cur = conn.cursor()

        cur.execute("SELECT tutor_id FROM tutor_courses;")
        valid_course_ids = {row["tutor_id"] for row in cur.fetchall()}

        cur.execute("SELECT tutor_id FROM tutor_modules;")
        valid_module_ids = {row["tutor_id"] for row in cur.fetchall()}

        cur.execute("SELECT tutor_id FROM tutor_lessons;")
        valid_lesson_ids = {row["tutor_id"] for row in cur.fetchall()}

        # Pour chaque ID, on garde le nom officiel issu du titre Tutor LMS
        official_names = {}

        # Construire la map des slugs officiels pour packs
        cur.execute("SELECT tutor_id, title FROM tutor_courses;")
        for row in cur.fetchall():
            official_names[row["tutor_id"]] = build_pack_dir_name(row["tutor_id"], row["title"] or "")

        # Modules
        cur.execute("SELECT tutor_id, title FROM tutor_modules;")
        for row in cur.fetchall():
            official_names[row["tutor_id"]] = build_module_dir_name(row["tutor_id"], row["title"] or "")

        # Leçons
        cur.execute("SELECT tutor_id, title FROM tutor_lessons;")
        for row in cur.fetchall():
            official_names[row["tutor_id"]] = build_lesson_dir_name(row["tutor_id"], row["title"] or "")
    finally:
        conn.close()

    for pack_path in root.iterdir():
        if not pack_path.is_dir():
            continue

        course_id = extract_id_from_name(pack_path.name)
        if course_id is None:
            continue

        official = official_names.get(course_id)
        if official and pack_path.name != official:
            if not dry_run:
                shutil.rmtree(pack_path, ignore_errors=True)
            stats["removed_packs"] += 1
            continue

        if course_id not in valid_course_ids:
            if not dry_run:
                shutil.rmtree(pack_path, ignore_errors=True)
            stats["removed_packs"] += 1
            continue

        for module_path in pack_path.iterdir():
            if not module_path.is_dir():
                continue

            module_id = extract_id_from_name(module_path.name)
            if module_id is None:
                continue

            official = official_names.get(module_id)
            if official and module_path.name != official:
                if not dry_run:
                    shutil.rmtree(module_path, ignore_errors=True)
                stats["removed_modules"] += 1
                continue

            if module_id not in valid_module_ids:
                if not dry_run:
                    shutil.rmtree(module_path, ignore_errors=True)
                stats["removed_modules"] += 1
                continue

            for lesson_path in module_path.iterdir():
                if not lesson_path.is_dir():
                    continue

                lesson_id = extract_id_from_name(lesson_path.name)
                if lesson_id is None:
                    continue

                official = official_names.get(lesson_id)
                if official and lesson_path.name != official:
                    if not dry_run:
                        shutil.rmtree(lesson_path, ignore_errors=True)
                    stats["removed_lessons"] += 1
                    continue

                if lesson_id not in valid_lesson_ids:
                    if not dry_run:
                        shutil.rmtree(lesson_path, ignore_errors=True)
                    stats["removed_lessons"] += 1

    return stats
