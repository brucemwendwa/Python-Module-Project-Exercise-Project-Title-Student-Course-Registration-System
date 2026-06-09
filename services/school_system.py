import json
from pathlib import Path

from models.course import Course
from models.registration import Registration
from models.student import Student


class SchoolSystem:
    """Manages students, courses, registrations, and JSON file storage."""

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.students_file = self.data_dir / "students.json"
        self.courses_file = self.data_dir / "courses.json"
        self.registrations_file = self.data_dir / "registrations.json"
        self.students = {}
        self.courses = {}
        self.registrations = []

    def add_student(self, student_id, name, email, phone_number):
        student = Student(student_id, name, email, phone_number)
        if student.student_id in self.students:
            raise ValueError(f"Student ID {student.student_id} already exists.")

        self.students[student.student_id] = student
        return student

    def get_all_students(self):
        return list(self.students.values())

    def search_students(self, search_term):
        search_term = str(search_term).strip()
        if not search_term:
            raise ValueError("Search term cannot be empty.")

        return [student for student in self.students.values() if student.matches(search_term)]

    def add_course(self, course_id, course_name, trainer_name, capacity):
        course = Course(course_id, course_name, trainer_name, capacity)
        if course.course_id in self.courses:
            raise ValueError(f"Course ID {course.course_id} already exists.")

        self.courses[course.course_id] = course
        return course

    def get_all_courses(self):
        return list(self.courses.values())

    def register_student(self, student_id, course_id):
        student_id = str(student_id).strip()
        course_id = str(course_id).strip()

        student = self.students.get(student_id)
        if student is None:
            raise ValueError("Student not found.")

        course = self.courses.get(course_id)
        if course is None:
            raise ValueError("Course not found.")

        if self.is_registered(student_id, course_id):
            raise ValueError(f"{student.name} is already registered for this course.")

        if self.is_course_full(course_id):
            raise ValueError("Registration failed. This course is already full.")

        self.registrations.append(Registration(student_id, course_id))
        return f"{student.name} successfully registered for {course.course_name}."

    def is_registered(self, student_id, course_id):
        return any(
            registration.has_same_pair(student_id, course_id)
            for registration in self.registrations
        )

    def course_registration_count(self, course_id):
        return sum(
            1
            for registration in self.registrations
            if registration.course_id == course_id
        )

    def is_course_full(self, course_id):
        course = self.courses.get(str(course_id).strip())
        if course is None:
            raise ValueError("Course not found.")
        return self.course_registration_count(course.course_id) >= course.capacity

    def get_students_in_course(self, course_id):
        course_id = str(course_id).strip()
        if course_id not in self.courses:
            raise ValueError("Course not found.")

        return [
            self.students[registration.student_id]
            for registration in self.registrations
            if registration.course_id == course_id
            and registration.student_id in self.students
        ]

    def get_courses_for_student(self, student_id):
        student_id = str(student_id).strip()
        if student_id not in self.students:
            raise ValueError("Student not found.")

        return [
            self.courses[registration.course_id]
            for registration in self.registrations
            if registration.student_id == student_id
            and registration.course_id in self.courses
        ]

    def save_data(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._write_json(self.students_file, [student.to_dict() for student in self.students.values()])
        self._write_json(self.courses_file, [course.to_dict() for course in self.courses.values()])
        self._write_json(
            self.registrations_file,
            [registration.to_dict() for registration in self.registrations],
        )
        return "Data saved successfully."

    def load_data(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)

        loaded_students = {}
        loaded_courses = {}
        loaded_registrations = []
        skipped_items = 0

        for student_data in self._read_json_collection(self.students_file):
            try:
                student = Student.from_dict(student_data)
            except ValueError:
                skipped_items += 1
                continue
            if student.student_id in loaded_students:
                skipped_items += 1
                continue
            loaded_students[student.student_id] = student

        for course_data in self._read_json_collection(self.courses_file):
            try:
                course = Course.from_dict(course_data)
            except ValueError:
                skipped_items += 1
                continue
            if course.course_id in loaded_courses:
                skipped_items += 1
                continue
            loaded_courses[course.course_id] = course

        for registration_data in self._read_json_collection(self.registrations_file):
            try:
                registration = Registration.from_dict(registration_data)
            except ValueError:
                skipped_items += 1
                continue

            duplicate = any(
                existing_registration.has_same_pair(
                    registration.student_id,
                    registration.course_id,
                )
                for existing_registration in loaded_registrations
            )
            if (
                duplicate
                or registration.student_id not in loaded_students
                or registration.course_id not in loaded_courses
            ):
                skipped_items += 1
                continue

            course = loaded_courses[registration.course_id]
            current_count = sum(
                1
                for existing_registration in loaded_registrations
                if existing_registration.course_id == registration.course_id
            )
            if current_count >= course.capacity:
                skipped_items += 1
                continue

            loaded_registrations.append(registration)

        self.students = loaded_students
        self.courses = loaded_courses
        self.registrations = loaded_registrations

        message = (
            f"Loaded {len(self.students)} students, "
            f"{len(self.courses)} courses, and "
            f"{len(self.registrations)} registrations."
        )
        if skipped_items:
            message += f" Skipped {skipped_items} invalid or duplicate records."
        return message

    def _read_json_collection(self, file_path):
        if not file_path.exists():
            return []

        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{file_path.name} contains invalid JSON.") from exc

        if not isinstance(data, list):
            raise ValueError(f"{file_path.name} must contain a JSON list.")

        return data

    @staticmethod
    def _write_json(file_path, data):
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
