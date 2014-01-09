from django.shortcuts import render_to_response, HttpResponseRedirect
from messenger.forms import LoginForm, MessageForm
from django.views.decorators.cache import never_cache, cache_control
from django.contrib.auth import logout


def home(request):
    output = dict({})
    output['content'] = "hello"
    output['title'] = "Send a message"
    output['login_form'] = LoginForm()
    output['message_form'] = MessageForm()
    return render_to_response('front_page.html', output)


@never_cache
@cache_control(no_cache=True, must_revalidate=True, max_age=0, no_store=True)
def user_page(request):
    """
    We aggressively prevent caching to avoid another user on the computer viewing a cached page that
    displays a private message.
    """
    if request.user.is_authenticated():
        output = dict({})
        output['content'] = "Logged in"
        return render_to_response('front_page.html', output)
    else:
        return HttpResponseRedirect("/")


def user_logout(request):
    """
    Simple logout functionality.
    """
    logout(request)
    return render_to_response('logged_out.html')
