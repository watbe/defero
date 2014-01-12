__author__ = 'Wayne'
from uuid import uuid4
from messenger.models import Conversation, AnonymousMessage
import re


def uuid_check(uuid):
    uuid4hex = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}\Z', re.I)
    if not uuid4hex.match(uuid):
        return False
    else:
        return True


def new_conversation():
    return Conversation.objects.create(uuid=uuid4())


def new_conversation_from_message(content, time):
    """
    Creates a new conversation from an initial message by making a blank conversation
    and adding the message as the conversation's first message
    """
    # We create a new conversation (as this is not a Reply) and give it a unique id
    conversation = new_conversation()

    # We create a message based on the form content and the new conversation
    message = AnonymousMessage.objects.create(content=content, time_posted=time)
    message.conversation_id = conversation.uuid.__str__()

    return conversation, message