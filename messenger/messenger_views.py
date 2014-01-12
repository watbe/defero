__author__ = 'Wayne'
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect, render
from messenger.forms import MessageForm, ReplyForm
from messenger.models import AnonymousMessage, Conversation, Officer
from messenger import views
import messenger.messenger_methods as messenger
from django.contrib.auth import get_user_model
from datetime import datetime
import re

# import the logging library
import logging
logger = logging.getLogger(__name__)


def new_message(request, output=None):
    if not output:
        output = dict()

    if 'message_form' not in output:
        output['message_form'] = MessageForm()

    if request.method == 'POST':

        form = MessageForm(request.POST)

        if request.POST and form.is_valid():

            conversation, message = messenger.new_conversation_from_message(
                content=form.cleaned_data['content'],
                time=datetime.now())

            # If the user is logged in, and is an Officer, we associate the message with the Officer.
            # TODO This should only happen in Replies as all initial messages should be anonymous
            if not request.user.is_anonymous:
                try:
                    author = Officer.objects.get(user=request.user)
                    message.author = author
                except Officer.DoesNotExist:
                    pass

            # Now we add the message to the conversation.
            conversation.messages.add(message)

            # We set access permissions for this conversation. If the user isn't anonymous, we add the user to
            # the access list.
            if not request.user.is_anonymous:
                author = get_user_model().objects.get(username=request.user.username)
                conversation.recipients.add(author)

            # We now add the officers from the recipients list in the submitted form
            for officer in form.cleaned_data['recipients']:
                conversation.recipients.add(officer.user)

            # Commit the new message and conversation to the database
            conversation.save()
            message.save()

            # Redirect to the page to display the message
            url = "/messages/" + message.conversation_id + "/"
            return HttpResponseRedirect(url)  # Redirect to a success page.

        # If the form is invalid, redirect to the message page with the incorrect form
        return views.home(request, {'message_form': form})
    else:
        return HttpResponseRedirect("/")  # Redirect to message page


def read_message(request, uuid, output=None):
    """
    Note, we must not differentiate between access denied (403's) and not found (404) to prevent people from
    trying to 'guess' URLs, as implausible as that may be...
    """

    # Extra check to make sure UUID is in correct format
    if not messenger.uuid_check(uuid):
        return not_found(request)

    # TODO access control
    if not output:
        output = dict()

    if 'reply_form' not in output:
        output['reply_form'] = ReplyForm()

    try:
        conversation = Conversation.objects.get(uuid=uuid)
        output['conversation'] = conversation

        if request.method == 'POST':  # If a reply has been submitted, add it.
            pass

        return render_to_response('message_conversation.html', output, context_instance=RequestContext(request))
    except Conversation.DoesNotExist:
        return not_found(request)

def reply(request):
    pass


def not_found(request):
    """
    This is the not found method.
    """
    response = render_to_response('message_not_found.html')
    response.status_code = 404
    return response