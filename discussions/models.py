from django.db import models
# from django.utils.translation import gettext as _
from django.conf import settings


# Create your models here.


class Discussion(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="discussions", null=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=254, null=False, default="Discussion Title")
    message = models.TextField(null=True)
    # open, closed, removed
    status = models.CharField(max_length=50, null=False, default="open")


class Discussion_Comment(models.Model):
    message = models.TextField(null=False, default="Message")
    datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="discussion_comments",
                             null=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="comments", null=True)
    # open, removed
    status = models.CharField(max_length=50, null=False, default="open")
