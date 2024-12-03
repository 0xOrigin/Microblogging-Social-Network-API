from django.urls import path
from django.urls import include


urlpatterns = [
    path('v1/tweets/', include('tweets.api.v1.urls'), name='tweets-api-v1'),
]
