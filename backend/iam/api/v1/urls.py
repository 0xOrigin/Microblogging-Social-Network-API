from django.urls import path
from django.urls import include
from django.conf import settings
from rest_framework_nested import routers
from iam.views import LoginView, LogoutView, TokenRefreshView, UserViewSet


router = routers.DefaultRouter(trailing_slash=settings.APPEND_SLASH)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
