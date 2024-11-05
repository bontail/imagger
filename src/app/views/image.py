from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (CreateAPIView, ListAPIView, UpdateAPIView,
                                     RetrieveAPIView, DestroyAPIView)
from app.models import Image
from app.serializers import ImageSerializer, MultiplyImageSerializer


class CreateImageView(CreateAPIView):
    model = Image
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = ImageSerializer

    def perform_create(self, serializer: ImageSerializer) -> None:
        serializer.save(author_id=self.request.user.id)


class UpdateImageView(UpdateAPIView):
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = ImageSerializer
    lookup_field = "id"

    def get_queryset(self) -> QuerySet:
        return Image.objects.filter(author_id=self.request.user.id)


class GetAllImagesView(ListAPIView):
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = MultiplyImageSerializer
    queryset = Image.objects.filter(is_private=False)


class GetUserImagesView(ListAPIView):
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = MultiplyImageSerializer

    def get_queryset(self) -> QuerySet:
        author_id = int(
            self.request.
            parser_context.
            get('kwargs').
            get("user_id", self.request.user.id)
        )
        return Image.objects.filter(
            author_id=author_id,
            is_private__in=[False, author_id == self.request.user.id]
        )


class GetImageView(RetrieveAPIView, GetUserImagesView):
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = ImageSerializer
    lookup_field = "id"


class DeleteImageView(DestroyAPIView, GetImageView):
    pass
