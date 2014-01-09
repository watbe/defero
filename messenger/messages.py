__author__ = 'Wayne'
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect, render
from messenger.forms import MessageForm
from messenger.models import Message, Conversation
from datetime import datetime


def new_message(request, output=None):
    if not output:
        output = dict()

    if 'message_form' not in output:
        output['message_form'] = MessageForm()

    if request.method == 'POST':  # If the form has been submitted...
        form = MessageForm(request.POST)  # A form bound to the POST data
        if request.POST and form.is_valid():
            conversation = Conversation()
            conversation.save()
            message = Message(content=form.cleaned_data['content'],
                              time_posted=datetime.now(),
                              conversation_id=conversation.id)
            message.save()
            url = "/messages/" + conversation.id
            return HttpResponseRedirect(url)  # Redirect to a success page.
        return render(request, 'front_page.html', {'message_form': form}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")  # Redirect to a success page.


    return render_to_response('front_page.html', output, context_instance=RequestContext(request))