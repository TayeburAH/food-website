from django.core.validators import ValidationError
from validate_email import validate_email


def validate_email_SMTP(email):
    if not validate_email(email, verify=True):
        raise ValidationError('Invalid Email')
    else:
        return email
