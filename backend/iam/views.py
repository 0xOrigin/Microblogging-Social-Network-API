from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView as JwtTokenRefreshView
from django.utils.translation import gettext_lazy as _
from core.renderers import BaseJSONRenderer
from core.views import BaseViewSet, NonCreatableViewSet
from iam.authentication import set_jwt_cookies, unset_jwt_cookies
from iam.filters import UserFilter
from iam.permissions import UserPermissions
from iam.models import User
from iam.serializers import UserSerializer, UserRegistrationSerializer


class BaseUserGenericAPIView(generics.GenericAPIView):
    renderer_classes = [BaseJSONRenderer, BrowsableAPIRenderer]
    permission_classes = []

    def get_queryset(self):
        return User.objects.all()


class LoginView(TokenObtainPairView, BaseUserGenericAPIView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        set_jwt_cookies(response, response.data['access_token'], response.data.pop('refresh'))
        return response


class LogoutView(BaseUserGenericAPIView):

    def get(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_200_OK)
        unset_jwt_cookies(response)
        return response


class TokenRefreshView(JwtTokenRefreshView, BaseUserGenericAPIView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        set_jwt_cookies(response, response.data.get('access_token'), response.data.get('refresh_token'))
        return response


class UserViewSet(NonCreatableViewSet, BaseViewSet):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [UserPermissions,]

    def get_queryset(self):
        return super().get_queryset()

    @action(detail=False, methods=['post'], url_name='register', url_path='register', permission_classes=[])
    def register(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)