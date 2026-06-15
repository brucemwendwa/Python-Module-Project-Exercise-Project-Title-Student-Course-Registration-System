import sys

try:
    from rich import box
    from rich.console import Console
    from rich.table import Table
except ImportError:  # pragma: no cover - fallback is for environments without Pipfile install
    box = None
    Console = None
    Table = None


def _rich_console(stderr=False):
    if Console is None:
        return None
    return Console(stderr=stderr, highlight=False)


def print_success(message):
    console = _rich_console()
    if console is None:
        print(message)
        return
    console.print(message, style="green")


def print_error(message):
    console = _rich_console(stderr=True)
    if console is None:
        print(message, file=sys.stderr)
        return
    console.print(message, style="red")


def print_info(message):
    console = _rich_console()
    if console is None:
        print(message)
        return
    console.print(message)


def print_students(students):
    students = list(students)
    if not students:
        print_info("No students found.")
        return

    console = _rich_console()
    if console is None:
        for student in students:
            print(student.display())
            print("-" * 35)
        return

    table = Table(title="Students", box=box.ASCII)
    table.add_column("Student ID", style="cyan")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Phone")

    for student in students:
        table.add_row(
            student.student_id,
            student.name,
            student.email,
            student.phone_number,
        )

    console.print(table)


def print_courses(system, courses):
    courses = list(courses)
    if not courses:
        print_info("No courses found.")
        return

    console = _rich_console()
    if console is None:
        for course in courses:
            registered_count = system.course_registration_count(course.course_id)
            print(course.display(registered_count))
            print("-" * 35)
        return

    table = Table(title="Courses", box=box.ASCII)
    table.add_column("Course ID", style="cyan")
    table.add_column("Course Name")
    table.add_column("Trainer")
    table.add_column("Capacity", justify="right")
    table.add_column("Registered", justify="right")

    for course in courses:
        registered_count = system.course_registration_count(course.course_id)
        table.add_row(
            course.course_id,
            course.course_name,
            course.trainer_name,
            str(course.capacity),
            f"{registered_count}/{course.capacity}",
        )

    console.print(table)
