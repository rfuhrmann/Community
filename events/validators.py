from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
User = get_user_model()


def validate_domainonly_username(username):
    if not User.objects.filter(username=username).exists():
        raise ValidationError(_("User does not exist"))
    return username
