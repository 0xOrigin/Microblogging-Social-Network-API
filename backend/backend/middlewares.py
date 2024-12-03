import traceback
from urllib.parse import parse_qs
from rest_framework import status
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AnonymousUser
from iam.authentication import JWTCookieAuthentication


def get_error_response(message, status_code):
    return JsonResponse(
        {
            'status_code': status_code,
            'message': message,
            'error': {}
        },
        status=status_code
    )


class JWTCookieAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authentication = JWTCookieAuthentication()

    def __call__(self, request):
        self.authenticate(request)
        response = self.get_response(request)
        return response

    def authenticate(self, request):
        try:
            authentication_result = self.jwt_authentication.authenticate(request)
        except AuthenticationFailed:
            authentication_result = None
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            return
        if authentication_result:
            request.user = authentication_result[0]


class ExceptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        return JsonResponse(
            {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': repr(exception),
                'error': {
                    'stacktrace': traceback.format_exc().split('\n')
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
