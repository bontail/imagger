from app.models import Tag
from rest_framework.serializers import ModelSerializer


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name',
        )
