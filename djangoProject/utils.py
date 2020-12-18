from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


class Forbidden(APIException):
    status_code = 403
