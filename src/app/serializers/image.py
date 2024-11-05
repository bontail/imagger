import os
from io import BytesIO
from django.core.files.base import ContentFile
from typing import Any
from django.core.files.uploadedfile import TemporaryUploadedFile, \
    InMemoryUploadedFile
from app.models import Image
from rest_framework.serializers import ModelSerializer
from PIL import Image as PILImage


class MultiplyImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = (
            'id', 'name', 'image', 'resolution', 'size', 'author', 'tags',
        )


class ImageSerializer(MultiplyImageSerializer):
    class Meta:
        model = Image
        fields = (
            'id', 'name', 'image', 'upload_datetime', 'update_datetime',
            'resolution', 'size', 'is_private', 'author', 'tags', 'description'
        )
        read_only_fields = ('id', 'size', 'author')

    @staticmethod
    def process_pil_image(image: PILImage,
                          resolution: tuple) -> PILImage:
        image = image.resize(resolution)
        image = image.convert('L')
        return image

    def process_memory_image(self, image: InMemoryUploadedFile,
                             resolution: tuple) -> InMemoryUploadedFile:
        memory_image = BytesIO(image.read())
        pil_img = PILImage.open(memory_image)
        pil_img = self.process_pil_image(pil_img, resolution)
        img_format = os.path.splitext(image.name)[1][1:].upper()
        memory_image = BytesIO()
        pil_img.save(memory_image, format=img_format)
        image = InMemoryUploadedFile(
            ContentFile(memory_image.getvalue()),
            "image", image.name,
            image.content_type, len(memory_image.getvalue()), None
        )
        return image

    def process_temporary_image(self, image: TemporaryUploadedFile,
                                resolution: tuple) -> TemporaryUploadedFile:
        pil_img: PILImage = PILImage.open(image.file)
        pil_img = self.process_pil_image(pil_img, resolution)
        pil_img.save(image.temporary_file_path())
        return image

    def process_image(self, image: InMemoryUploadedFile | TemporaryUploadedFile, resolution: tuple):
        if isinstance(image, InMemoryUploadedFile):
            image = self.process_memory_image(image, resolution)
        else:
            image = self.process_temporary_image(image, resolution)
        return image

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        image = data.get('image')
        resolution = tuple(map(int, data.get('resolution', "0x0").split('x')))
        if image and resolution != (0, 0):
            image = self.process_image(image, resolution)
            data['image'] = image
        return data

    def update(self, instance: Image, validated_data: dict[str, Any]) -> Image:
        instance.name = validated_data.get('name', instance.name)
        instance.tags.set(validated_data.get('tags', instance.tags.all()))
        instance.is_private = validated_data.get(
            'is_private', instance.is_private
        )
        instance.resolution = validated_data.get(
            'resolution', instance.resolution
        )
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.save()
        return instance
