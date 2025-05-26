from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
import logging

from utils.apps_exceptions import AppException

logger = logging.getLogger(__name__)

ERROR_TRANSLATIONS = {
    "user with this username already exists.": "نام کاربری وارد شده قبلا ثبت شده است.",
    "This field may not be blank.": "این فیلد نمی‌تواند خالی باشد.",
    "This field is required.": "پر کردن این فیلد الزامی است.",
    "Enter a valid email address.": "یک ایمیل معتبر وارد کنید.",
    "Passwords do not match.": "رمزهای عبور مطابقت ندارند.",
    "Ensure this field has at most": "حداکثر طول این فیلد باید",
    "Ensure this field has at least": "حداقل طول این فیلد باید",
    # اگر پیام‌های بیشتری مد نظرت بود اضافه کن
}


def translate_errors(data):
    if isinstance(data, dict):
        return {key: translate_errors(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [translate_errors(item) for item in data]
    elif isinstance(data, str):
        # جستجو در کلیدهای دیکشنری و جایگزینی اگر شروع متن یکی از کلیدها بود
        for en_text, fa_text in ERROR_TRANSLATIONS.items():
            if data.lower().startswith(en_text):
                return data.replace(en_text, fa_text)
        return data
    else:
        return data


def extract_message(data):
    """
    داده را بررسی می‌کند و فقط متن پیام را استخراج می‌کند:
    - اگر دیکشنری باشد و کلید 'detail' داشته باشد، مقدار آن را برمی‌گرداند
    - اگر دیکشنری باشد بدون 'detail'، اولین مقدار را استخراج می‌کند
    - اگر لیست باشد، اولین پیام را استخراج می‌کند
    - اگر رشته باشد، همان را برمی‌گرداند
    """
    if isinstance(data, dict):
        if 'detail' in data:
            return extract_message(data['detail'])
        # اگر دیکشنری است ولی detail ندارد، اولین مقدار را استخراج کن
        for value in data.values():
            return extract_message(value)
    elif isinstance(data, list):
        if len(data) > 0:
            return extract_message(data[0])
        else:
            return ""
    elif isinstance(data, str):
        return data
    return ""


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # If DRF handled the exception (like ValidationError), format it
    if response is not None:
        translated = translate_errors(response.data)
        message = extract_message(translated)
        return Response(
            {
                "message": message,
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
