class Course:
    """Represents a course offered by the school."""

    def __init__(self, course_id, course_name, trainer_name, capacity):
        self.course_id = self._require_text(course_id, "Course ID")
        self.course_name = self._require_text(course_name, "Course name")
        self.trainer_name = self._require_text(trainer_name, "Trainer name")
        self.capacity = self._validate_capacity(capacity)

    @staticmethod
    def _require_text(value, field_name):
        cleaned_value = str(value).strip()
        if not cleaned_value:
            raise ValueError(f"{field_name} cannot be empty.")
        return cleaned_value

    @staticmethod
    def _validate_capacity(capacity):
        try:
            cleaned_capacity = int(capacity)
        except (TypeError, ValueError) as exc:
            raise ValueError("Course capacity must be a number.") from exc

        if cleaned_capacity <= 0:
            raise ValueError("Course capacity must be greater than 0.")

        return cleaned_capacity

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "trainer_name": self.trainer_name,
            "capacity": self.capacity,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("course_id", ""),
            data.get("course_name", ""),
            data.get("trainer_name", ""),
            data.get("capacity", 0),
        )

    def display(self, registered_count=0):
        return (
            f"Course ID: {self.course_id}\n"
            f"Course Name: {self.course_name}\n"
            f"Trainer: {self.trainer_name}\n"
            f"Capacity: {self.capacity} students\n"
            f"Registered: {registered_count}/{self.capacity}"
        )
