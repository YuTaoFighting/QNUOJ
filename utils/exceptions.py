from rest_framework import status
from rest_framework.exceptions import APIException


class UserDisabledException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = '该用户处于不可用状态，如有疑问请联系管理员。'


class UserDoesNotExistException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '用户不存在。'


class ContestDoesNotExistException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '比赛不存在。'


class ContestIsPendingException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '比赛还未开始， 无法查看该页面。'


class ContestIsEndedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '比赛已经结束。'


class ProblemDoesNotExistException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '题目不存在。'


class SubmissionDoesNotExistException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '提交记录不存在。'


class SubmissionUserDoesNotSelfException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '提交用户与登录用户不一致。'


class TokenInvalidException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Token无效。'
