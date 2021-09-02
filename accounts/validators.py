from django.core.exceptions import ValidationError


def validate_is_digits(value: str):
    if not value.isdigit():
        raise ValidationError(
            '%(value)s is not a phone number.',
            params={'value': value},
        )


def validate_email(value: str):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(value)
        return True
    except ValidationError:
        return False
