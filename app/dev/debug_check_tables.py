from db import get_connection

def main():
    conn = get_connection()
    cur = conn.cursor()

    tables = ["packs", "modules", "lessons", "tutor_courses", "tutor_modules", "tutor_lessons"]

    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table};")
        count = cur.fetchone()[0]
        print(f"{table}: {count}")

    conn.close()

if __name__ == "__main__":
    main()
