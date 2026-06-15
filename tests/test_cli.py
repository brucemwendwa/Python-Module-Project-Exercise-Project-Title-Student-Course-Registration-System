import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from cli import main as cli_main


class CLITest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_cli(self, *args):
        stdout = StringIO()
        stderr = StringIO()
        command = ["--data-dir", self.temp_dir.name, *args]

        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = cli_main(command)

        return exit_code, stdout.getvalue(), stderr.getvalue()

    def add_sample_student(self):
        return self.run_cli(
            "add-student",
            "--student-id",
            "S001",
            "--name",
            "Mary Wanjiku",
            "--email",
            "mary@example.com",
            "--phone",
            "0711111111",
        )

    def add_sample_course(self):
        return self.run_cli(
            "add-course",
            "--course-id",
            "PY101",
            "--name",
            "Python Fundamentals",
            "--trainer",
            "Mr. Joseph",
            "--capacity",
            "2",
        )

    def test_cli_adds_and_lists_student(self):
        exit_code, output, error = self.add_sample_student()

        self.assertEqual(0, exit_code)
        self.assertEqual("", error)
        self.assertIn("Student Mary Wanjiku added successfully.", output)

        exit_code, output, error = self.run_cli("list-students")

        self.assertEqual(0, exit_code)
        self.assertEqual("", error)
        self.assertIn("S001", output)
        self.assertIn("Mary Wanjiku", output)

    def test_cli_registers_student_and_rejects_duplicate(self):
        self.add_sample_student()
        self.add_sample_course()

        exit_code, output, error = self.run_cli(
            "register",
            "--student-id",
            "S001",
            "--course-id",
            "PY101",
        )

        self.assertEqual(0, exit_code)
        self.assertEqual("", error)
        self.assertIn("successfully registered", output)

        exit_code, output, error = self.run_cli(
            "register",
            "--student-id",
            "S001",
            "--course-id",
            "PY101",
        )

        self.assertEqual(1, exit_code)
        self.assertIn("already registered", output + error)

    def test_cli_returns_error_for_missing_course(self):
        self.add_sample_student()

        exit_code, output, error = self.run_cli(
            "register",
            "--student-id",
            "S001",
            "--course-id",
            "MISSING",
        )

        self.assertEqual(1, exit_code)
        self.assertIn("Course not found", output + error)


if __name__ == "__main__":
    unittest.main()
