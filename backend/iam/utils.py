from django.conf import settings
from django.utils import timezone
from iam.models import User


def create_superuser():
    if User.objects.filter(is_superuser=True, is_staff=True, is_active=True).exists():
        return
    User.objects.create_superuser(
        username='admin',
        email='egyahmed.ezzat120@gmail.com',
        password='Admin@123',
        first_name='Ahmed',
        last_name='Ezzat',
    )
    print('Superuser created')
