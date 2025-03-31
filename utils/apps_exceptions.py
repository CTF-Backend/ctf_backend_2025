from rest_framework.exceptions import APIException
from rest_framework import status

class AppException(APIException):
    """Base class for all application exceptions."""
    status_code = status.HTTP_400_BAD_REQUEST  # Default HTTP status code
    default_detail = "An error occurred."
    default_code = "error"

    def __init__(self, message=None, message_en=None, status_code=None):
        # Get class-level attributes if not overridden in __init__
        self.message = message or getattr(self, "message", self.default_detail)
        self.message_en = message_en or getattr(self, "message_en", "An error occurred.")
        self.status_code = status_code or self.status_code

        super().__init__(self.message)

    def to_representation(self):
        return {
            "message": self.message,
            "message_en": self.message_en,
            "status": self.status_code
        }
