import argparse
import os

from services.school_system import SchoolSystem
from utils.console_output import (
    print_courses,
    print_error,
    print_info,
    print_students,
    print_success,
)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Manage students, courses, and course registrations.",
    )
    parser.add_argument(
        "--data-dir",
        default=os.environ.get("SCHOOL_DATA_DIR", "data"),
        help="Folder used for students.json, courses.json, and registrations.json.",
    )

    subcommands = parser.add_subparsers(dest="command", required=True)

    add_student = subcommands.add_parser("add-student", help="Add a new student.")
    add_student.add_argument("--student-id", required=True, help="Unique student ID.")
    add_student.add_argument("--name", required=True, help="Student full name.")
    add_student.add_argument("--email", required=True, help="Student email address.")
    add_student.add_argument("--phone", required=True, help="Student phone number.")

    subcommands.add_parser("list-students", help="View all students.")

    search_student = subcommands.add_parser(
        "search-student",
        help="Search students by ID or name.",
    )
    search_student.add_argument("term", help="Student ID or name to search for.")

    add_course = subcommands.add_parser("add-course", help="Add a new course.")
    add_course.add_argument("--course-id", required=True, help="Unique course ID.")
    add_course.add_argument("--name", required=True, help="Course name.")
    add_course.add_argument("--trainer", required=True, help="Trainer name.")
    add_course.add_argument(
        "--capacity",
        required=True,
        type=int,
        help="Maximum number of students allowed in the course.",
    )

    subcommands.add_parser("list-courses", help="View all courses.")

    register = subcommands.add_parser(
        "register",
        help="Register a student to a course.",
    )
    register.add_argument("--student-id", required=True, help="Existing student ID.")
    register.add_argument("--course-id", required=True, help="Existing course ID.")

    students_in_course = subcommands.add_parser(
        "students-in-course",
        help="View students registered in a course.",
    )
    students_in_course.add_argument("--course-id", required=True, help="Course ID.")

    courses_for_student = subcommands.add_parser(
        "courses-for-student",
        help="View courses registered by a student.",
    )
    courses_for_student.add_argument("--student-id", required=True, help="Student ID.")

    subcommands.add_parser("save", help="Save current JSON data.")
    subcommands.add_parser("load", help="Load and summarize current JSON data.")

    return parser


def run_command(args):
    system = SchoolSystem(args.data_dir)
    load_message = system.load_data()

    if args.command == "add-student":
        student = system.add_student(
            args.student_id,
            args.name,
            args.email,
            args.phone,
        )
        system.save_data()
        print_success(f"Student {student.name} added successfully.")
        return 0

    if args.command == "list-students":
        print_students(system.get_all_students())
        return 0

    if args.command == "search-student":
        print_students(system.search_students(args.term))
        return 0

    if args.command == "add-course":
        course = system.add_course(
            args.course_id,
            args.name,
            args.trainer,
            args.capacity,
        )
        system.save_data()
        print_success(f"Course {course.course_name} added successfully.")
        return 0

    if args.command == "list-courses":
        print_courses(system, system.get_all_courses())
        return 0

    if args.command == "register":
        message = system.register_student(args.student_id, args.course_id)
        system.save_data()
        print_success(message)
        return 0

    if args.command == "students-in-course":
        students = system.get_students_in_course(args.course_id)
        print_students(students)
        return 0

    if args.command == "courses-for-student":
        courses = system.get_courses_for_student(args.student_id)
        print_courses(system, courses)
        return 0

    if args.command == "save":
        print_success(system.save_data())
        return 0

    if args.command == "load":
        print_info(load_message)
        return 0

    print_error("Unknown command.")
    return 1


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return run_command(args)
    except ValueError as error:
        print_error(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
