__author__ = 'Wayne'
from django.shortcuts import render_to_response, RequestContext


def new_message(request, output=None):
    if not output:
        output = dict()

    output['title'] = "Write a message"
    if 'login_form' not in output:
        output['login_form'] = LoginForm()
    output['message_form'] = MessageForm()

    return render_to_response('front_page.html', output, context_instance=RequestContext(request))