__author__ = 'Wayne'
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect, render
from messenger.forms import MessageForm
from messenger.models import Message, Conversation
from datetime import datetime
import uuid


def new_message(request, output=None):
    if not output:
        output = dict()

    if 'message_form' not in output:
        output['message_form'] = MessageForm()

    if request.method == 'POST':  # If the form has been submitted...
        form = MessageForm(request.POST)  # A form bound to the POST data
        if request.POST and form.is_valid():
            conversation = Conversation.objects.create(uuid=uuid.uuid4())
            message = Message.objects.create(
                content=form.cleaned_data['content'],
                time_posted=datetime.now(),
                author=request.user)
            message.conversation_id = conversation.uuid.__str__()
            conversation.messages.add(message)
            conversation.save()
            message.save()
            url = "/messages/" + message.conversation_id
            return HttpResponseRedirect(url)  # Redirect to a success page.
        return render(request, 'front_page.html', {'message_form': form}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")  # Redirect to a success page.


    return render_to_response('front_page.html', output, context_instance=RequestContext(request))


def read_message(request, uuid=None):
    """
    Note, we must not differentiate between access denied (403's) and not found (404) to prevent people from
    trying to 'guess' URLs, as implausible as that may be...
    """
    try:
        conversation = Conversation.objects.get(uuid=uuid)
        return render_to_response('message_conversation.html', {'conversation': conversation},
                                  context_instance=RequestContext(request))
    except Conversation.DoesNotExist:
        return not_found(request)


def not_found(request):
    """
    This is the not found method.
    """
    response = render_to_response('message_not_found.html')
    response.status_code = 404
    return response