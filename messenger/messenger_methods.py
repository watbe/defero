__author__ = 'Wayne'
from uuid import uuid4
from messenger.models import Conversation, BaseMessage, Officer
from django.contrib.auth import get_user_model
import re
from datetime import datetime
from random import randint

# import the logging library
import logging
logger = logging.getLogger(__name__)


def uuid_check(uuid):
    uuid4hex = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}\Z', re.I)
    if not uuid4hex.match(uuid):
        return False
    else:
        return True


def new_conversation():
    return Conversation.objects.create(uuid=uuid4())


def get_conversation_or_false(uuid, user):
    """
    All conversation requests must include the requesting user.
    """
    try:
        conversation = Conversation.objects.get(uuid=uuid)
        if not conversation.recipients.filter(id=user.id).exists():
            return False
        return conversation
    except Conversation.DoesNotExist:
        return False
    except Conversation.MultipleObjectsReturned:
        return False


def new_conversation_from_message(content, time=None):
    """
    Creates a new conversation from an initial message by making a blank conversation
    and adding the message as the conversation's first message
    """
    # We create a new conversation (as this is not a Reply) and give it a unique id
    conversation = new_conversation()

    if not time:
        time = datetime.now()

    # We create a message based on the form content and the new conversation
    message = BaseMessage.objects.create(content=content, time_posted=time)
    message.conversation_id = conversation.uuid.__str__()

    return conversation, message


def get_officer_or_false(user):
    """
    Tests for whether the user is an officer and returns the officer object if it is, otherwise returns False
    """
    try:
        officer = Officer.objects.get(user=user)
        return officer
    except Officer.DoesNotExist:
        return False


def new_reply(uuid, content, user):
    conversation = get_conversation_or_false(uuid, user)
    if not conversation:
        return False

    officer = get_officer_or_false(user)

    if officer:
        message = BaseMessage.objects.create(author=officer,
                                             content=content,
                                             time_posted=datetime.now(),
                                             conversation_id=conversation.uuid)
    else:
        message = BaseMessage.objects.create(content=content,
                                             time_posted=datetime.now(),
                                             conversation_id=conversation.uuid)

    message.save()
    conversation.messages.add(message)
    conversation.save()

    return True


def make_new_anonymous_user(password):

    random_number = randint(100000, 999999)
    while get_user_model().objects.filter(username=random_number).exists():
        random_number = randint(100000, 999999)

    new_user = get_user_model().objects.create(username=random_number.__str__(), password=password)

    return new_user