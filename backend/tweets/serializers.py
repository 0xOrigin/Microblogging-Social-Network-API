from core.serializers import BaseSerializer
from iam.serializers import UserSerializer
from tweets.models import Tweet


class TweetSerializer(BaseSerializer):

    class Meta:
        model = Tweet
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

    def get_nested_serializer_fields(self) -> dict:
        data = super().get_nested_serializer_fields()
        data.update({
            'created_by': {
                'serializer': UserSerializer,
                'kwargs': {'context': self.context}
            },
        })
        return data
