from datetime import datetime

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


SLUG_VALIDATOR = RegexValidator(r'^[-a-zA-Z0-9_]+$')


def year_validator(year):
    if year > datetime.now().year:
        raise ValidationError(
            f'Введенный {year} год не может быть больше текущего!'
        )
