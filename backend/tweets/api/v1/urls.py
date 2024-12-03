from django.urls import path
from django.urls import include
from django.conf import settings
from rest_framework_nested import routers
from tweets.views import TweetViewSet


router = routers.DefaultRouter(trailing_slash=settings.APPEND_SLASH)
router.register(r'tweets', TweetViewSet, 'tweet')

urlpatterns = [
    path('', include(router.urls)),
]
