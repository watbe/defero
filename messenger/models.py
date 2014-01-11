from django.db import models
from django.contrib.auth import get_user_model
import uuid


class Officer(models.Model):
    user = models.OneToOneField(get_user_model())
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role


class BaseMessage(models.Model):
    # Editable by user
    content = models.TextField()

    time_posted = models.DateTimeField()
    conversation_id = models.CharField(max_length=16, blank=True)


class Message(BaseMessage):
    """
    Messages are messages sent from the reporter to the officer. Replies are different classes.
    """
    author = models.ForeignKey(get_user_model(), blank=True)


class Reply(BaseMessage):
    """
    A reply is a message sent from the officer to reporter.
    """
    author = models.ForeignKey(Officer)


class Conversation(models.Model):
    """
    Conversations are identified by a unique UUID. All messages are associated with a conversation.
    Messages have sequential IDs as they are never exposed to the user.
    """
    uuid = models.CharField(max_length=16)

    recipients = models.ManyToManyField(Officer, related_name='officer_link')  # These are people allowed to view the conversation. Cannot be changed
    messages = models.ManyToManyField(BaseMessage, related_name='messages_link')  # A list of all messages belonging to this conversation.
    subject = models.CharField(max_length=200)  # A headline for the conversation, can be changed by either party