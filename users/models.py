from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.utils.translation import gettext as _
from django.conf import settings
import datetime


# Create your models here.

class Address(models.Model):
    country = models.CharField(max_length=254, null=False, default="Country")
    postal_code = models.PositiveIntegerField(null=False, default=1)
    town = models.CharField(max_length=254, null=False, default="Town")
    street = models.CharField(max_length=254, null=False, default="Street")
    street_number = models.PositiveIntegerField(null=False, default=1)


# Extending User Model Using a Custom Model Extending AbstractUser
class User(AbstractUser):
    # attributes included in django model:
    # username
    # first_name
    # last_name
    # email
    # password
    # groups
    # user_permissions
    # is_staff
    # is_active
    # is_superuser
    # last_login
    # date_joined
    phone = models.CharField(max_length=50, null=True)
    logged_in = models.BooleanField(null=True)
    img = models.ImageField(null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="residents", null=True)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Friendship(models.Model):
    request_datetime = models.DateTimeField(auto_now=True)
    response_datetime = models.DateTimeField(null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendships_requested", null=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendships_receipt", null=True)
    # request, accepted, declined, removed
    status = models.CharField(max_length=20, null=False, default='request')


class Status(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="status", null=True)
    title = models.CharField(max_length=254, null=False, default="Title")
    message = models.TextField(null=True)
    datetime = models.DateTimeField(auto_now=True)


class Status_Comment(models.Model):
    message = models.TextField(null=False, default="Message")
    # date = models.DateTimeField(_("Date"), default=datetime.date.today)
    datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="status_comments", null=True)
    status = models.ForeignKey(Status, on_delete=models.CharField, related_name="comments", null=True)

    class Meta:
        ordering = ['-datetime']


class Privacy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    contact = models.BooleanField(default=False)
    address = models.BooleanField(default=False)
    status_comments = models.BooleanField(default=False)
    friends = models.BooleanField(default=False)
    discussions = models.BooleanField(default=False)
    events = models.BooleanField(default=False)
    groups = models.BooleanField(default=False)
