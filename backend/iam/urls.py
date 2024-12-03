from django.urls import path
from django.urls import include
from iam.apps import IamConfig

app_name = IamConfig.name

urlpatterns = [
    path('api/', include('iam.api.urls'), name='iam-api'),
]
