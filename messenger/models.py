from django.db import models
from django.contrib.auth import get_user_model


class Officer(models.Model):
    user = models.OneToOneField(get_user_model())
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role



class Message(models.Model):
    # Editable by user
    recipients = models.ManyToManyField(Officer)
    author = models.ForeignKey(get_user_model(), blank=True)
    content = models.TextField()

    # Hidden from user
    time_posted = models.DateTimeField()
    conversation_id = models.IntegerField()