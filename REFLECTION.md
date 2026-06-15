# Project Reflection

## Project Summary

This project is a terminal-based Student Course Registration System. It allows an admin to add students, add courses, register students for courses, search records, view registration lists, and save or load data using JSON files.

The project now includes two ways to use the program: an interactive menu in `main.py` and an `argparse` subcommand CLI in `cli.py`.

## What was the hardest part of this project?

The hardest part was the registration logic. The system needed to check several things before adding a registration: whether the student exists, whether the course exists, whether the student is already registered, and whether the course still has space.

## Which classes did you create and why?

I created `Person` as a base class for shared personal details like name, email, and phone number.

I created `Student` to store student information and inherit shared details from `Person`.

I created `Course` to store course information such as course ID, course name, trainer name, and capacity.

I created `Registration` to represent the link between one student and one course.

I created `SchoolSystem` to manage the main logic, including adding records, searching, registering students, saving data, and loading data.

## How did you use object-oriented programming?

I used separate classes so that each part of the system has a clear responsibility. `Student`, `Course`, and `Registration` store project data, while `SchoolSystem` controls the main actions. I also used inheritance by making `Student` inherit shared contact fields from the `Person` class.

## How did you build the command-line interface?

The first interface is the menu in `main.py`, which repeatedly asks the user to choose an option. To meet the CLI project rubric, I also added `cli.py`, which uses `argparse` subcommands such as `add-student`, `add-course`, `register`, `list-students`, and `list-courses`. This makes the project easier to test and allows users to run specific actions directly from the terminal.

## How does your registration logic prevent duplicate registrations?

Before adding a new registration, the `SchoolSystem.register_student()` method calls `is_registered()`. That method loops through the existing registrations and checks whether the same student ID and course ID already exist together. If they do, the system raises an error and does not add another registration.

## How does your system check if a course is full?

The system counts how many registrations already exist for the course using `course_registration_count()`. Then `is_course_full()` compares that number with the course capacity. If the count is equal to or greater than the capacity, registration is blocked.

## What bugs did you face and how did you fix them?

One bug was handling invalid course capacity input. If the user typed text instead of a number, the program could have crashed. I fixed it by using `try` and `except` and asking for a valid number.

Another issue was loading saved JSON data safely. A saved registration could point to a missing student or course. I fixed this by checking records during loading and skipping invalid or duplicate records.

I also had to adjust the screenshot helper because normal subprocess input did not show typed values in the captured terminal output. I fixed that by using a pseudo-terminal so the screenshots look like real terminal sessions.

Another challenge was adding the `argparse` CLI without duplicating the whole program. I solved this by keeping the main logic inside `SchoolSystem` and making both `main.py` and `cli.py` call the same methods.

## What did you learn?

This project helped me practice classes, inheritance, validation, dictionaries, lists, loops, functions, modules, error handling, file handling, and CLI design with `argparse`. I also learned how useful it is to separate user interface code from business logic, because it made the `SchoolSystem` class easier to reuse and test.

I also learned how to manage external packages with a `Pipfile`. The project uses `rich` for clearer CLI output, and the screenshot helper uses `pillow` to generate terminal screenshots.

## Which part of the code would you improve if you had more time?

If I had more time, I would add update and delete features for students and courses. I would also improve validation for phone numbers and email addresses, and I would add more tests for the menu input flow.
