import tempfile
import unittest

from services.school_system import SchoolSystem


class SchoolSystemTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.system = SchoolSystem(data_dir=self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def add_sample_student(self, student_id="S001", name="Mary Wanjiku"):
        return self.system.add_student(
            student_id,
            name,
            f"{student_id.lower()}@example.com",
            "0711111111",
        )

    def add_sample_course(self, course_id="PY101", capacity=2):
        return self.system.add_course(
            course_id,
            "Python Fundamentals",
            "Mr. Joseph",
            capacity,
        )

    def test_prevents_duplicate_student_ids(self):
        self.add_sample_student()

        with self.assertRaises(ValueError) as context:
            self.add_sample_student(name="Different Name")

        self.assertIn("already exists", str(context.exception))

    def test_prevents_duplicate_course_ids(self):
        self.add_sample_course()

        with self.assertRaises(ValueError) as context:
            self.add_sample_course(capacity=5)

        self.assertIn("already exists", str(context.exception))

    def test_prevents_duplicate_registrations(self):
        self.add_sample_student()
        self.add_sample_course()
        self.system.register_student("S001", "PY101")

        with self.assertRaises(ValueError) as context:
            self.system.register_student("S001", "PY101")

        self.assertIn("already registered", str(context.exception))

    def test_prevents_registration_when_course_is_full(self):
        self.add_sample_course(capacity=1)
        self.add_sample_student("S001", "Mary Wanjiku")
        self.add_sample_student("S002", "John Mwangi")
        self.system.register_student("S001", "PY101")

        with self.assertRaises(ValueError) as context:
            self.system.register_student("S002", "PY101")

        self.assertEqual(
            "Registration failed. This course is already full.",
            str(context.exception),
        )

    def test_saves_and_loads_data_from_json_files(self):
        self.add_sample_student()
        self.add_sample_course()
        self.system.register_student("S001", "PY101")
        self.system.save_data()

        loaded_system = SchoolSystem(data_dir=self.temp_dir.name)
        message = loaded_system.load_data()

        self.assertIn("Loaded 1 students, 1 courses, and 1 registrations", message)
        self.assertEqual(1, len(loaded_system.get_students_in_course("PY101")))
        self.assertEqual(1, len(loaded_system.get_courses_for_student("S001")))


if __name__ == "__main__":
    unittest.main()
