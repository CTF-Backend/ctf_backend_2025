from utils.apps_exceptions import AppException


class EmailISNotValid(AppException):
    message = 'ایمیل وارد شده معتبر نمی باشد.'
    message_en = 'entered email is not valid.'


class UsernameIsRequired(AppException):
    message = 'وارد کردن نام تیم الزامی میباشد.'
    message_en = 'team name is required.'


class PasswordISNotSameAsPassword2(AppException):
    message = 'پسورد ارسال شده با پسورد تکرار شده تطابق ندارد.'
    message_en = 'The password sent does not match the repeated password.'
