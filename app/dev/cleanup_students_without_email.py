from db import get_connection

def cleanup_students_without_email():
    conn = get_connection()
    cur = conn.cursor()

    # Supprimer d'abord les enrollments liés à des étudiants sans email
    cur.execute("""
        DELETE FROM enrollments
        WHERE student_id IN (
            SELECT id FROM students
            WHERE email IS NULL OR TRIM(email) = ''
        );
    """)

    # Puis supprimer les étudiants sans email
    cur.execute("""
        DELETE FROM students
        WHERE email IS NULL OR TRIM(email) = '';
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    cleanup_students_without_email()
    print("Nettoyage terminé : étudiants sans email supprimés.")
