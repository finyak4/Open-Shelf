from django.core.exceptions import ValidationError

def validate_four_digits(value):
    if not (1000 <= value <= 9999):
        raise ValidationError('Value must be a 4-digit number.')