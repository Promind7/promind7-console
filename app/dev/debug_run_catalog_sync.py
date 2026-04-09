from db import get_connection
from services.catalog_sync_service import sync_internal_catalog_from_tutor

def main():
    conn = get_connection()
    try:
        print("Synchronisation du catalogue interne à partir de Tutor LMS...")
        sync_internal_catalog_from_tutor(conn=conn)
        print("OK.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
