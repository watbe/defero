__author__ = 'Wayne'
from uuid import uuid4
from messenger.models import Conversation, BaseMessage, Officer
from django.contrib.auth import get_user_model
import re
from datetime import datetime
from random import randint
from django.core.mail import send_mail

# import the logging library
import logging
logger = logging.getLogger(__name__)


class MessengerException(Exception):
    pass

class MessengerNotFoundException(MessengerException):
    pass

def uuid_check(uuid):
    """
    Checks if a UUID is valid based on the expected format for a UUID. It does not check against the database.
    """
    uuid4hex = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}\Z', re.I)
    if not uuid4hex.match(uuid):
        return False
    else:
        return True


def new_conversation():
    """
    Helper function for starting a new function. May include new things later.
    """
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


def get_officer(user):
    """
    Tests for whether the user is an officer and returns the officer object if it is, otherwise returns
    a MessengerNotFoundException exception
    """
    try:
        return Officer.objects.get(user=user)
    except (Officer.DoesNotExist, Officer.MultipleObjectsReturned):
        raise MessengerNotFoundException


def new_reply(uuid, content, user):
    """
    Adds a new reply to a conversation
    """
    conversation = get_conversation_or_false(uuid, user)
    if not conversation:
        return False

    try:
        officer = get_officer(user)
        message = BaseMessage.objects.create(author=officer,
                                             content=content,
                                             time_posted=datetime.now(),
                                             conversation_id=conversation.uuid)
    except MessengerNotFoundException:
        message = BaseMessage.objects.create(content=content,
                                             time_posted=datetime.now(),
                                             conversation_id=conversation.uuid)

    message.save()
    conversation.messages.add(message)
    conversation.save()

    return True


def make_new_anonymous_user(password):
    """
    Makes a new user with a random user id. Password is supplied.
    """

    # TODO account for the fact that someone might maliciously create more than 999999 accounts
    random_number = randint(1000000, 9999999)
    while get_user_model().objects.filter(username=random_number).exists():
        random_number = randint(1000000, 9999999)

    # Whatever happens, we must not give someone else access to another account
    if get_user_model().objects.filter(username=random_number).exists():
        raise MessengerException

    new_user = get_user_model().objects.create(username=random_number.__str__())
    new_user.set_password(password)
    new_user.save()

    return new_user


def get_conversation_list_for_user(user_id):
    """
    Returns a list of conversations that the user can access
    """

    # TODO test access
    return Conversation.objects.filter(recipients__pk=user_id)


def send_email_notifications(recipients, sender):
    """
    Based on a list of recipients, this method will check if an email address is given, and if there is one, will
    send an email notification with simple details about a new message on the website.
    """

    for user in recipients.all():
        if user.email:
            if not sender == user:
                send_mail('New message on Messenger', 'Hi there, this is a simple notification to let you know that '
                                                  'you have received a new message on Messenger. Please log in to '
                                                  'view the new message.'
                                                  '\nKindest regards - Automated email',
                      'messenger@lab273.com',[user.email], fail_silently=True)