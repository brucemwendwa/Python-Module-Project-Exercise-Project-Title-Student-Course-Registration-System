class Person:
    """Base class for people stored in the school system."""

    def __init__(self, name, email, phone_number):
        self.name = self._require_text(name, "Name")
        self.email = self._validate_email(email)
        self.phone_number = self._require_text(phone_number, "Phone number")

    @staticmethod
    def _require_text(value, field_name):
        cleaned_value = str(value).strip()
        if not cleaned_value:
            raise ValueError(f"{field_name} cannot be empty.")
        return cleaned_value

    @staticmethod
    def _validate_email(email):
        cleaned_email = str(email).strip()
        if "@" not in cleaned_email or cleaned_email.startswith("@") or cleaned_email.endswith("@"):
            raise ValueError("Email must contain @ and have text before and after it.")
        return cleaned_email

    def contact_details(self):
        return f"Email: {self.email}\nPhone: {self.phone_number}"
