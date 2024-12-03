from django.urls import path
from django.urls import include


urlpatterns = [
    path('v1/iam/', include('iam.api.v1.urls'), name='iam-api-v1'),
]
