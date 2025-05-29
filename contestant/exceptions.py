from utils.apps_exceptions import AppException


class MaxTeamMember(AppException):
    message = 'تعداد اعضای هر تیم 3 نفر میباشد.'
    message_en = 'The number of members in each team is 3.'


class EditTeamMemberIsNotAllowed(AppException):
    message = 'بعد از تایید استف امکان ویرایش اطلاعات اعضای تیم وجود ندارد.'
    message_en = 'After staff approval, editing team members information is not allowed.'


class AnswerLimitExceeded(AppException):
    message = 'حد مجاز تعداد پاسخ‌های صحیح برای این سوال تکمیل شده است.'
    message_en = 'The maximum number of correct answers for this question has been reached.'


class AnswerSubmissionEnded(AppException):
    message = 'مهلت ارسال پاسخ به اتمام رسیده است.'
    message_en = 'Answer submission has been ended.'


class FlagIsWrong(AppException):
    message = 'فلگ ارسال شده نادرست است.'
    message_en = 'The flag is wrong.'


class FlagIsDuplicate(AppException):
    message = 'شما قبلا به این سوال پاسخ داده اید.'
    message_en = 'You have already answered this question.'


class HintAlreadyReceived(AppException):
    message = 'شما راهنمایی این فلگ را دریافت کرده اید.'
    message_en = 'You have received the hint for this flag.'


class CoinIsNotEnough(AppException):
    message = 'سکه های شما برای خرید این راهنمایی کافی نمیباشد.'
    message_en = 'Your coins are not enough to purchase this hint.'


class UserDoesNotHaveTeam(AppException):
    message = 'کاربر وارد شده دارای تیم نمیباشد.'
    message_en = 'User does not have team.'


class TeamDoesntExist(AppException):
    message = 'شما به عنوان تیم وارد نشده اید.'
    message_en = 'You are not logged in as a team.'


class FlagCountLimitation(AppException):
    message = 'شما به حداکثر تعداد مجاز ثبت فلگ رسیده‌اید.'
    message_en = 'You have reached the maximum allowed number of flag submissions.'
