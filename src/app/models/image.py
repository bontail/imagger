import re
from django.core.exceptions import ValidationError
from django.db.models import Model, CharField, ImageField, DateTimeField, \
    BooleanField, ManyToManyField, ForeignKey, PROTECT, \
    PositiveIntegerField, TextField
from django.conf import settings
from django.core.files.images import get_image_dimensions
from imagger.celery import image_uploaded, image_deleted
import uuid


def validate_resolution(value: str) -> None:
    reg = re.compile(r'^(([1-4]?[0-9]{3})|5000)x(([1-4]?[0-9]{3})|5000)$')
    if not reg.match(value):
        raise ValidationError(f"Invalid format ({value})")


def generate_image_path(instance: 'Image', filename: str) -> str:
    ext = filename.split('.')[-1]
    return f'images/{uuid.uuid4()}.{ext}'


class Image(Model):
    name = CharField(max_length=30)
    image = ImageField(upload_to=generate_image_path)
    upload_datetime = DateTimeField(auto_now_add=True)
    update_datetime = DateTimeField(auto_now=True)
    resolution = CharField(
        max_length=30, validators=[validate_resolution]
    )
    size = PositiveIntegerField()
    is_private = BooleanField(default=False)
    tags = ManyToManyField("Tag", related_name="images")
    author = ForeignKey(
        settings.AUTH_USER_MODEL, related_name="images", on_delete=PROTECT
    )
    description = TextField()

    def save(self, *args, **kwargs) -> None:
        w, h = get_image_dimensions(self.image)
        self.resolution = f"{w}x{h}"
        self.size = self.image.size
        super().save(*args, **kwargs)
        image_uploaded.delay(self.image.path)

    def delete(self, *args, **kwargs) -> None:
        image_deleted.delay(self.image.path)
        super().delete(*args, **kwargs)
