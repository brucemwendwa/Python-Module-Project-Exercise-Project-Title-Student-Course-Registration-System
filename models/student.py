from models.person import Person


class Student(Person):
    """Represents one student and inherits shared contact details from Person."""

    def __init__(self, student_id, name, email, phone_number):
        self.student_id = self._require_text(student_id, "Student ID")
        super().__init__(name, email, phone_number)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("student_id", ""),
            data.get("name", ""),
            data.get("email", ""),
            data.get("phone_number", ""),
        )

    def matches(self, search_term):
        lowered_term = search_term.strip().lower()
        return lowered_term in self.student_id.lower() or lowered_term in self.name.lower()

    def display(self):
        return (
            f"Student ID: {self.student_id}\n"
            f"Name: {self.name}\n"
            f"{self.contact_details()}"
        )
