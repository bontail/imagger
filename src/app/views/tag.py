from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from app.models import Tag
from app.serializers import TagSerializer


class GetAllTagsView(ListAPIView):
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
