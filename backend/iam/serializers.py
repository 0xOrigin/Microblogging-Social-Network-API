from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.serializers import BaseSerializer
from core.utils import dynamic_exclude
from iam.models import User, Follow
from iam.emails import send_user_registration_email


class BaseTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    default_error_messages = {
        'no_active_account': _('Invalid email or password')
    }

    def validate(self, attrs):
        data = super().validate(attrs)

        data['access_token'] = data.pop('access')
        data['user'] = UserSerializer(self.user, context=self.context).data
        return data


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(required=False)

    def extract_refresh_token(self):
        request = self.context['request']
        if 'refresh' in request.data and request.data['refresh'] != '':
            return request.data['refresh']
        
        cookie_name = settings.JWT_AUTH_REFRESH_COOKIE_NAME
        if cookie_name and cookie_name in request.COOKIES:
            return request.COOKIES.get(cookie_name)
        else:
            raise InvalidToken(_('No valid refresh token found'))

    def validate(self, attrs):
        attrs['refresh'] = self.extract_refresh_token()
        data = super().validate(attrs)
        data['refresh_token'] = data.pop('refresh')
        data['access_token'] = data.pop('access')
        return data


class UserSerializer(BaseSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        exclude = dynamic_exclude(model)
        extra_kwargs = dict(
            BaseSerializer.Meta.extra_kwargs,
            **{
                'last_login': {'read_only': True},
                'password': {'write_only': True},
            }
        )

    def validate_email(self, value):
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        try:
            validate_password(value)
        except Exception as exception:
            raise serializers.ValidationError(exception.messages)
        return value

    def save(self, **kwargs):
        if 'password' in self.validated_data:
            self.validated_data['password'] = make_password(self.validated_data['password'])
        return super().save(**kwargs)


class UserRegistrationSerializer(UserSerializer):

    class Meta:
        model = User
        exclude = dynamic_exclude(model)
        extra_kwargs = UserSerializer.Meta.extra_kwargs

    def validate_confirm_password(self):
        if 'confirm_password' not in self.initial_data:
            raise serializers.ValidationError({'confirm_password': _('This field is required.')})
        return self.initial_data.get('confirm_password')

    def validate_passwords_match(self, password, confirm_password):
        if password != confirm_password:
            raise serializers.ValidationError(_("The two password fields didn't match."))

    def validate(self, attrs):
        attrs = super().validate(attrs)
        confirm_password = self.validate_confirm_password()
        self.validate_passwords_match(attrs['password'], confirm_password)
        return attrs
    
    def create(self, validated_data):
        validated_data['is_active'] = True
        instance = super().create(validated_data)
        send_user_registration_email(instance)
        return instance


class FollowSerializer(BaseSerializer):

    class Meta:
        model = Follow
        exclude = dynamic_exclude(model, extra_fields=['follower'])
        extra_kwargs = {
            'followee': {'read_only': True},
        }

    def get_nested_serializer_fields(self) -> dict:
        data = super().get_nested_serializer_fields()
        data.update({
            'followee': {
                'serializer': UserSerializer,
                'kwargs': {'context': self.context},
            },
        })
        return data

    def set_from_context(self, validated_data):
        super().set_from_context(validated_data)
        validated_data['follower'] = self.get_current_user()
        if 'followee_pk' in self.context:
            validated_data['followee_id'] = self.context.get('followee_pk')

    def validate_follower_followee_not_equal(self, follower, followee):
        if str(follower) == str(followee):
            raise serializers.ValidationError(_('You cannot follow yourself!'))

    def validate_follower_followee_unique_together(self, follower, followee):
        if Follow.objects.filter(follower=follower, followee=followee).exists():
            raise serializers.ValidationError(_('You are already following this user'))

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self.validate_follower_followee_not_equal(self.get_current_user().pk, self.context.get('followee_pk'))
        self.validate_follower_followee_unique_together(self.get_current_user(), self.context.get('followee_pk'))
        return attrs
