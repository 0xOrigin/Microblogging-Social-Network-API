from django.db import models
from core.models import BaseAuditModel


class Tweet(BaseAuditModel):
    tweet_text = models.CharField(max_length=140, null=False, blank=False)

    class Meta:
        db_table = 'Tweet'
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['created_by']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.pk
