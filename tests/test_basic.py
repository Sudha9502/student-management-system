import os
import tempfile
import json
import unittest

from student_mgmt import StudentManager

class TestStudentManager(unittest.TestCase):
    def setUp(self):
        # Use a temp file for tests to avoid clobbering real data.json
        self.tmpdir = tempfile.TemporaryDirectory()
        self.data_file = os.path.join(self.tmpdir.name, "data.json")
        self.mgr = StudentManager(data_file=self.data_file)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_add_and_find(self):
        self.mgr.add_student("101", "Alice", "A", "15")
        self.assertIsNotNone(self.mgr.find_by_roll("101"))
        self.assertEqual(self.mgr.find_by_roll("101")["name"], "Alice")

    def test_duplicate_roll(self):
        self.mgr.add_student("101", "Alice", "A")
        with self.assertRaises(ValueError):
            self.mgr.add_student("101", "Bob", "B")

    def test_update(self):
        self.mgr.add_student("101", "Alice", "A")
        ok = self.mgr.update_student("101", name="Alicia", grade="A+")
        self.assertTrue(ok)
        s = self.mgr.find_by_roll("101")
        self.assertEqual(s["name"], "Alicia")
        self.assertEqual(s["grade"], "A+")

    def test_delete(self):
        self.mgr.add_student("101", "Alice", "A")
        ok = self.mgr.delete_student("101")
        self.assertTrue(ok)
        self.assertIsNone(self.mgr.find_by_roll("101"))

    def test_persistence(self):
        self.mgr.add_student("101", "Alice", "A")
        self.mgr.save_data()
        # Load into a new manager
        m2 = StudentManager(data_file=self.data_file)
        self.assertIsNotNone(m2.find_by_roll("101"))

if __name__ == "__main__":
    unittest.main()
