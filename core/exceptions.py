from utils.apps_exceptions import AppException


class UsernameIsRequired(AppException):
    message = 'وارد کردن نام تیم الزامی میباشد.'
    message_en = 'team name is required.'


class PasswordISNotSameAsPassword2(AppException):
    message = 'پسورد ارسال شده با پسورد تکرار شده تطابق ندارد.'
    message_en = 'The password sent does not match the repeated password.'


class PasswordAndUsernameIsRequired(AppException):
    message = 'وارد کردن نام کاربری و رمز عبور الزامی است.'
    message_en = 'Entering a username and password is required.'


class PasswordOrUsernameIsIncorrect(AppException):
    message = 'نام کاربری یا رمز عبور وارد شده نادرست میباشد.'
    message_en = 'The username or password entered is incorrect.'


class SuccessfullyLoggOut(AppException):
    message = 'با موفقیت از حساب کاربری خود خارج شدید.'
    message_en = 'You have been successfully logged out.'
    status_code = 200
