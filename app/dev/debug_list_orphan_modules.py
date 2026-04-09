from pathlib import Path
from db import get_connection, list_packs, list_modules, list_lessons
from services.content_service import (
    get_content_root,
    build_pack_dir_name,
    get_expected_module_dir_names,
    get_expected_lesson_dir_names,
)

def main():
    root = get_content_root()
    print("CONTENT ROOT:", root)

    packs = list_packs()
    packs_by_dir = {}
    for pack in packs:
        code = pack["code"]
        dir_name = build_pack_dir_name(code)
        packs_by_dir[dir_name] = pack

    if not root.exists():
        print("Pas de content root.")
        return

    orphan_modules = []

    for pack_path in root.iterdir():
        if not pack_path.is_dir():
            continue

        pack_dir_name = pack_path.name
        if pack_dir_name not in packs_by_dir:
            continue  # pack orphelin, on s'en fout ici

        pack = packs_by_dir[pack_dir_name]
        pack_code = pack["code"]
        modules = list_modules(pack_code)

        expected_module_dirs = {}
        for module in modules:
            module_id = module["id"]
            module_title = module.get("title") or ""
            for name in get_expected_module_dir_names(module_id, module_title):
                expected_module_dirs[name] = module

        for module_path in pack_path.iterdir():
            if not module_path.is_dir():
                continue
            module_dir_name = module_path.name
            if module_dir_name not in expected_module_dirs:
                orphan_modules.append((pack_dir_name, module_dir_name))

    print("Modules orphelins détectés :")
    for pack_dir, module_dir in orphan_modules:
        print(f"- {pack_dir} / {module_dir}")

if __name__ == "__main__":
    main()
