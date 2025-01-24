from rest_framework.exceptions import APIException
from rest_framework import status


class AppException(APIException):
    """Base class for all application exceptions."""
    status_code = status.HTTP_400_BAD_REQUEST  # Default HTTP status code
    default_detail = 'An error occurred.'
    default_code = 'error'

    def __init__(self, message=None, message_en=None, status_code=None):
        if message:
            self.default_detail = message
        if message_en:
            self.message_en = message_en
        if status_code:
            self.status_code = status_code
        super().__init__(self.default_detail)

    def to_representation(self):
        return {
            "message": self.default_detail,
            "message_en": self.message_en,
            "status": self.status_code
        }
