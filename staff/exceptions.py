from utils.apps_exceptions import AppException


class OnlyTeamIsAllowed(AppException):
    message = 'تنها تیم ها مجاز به پرسیدن سوالات می باشند.'
    message_en = 'Only teams are allowed to ask questions.'
