from django.contrib import admin
from core.admin import BaseAdmin
from tweets.models import Tweet


@admin.register(Tweet)
class TweetAdmin(BaseAdmin):
    pass
