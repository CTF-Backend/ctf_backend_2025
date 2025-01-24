class AppException(Exception):
    """Base class for all application exceptions."""
    message = 'An error occurred.'  # Default message
    message_en = 'An error occurred.'  # Default English message
    status = 400  # Default HTTP status code

    def __init__(self, message=None, message_en=None, status=None):
        if message:
            self.message = message
        if message_en:
            self.message_en = message_en
        if status:
            self.status = status
        super().__init__(self.message)

    def to_dict(self):
        """Converts the exception to a dictionary format."""
        return {
            "message": self.message,
            "message_en": self.message_en,
            "status": self.status
        }