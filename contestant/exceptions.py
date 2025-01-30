from utils.apps_exceptions import AppException


class MaxTeamMember(AppException):
    message = 'تعداد اعضای هر تیم 3 نفر میباشد.'
    message_en = 'The number of members in each team is 3.'


class EditTeamMemberIsNotAllowed(AppException):
    message = 'بعد از تایید استف امکان ویرایش اطلاعات اعضای تیم وجود ندارد.'
    message_en = 'After staff approval, editing team members information is not allowed.'
