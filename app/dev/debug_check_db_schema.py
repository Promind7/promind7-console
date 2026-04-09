
import sqlite3
from db.connection import get_db_path

def check():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    print("--- TABLES ---")
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall()]
    print(tables)
    
    if "packs" in tables:
        print("\n--- PACKS LIMIT 5 ---")
        cur.execute("SELECT code, title, tutor_course_id FROM packs LIMIT 5;")
        for r in cur.fetchall():
            print(r)
            
    if "courses" in tables:
        print("\n--- COURSES LIMIT 5 ---")
        cur.execute("SELECT * FROM courses LIMIT 5;")
        for r in cur.fetchall():
            print(r)
    else:
        print("\n--- NO 'courses' TABLE ---")

    if "tutor_courses" in tables:
        print("\n--- TUTOR_COURSES LIMIT 5 ---")
        cur.execute("SELECT tutor_id, title FROM tutor_courses LIMIT 5;")
        for r in cur.fetchall():
            print(r)

    conn.close()

if __name__ == "__main__":
    check()
