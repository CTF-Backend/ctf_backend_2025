from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
import logging

from utils.apps_exceptions import AppException

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # If DRF handled the exception (like ValidationError), format it
    if response is not None:
        return Response(
            {
                "message": response.data.get("detail", "An unexpected error occurred."),
                "message_en": "An unexpected error occurred.",
                "status": response.status_code
            },
            status=response.status_code
        )

    # Handle custom AppException and APIException
    if isinstance(exc, AppException) or isinstance(exc, APIException):
        response_data = {
            "message": getattr(exc, "message", "An error occurred."),
            "message_en": getattr(exc, "message_en", "An error occurred."),
            "status": getattr(exc, "status_code", status.HTTP_400_BAD_REQUEST),
        }
        return Response(response_data, status=exc.status_code)

    # Log unexpected exceptions
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

    # Handle unexpected Python errors
    return Response(
        {
            "message": "An internal server error occurred.",
            "message_en": "An internal server error occurred.",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
