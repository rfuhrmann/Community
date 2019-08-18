from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from users.models import Friendship
from django.contrib.auth import get_user_model
User = get_user_model()


def validate_domainonly_username(username):
    if not User.objects.filter(username=username).exists():
        raise ValidationError(_("User does not exist"))
    return username


def validate_domainonly_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError(_("Email already used"))
    return email


def validate_user_not_active(username):
    if not User.objects.filter(username=username):
        raise ValidationError(_("User not exist"))
    user = User.objects.get(username=username)
    if user:
        if not user.is_active:
            raise ValidationError(_("User was deleted"))
    else:
        raise ValidationError(_("User not found"))
    return username
