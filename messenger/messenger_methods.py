__author__ = 'Wayne'
from uuid import uuid4
from messenger.models import Conversation


def new_conversation():
    return Conversation.objects.create(uuid=uuid4())