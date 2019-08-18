from django.db import models
from django.conf import settings
from users.models import Address
import datetime

# Create your models here.


class Place(models.Model):
    name = models.CharField(max_length=254, null=False, default="Place")
    description = models.CharField(max_length=254, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="places", null=True)


class Event(models.Model):
    CATEGORIES = (
        (1, "Other"),
        (2, "Sport"),
        (3, "Party"),
        (4, "Food"),
        (5, "Work"),
        (6, "Meeting"),
        (7, "Sauna"),
        (8, "Family"),
        (9, "SitSit")
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events", null=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=254, null=False, default="Event")
    description = models.TextField(null=True)
    category = models.IntegerField(null=False, choices=CATEGORIES)
    start_datetime = models.DateTimeField(null=True)
    end_datetime = models.DateTimeField(null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="events", null=True)
    # open, removed
    status = models.CharField(max_length=50, null=False, default="open")


class EventInvitation(models.Model):
    creation_datetime = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="invitations", null=True)
    request_datetime = models.DateTimeField(auto_now=True)
    response_datetime = models.DateTimeField(null=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name="event_invitations_requested", null=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name="event_invitations_receipt", null=True)
    # request, accepted, declined, removed
    status = models.CharField(max_length=20, null=False, default='request')
