from CTFBackend2025.apps_exceptions import AppException


class EmailISNotValid(AppException):
    message = 'ایمیل وارد شده معتبر نمی باشد.'
    message_en = 'entered email is not valid.'


class UsernameIsRequired(AppException):
    message = 'وارد کردن نام تیم الزامی میباشد.'
    message_en = 'team name is required.'


class IsSuperuserMustBeTrue(AppException):
    message = 'برای ادمین تیک تایید کاربر ویژه باید زده شود.'
    message_en = 'for the admin, the is_superuser checkbox must be selected.'


class PasswordISNotSameAsPassword2(AppException):
    message = 'پسورد ارسال شده با تکرار پسورد تطابق ندارد.'
    message_en = 'password and password2 are not match.'
