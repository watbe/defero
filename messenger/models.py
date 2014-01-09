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

    # Hidden from user
    message_id = models.AutoField(primary_key=True)
    time_posted = models.DateTimeField()
    conversation_id = models.CharField(max_length=16)


class Message(BaseMessage):
    """
    Messages are messages sent from the reporter to the officer. Replies are different classes.
    """
    author = models.ForeignKey(get_user_model())


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
    id = models.CharField(max_length=16, default=uuid.uuid4(), primary_key=True)

    recipients = models.ManyToManyField(Officer)  # These are people allowed to view the conversation. Cannot be changed
    messages = models.ManyToManyField(BaseMessage)  # A list of all messages belonging to this conversation.
    subject = models.CharField(max_length=200)  # A headline for the conversation, can be changed by either party