from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, APIException):
        response_data = {
            'message': getattr(exc, 'message', ''),
            'message_en': getattr(exc, 'message_en', ''),
            'status': exc.status_code
        }
        return Response(response_data, status=exc.status_code)

    return response
