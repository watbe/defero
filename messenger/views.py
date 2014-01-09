from django.shortcuts import render_to_response
from messenger.forms import LoginForm, MessageForm


def home(request):
    output = dict({})
    output['content'] = "hello"
    output['title'] = "Send a message"
    output['login_form'] = LoginForm()
    output['message_form'] = MessageForm()
    return render_to_response('front_page.html', output)