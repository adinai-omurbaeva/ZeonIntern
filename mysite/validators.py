import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    """ Проверка типа файла загружаемого в качестве иконки "наши преимущества" """
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.png', '.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_amount(value):
    """ Проверка товара, чтобы число не было отрицательным или 0 """
    if value < 1:
        raise ValidationError('Минимум 1')
