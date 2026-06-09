import os

from services.school_system import SchoolSystem


MENU = """
===== Student Course Registration System =====

1. Add Student
2. View Students
3. Search Student
4. Add Course
5. View Courses
6. Register Student to Course
7. View Students in a Course
8. View Courses for a Student
9. Save Data
10. Load Data
0. Exit
"""


def pause():
    input("\nPress Enter to continue...")


def prompt_required(label):
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print(f"{label} cannot be empty.")


def prompt_email():
    while True:
        email = prompt_required("Email")
        if "@" in email and not email.startswith("@") and not email.endswith("@"):
            return email
        print("Email must contain @ and have text before and after it.")


def prompt_positive_number(label):
    while True:
        value = input(f"{label}: ").strip()
        try:
            number = int(value)
        except ValueError:
            print(f"{label} must be a number.")
            continue

        if number > 0:
            return number
        print(f"{label} must be greater than 0.")


def print_section(title):
    print(f"\n--- {title} ---")


def print_students(students):
    if not students:
        print("No students found.")
        return

    for student in students:
        print(student.display())
        print("-" * 35)


def print_courses(system, courses):
    if not courses:
        print("No courses found.")
        return

    for course in courses:
        registered_count = system.course_registration_count(course.course_id)
        print(course.display(registered_count))
        print("-" * 35)


def add_student(system):
    print_section("Add Student")
    student_id = prompt_required("Student ID")
    name = prompt_required("Name")
    email = prompt_email()
    phone_number = prompt_required("Phone number")

    try:
        student = system.add_student(student_id, name, email, phone_number)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(f"Student {student.name} added successfully.")


def view_students(system):
    print_section("All Students")
    print_students(system.get_all_students())


def search_student(system):
    print_section("Search Student")
    search_term = prompt_required("Enter student ID or name")

    try:
        results = system.search_students(search_term)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print_students(results)


def add_course(system):
    print_section("Add Course")
    course_id = prompt_required("Course ID")
    course_name = prompt_required("Course Name")
    trainer_name = prompt_required("Trainer")
    capacity = prompt_positive_number("Capacity")

    try:
        course = system.add_course(course_id, course_name, trainer_name, capacity)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(f"Course {course.course_name} added successfully.")


def view_courses(system):
    print_section("All Courses")
    print_courses(system, system.get_all_courses())


def register_student(system):
    print_section("Register Student to Course")
    student_id = prompt_required("Student ID")
    course_id = prompt_required("Course ID")

    try:
        message = system.register_student(student_id, course_id)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(message)


def view_students_in_course(system):
    print_section("Students in a Course")
    course_id = prompt_required("Course ID")

    try:
        students = system.get_students_in_course(course_id)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print_students(students)


def view_courses_for_student(system):
    print_section("Courses for a Student")
    student_id = prompt_required("Student ID")

    try:
        courses = system.get_courses_for_student(student_id)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print_courses(system, courses)


def save_data(system):
    print_section("Save Data")
    print(system.save_data())


def load_data(system):
    print_section("Load Data")
    try:
        print(system.load_data())
    except ValueError as error:
        print(f"Error: {error}")


def exit_program(system):
    print_section("Exit")
    try:
        print(system.save_data())
    except ValueError as error:
        print(f"Data could not be saved: {error}")
    print("Goodbye.")


def run_menu(data_dir=None):
    selected_data_dir = data_dir or os.environ.get("SCHOOL_DATA_DIR", "data")
    system = SchoolSystem(selected_data_dir)
    try:
        startup_message = system.load_data()
    except ValueError as error:
        startup_message = f"Could not load saved data: {error}"
    print(startup_message)

    actions = {
        "1": add_student,
        "2": view_students,
        "3": search_student,
        "4": add_course,
        "5": view_courses,
        "6": register_student,
        "7": view_students_in_course,
        "8": view_courses_for_student,
        "9": save_data,
        "10": load_data,
    }

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "0":
            exit_program(system)
            break

        action = actions.get(choice)
        if action is None:
            print("Invalid option. Please choose a number from the menu.")
        else:
            action(system)

        pause()


if __name__ == "__main__":
    run_menu()
