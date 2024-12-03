from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from core.utils import get_random_file_name
from core.models import BaseManager, BaseAuditModel


class UserManager(BaseUserManager, BaseManager):

    def create_user(self, email, username, password=None, created_at=timezone.now(), **kwargs):
        if not email:
            raise ValueError(_('User must have an email address'))
        if not username:
            raise ValueError(_('User must have a username'))

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            created_at=created_at,
            is_active=True,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, created_at=timezone.now(), **kwargs):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            created_at=created_at,
            **kwargs
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def validate_image_size(image):
    MAX_SIZE = 1.0 * 1024 * 1024
    if image.size > MAX_SIZE:
        raise ValidationError(_('Image size must be less than or equal 1MB'))


class User(AbstractUser, BaseAuditModel):

    def get_user_picture_upload_path(self, filename):
        return get_random_file_name('profile-pictures/', filename)
    
    email = models.EmailField(unique=True, null=False, blank=False)
    picture = models.ImageField(upload_to=get_user_picture_upload_path, null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'png']), validate_image_size
    ])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'User'
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['email']),
            models.Index(fields=['username']),
        ]

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.email}"
