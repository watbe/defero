from django.db import models
from django.contrib.auth import get_user_model


class Officer(models.Model):
    """
    We are not extending User for Officer
    """
    user = models.OneToOneField(get_user_model())
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role


class BaseMessage(models.Model):
    """
    All messages are anonymous unless they are written by an officer
    """
    content = models.TextField()

    time_posted = models.DateTimeField()
    conversation_id = models.CharField(max_length=40, blank=True)

    author = models.ForeignKey(Officer, blank=True, null=True)


class Conversation(models.Model):
    """
    Conversations are identified by a unique UUID. All messages are associated with a conversation.
    Messages have sequential IDs as they are never exposed to the user.
    """
    uuid = models.CharField(max_length=40) # UUID length is max 16 chars

    recipients = models.ManyToManyField(get_user_model(), related_name='recipient_set')  # These are people allowed to view the conversation. Cannot be changed
    messages = models.ManyToManyField(BaseMessage, related_name='message_set')  # A list of all messages belonging to this conversation.
    subject = models.CharField(max_length=200)  # A headline for the conversation, can be changed by either party