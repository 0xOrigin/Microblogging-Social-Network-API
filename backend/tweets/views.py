from django.db.models import Q
from core.views import BaseViewSet
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from tweets.permissions import TweetPermissions


class TweetViewSet(BaseViewSet):
    model = Tweet
    queryset = model.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [TweetPermissions,]

    def get_queryset(self):
        if self.request.user.is_anonymous: # For browsable api issue
            return super().get_queryset().order_by('-created_at')

        return (
            super().get_queryset()
            .prefetch_related('created_by')
            .filter(Q(created_by=self.request.user) | Q(created_by__followers__follower=self.request.user))
            .order_by('-created_at')
        )
