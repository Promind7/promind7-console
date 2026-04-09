
import unittest
import sys
import os
import sqlite3

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set test DB to memory BEFORE importing anything that might use it (though get_connection reads env at runtime)
os.environ["PROMIND7_DB_PATH"] = ":memory:"

from db.schema import init_db
from db.connection import get_connection
from db.queries.students import list_students, upsert_student_from_tutor
from db.queries.tasks import add_task, list_tasks, update_task_status
from db.queries.stats import count_students
import consts

class TestDBQueries(unittest.TestCase):

    def setUp(self):
        # Initialize DB schema in memory
        init_db()

    def tearDown(self):
        # In-memory DB is separate per connection usually, 
        # but if get_connection creates new connections to :memory:, 
        # they are distinct unless we share valid uri.
        # Wait, sqlite3.connect(":memory:") creates a fresh one each time unless shared cache is used.
        # The schema uses get_connection().
        # If I want to test persistence across calls (add_task -> list_tasks), 
        # I need a persistent DB for the duration of the test.
        # :memory: is tricky with our pattern of opening/closing connections in each query.
        # SOLUTION: Use a temporary file.
        pass

    @classmethod
    def setUpClass(cls):
        # Use a temporary file for the whole class or session
        cls.test_db = "test_promind7.db"
        os.environ["PROMIND7_DB_PATH"] = cls.test_db
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
        
        # Initialize Once
        init_db()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db):
            # Close any lingering connections if possible, though our code closes them.
            try:
                os.remove(cls.test_db)
            except PermissionError:
                pass # Might be open

    def test_student_workflow(self):
        # 1. Start with 0 students
        self.assertEqual(count_students(), 0)
        
        # 2. Add student via upsert (Tutor LMS import simulation)
        upsert_student_from_tutor("Jean Test", "jean@test.com", "jeanT")
        
        # 3. Check count
        self.assertEqual(count_students(), 1)
        
        # 4. List and verify
        students = list_students()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]['name'], "Jean Test")

    def test_task_workflow(self):
        # 1. Add Task
        add_task(
            title="Test Task",
            description="Unit Test Description",
            priority="High",
            due_date="2025-01-01",
            pack_code="P1",
            module_id=None,
            lesson_id=None,
            quiz_id=None
        )
        
        # 2. List Tasks
        tasks = list_tasks(include_done=True)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['title'], "Test Task")
        self.assertEqual(tasks[0]['status'], consts.TASK_STATUS_TODO)
        
        # 3. Update Status
        task_id = tasks[0]['id']
        update_task_status(task_id, consts.TASK_STATUS_DONE)
        
        # 4. List (default hides done)
        tasks_active = list_tasks(include_done=False)
        self.assertEqual(len(tasks_active), 0)
        
        # 5. List all (shows done)
        tasks_all = list_tasks(include_done=True)
        self.assertEqual(len(tasks_all), 1)
        self.assertEqual(tasks_all[0]['status'], consts.TASK_STATUS_DONE)

if __name__ == '__main__':
    unittest.main()
