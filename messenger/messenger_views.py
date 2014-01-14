__author__ = 'Wayne'
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from messenger.forms import MessageForm, ReplyForm
from messenger import views
import messenger.messenger_methods as messenger
from django.contrib.auth import get_user_model
from datetime import datetime

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

            # Now we add the message to the conversation.
            conversation.messages.add(message)

            # We set access permissions for this conversation. If the user isn't anonymous, we add the user to
            # the access list.
            if not request.user.is_anonymous():
                author = get_user_model().objects.get(username=request.user.username)
                conversation.recipients.add(author)
            elif form.cleaned_data['password']:
                new_user = messenger.make_new_anonymous_user(form.cleaned_data['password'])
                conversation.recipients.add(new_user)
                output['new_user'] = new_user.username

            # We now add the officers from the recipients list in the submitted form
            for officer in form.cleaned_data['recipients']:
                conversation.recipients.add(officer.user)

            # Commit the new message and conversation to the database
            conversation.save()
            message.save()

            output['conversation'] = conversation
            output['logged_in'] = True

            return render_to_response('message_success.html', output, context_instance=RequestContext(request))

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

    conversation = messenger.get_conversation_or_false(uuid, request.user)
    if not conversation:
        return not_found(request)

    if not output:
        output = dict()

    if 'reply_form' not in output:
        output['reply_form'] = ReplyForm()

    output['conversation'] = conversation
    output['authorised_users'] = []
    for reader in conversation.recipients.all():
        officer = messenger.get_officer_or_false(reader)
        if officer:
            output['authorised_users'].append(officer.__str__())
        else:
            output['authorised_users'].append("Anonymous User")

    return render_to_response('message_conversation.html', output, context_instance=RequestContext(request))


def list_messages(request):
    if request.user.is_anonymous():
        return not_found(request)
    else:
        output = dict()
        output['conversation_list'] = messenger.get_conversation_list_for_user(request.user.id)
        return render_to_response('message_list.html', output, context_instance=RequestContext(request))


def reply(request, uuid):
    """
    Processes replies
    """

    # TODO access control

    # Extra check to make sure UUID is in correct format
    if not messenger.uuid_check(uuid):
        return not_found(request)

    if request.method == 'POST':

        form = ReplyForm(request.POST)

        if request.POST and form.is_valid():

            # new_reply automatically checks whether the user is an officer or not
            if messenger.new_reply(uuid, form.cleaned_data['content'], request.user):
                msg = 'Your reply has been added to the conversation.'
                return read_message(request, uuid, {'success_message': msg})
            else:
                return not_found(request)
        else:
            return read_message(request, uuid, {'reply_form': form})


def not_found(request):
    """
    This is the not found method.
    """
    response = render_to_response('message_not_found.html', context_instance=RequestContext(request))
    response.status_code = 404
    return response