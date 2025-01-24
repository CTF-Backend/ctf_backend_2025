from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    # Call the default exception handler
    response = exception_handler(exc, context)

    # Handle custom exceptions
    if isinstance(exc, APIException):
        # If the exception is a custom exception, modify the response
        response_data = {
            'message': getattr(exc, 'message', ''),
            'message_en': getattr(exc, 'message_en', ''),
            'status': exc.status_code
        }
        # Return the custom response
        return Response(response_data, status=exc.status_code)

    # In case no custom exception is found, return the default response
    return response
