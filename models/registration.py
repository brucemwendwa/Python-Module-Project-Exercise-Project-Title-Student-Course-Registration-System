class Registration:
    """Connects one student to one course."""

    def __init__(self, student_id, course_id):
        self.student_id = str(student_id).strip()
        self.course_id = str(course_id).strip()

        if not self.student_id:
            raise ValueError("Registration must include a student ID.")
        if not self.course_id:
            raise ValueError("Registration must include a course ID.")

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "course_id": self.course_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("student_id", ""), data.get("course_id", ""))

    def has_same_pair(self, student_id, course_id):
        return self.student_id == student_id and self.course_id == course_id
