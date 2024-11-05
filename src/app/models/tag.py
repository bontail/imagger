import re
from django.core.exceptions import ValidationError
from django.db.models import Model, CharField


def validate_only_ascii(value: str) -> None:
    reg = re.compile(r'^[^\x00-\x7F]+$')
    if not reg.match(value):
        raise ValidationError(f"Only ASCII characters are allowed ({value})")


class Tag(Model):
    name = CharField(
        primary_key=True, max_length=20, validators=[validate_only_ascii]
    )
