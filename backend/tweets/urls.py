from django.urls import path
from django.urls import include
from tweets.apps import TweetsConfig

app_name = TweetsConfig.name

urlpatterns = [
    path('api/', include('tweets.api.urls'), name='tweets-api'),
]
