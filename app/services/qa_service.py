import os
from pathlib import Path
from typing import List, Dict, Any
import datetime

from services.tutor_lms_service import get_all_courses, get_modules_for_course
from services.content_service import get_pack_dir, build_pack_dir_name

def perform_global_audit() -> List[Dict[str, Any]]:
    """
    Scanne tous les packs et vérifie leur intégrité (FS + SQL).
    Retourne une liste de dicts pour l'affichage en tableau.
    """
    courses = get_all_courses()
    report = []
    
    for c in courses:
        pack_status = {
            "Pack ID": c["tutor_id"],
            "Pack Title": c["title"],
            "Status": "✅ OK",
            "Path Status": "✅ Exists",
            "Master File": "✅ Found",
            "Modules (SQL)": 0,
            "Linked .txt": 0,
            "Issues": []
        }
        
        # 1. SQL Check
        modules = get_modules_for_course(c["tutor_id"])
        pack_status["Modules (SQL)"] = len(modules)
        
        # 2. Path Check
        pack_dir = get_pack_dir(c["tutor_id"], c["title"])
        if not pack_dir.exists():
            pack_status["Path Status"] = "❌ Missing"
            pack_status["Status"] = "🚫 BROKEN"
            pack_status["Issues"].append("Dossier manquant")
        else:
            # 3. Master File Check
            # Reconstruct expected name logic or glob
            # Logique actuelle : "MASTER_CONTENT_[slug].md" where slug is usually partial pack dir name or generic.
            # Best check: ANY MASTER_CONTENT file.
            masters = list(pack_dir.glob("MASTER_CONTENT_*.md"))
            if not masters:
                pack_status["Master File"] = "❌ Missing"
                pack_status["Status"] = "⚠️ WARNING"
                pack_status["Issues"].append("Master File manquant")
            
            # 4. Content Scan
            txt_files = list(pack_dir.glob("*.txt"))
            pack_status["Linked .txt"] = len(txt_files)
            
        report.append(pack_status)
        
    return report


def scan_root_content_files() -> List[str]:
    """Retourne la liste des fichiers .txt/.md orphelins ou en attente dans /content"""
    root = Path("content")
    if not root.exists():
        return []
        
    files = [f.name for f in root.glob("*") if f.is_file() and f.suffix in ['.txt', '.md', '.docx']]
    return files


def fix_missing_masters(pack_ids: List[int]) -> List[str]:
    """
    Crée les fichiers Master manquants pour les IDs donnés.
    """
    logs = []
    all_courses = {c["tutor_id"]: c for c in get_all_courses()}
    
    for pid in pack_ids:
        if pid not in all_courses:
            continue
            
        c = all_courses[pid]
        pack_dir = get_pack_dir(c["tutor_id"], c["title"])
        
        # Check again to be safe
        if list(pack_dir.glob("MASTER_CONTENT_*.md")):
            logs.append(f"Skipped {c['title']} (Master existe déjà)")
            continue
            
        # Create
        slug = build_pack_dir_name(c["tutor_id"], c["title"]).split("__")[0]
        master_file = pack_dir / f"MASTER_CONTENT_{slug}.md"
        
        content = f"""# PACK : {c['title']}

**Statut :** Initialisé par QA Audit le {datetime.date.today()}

## 🧠 Boîte à Idées du Pack

*(Section initialisée automatiquement)*
"""
        master_file.write_text(content, encoding="utf-8")
        logs.append(f"✅ Created Master for : {c['title']}")
        
    return logs
