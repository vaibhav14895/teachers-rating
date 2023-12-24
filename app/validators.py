from django.core.exceptions import ValidationError

def validate_username(value):

    if len(value) < 5:
        raise ValidationError("Username must be at least 5 characters long.")
    if not value.isalnum():
        raise ValidationError("Username must contain only letters and numbers.")