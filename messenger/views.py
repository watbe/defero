from django.shortcuts import render_to_response, HttpResponseRedirect, render, RequestContext
from messenger.forms import LoginForm, MessageForm
from django.views.decorators.cache import never_cache, cache_control
from django.contrib.auth import logout
from django.contrib.auth import login


@never_cache
@cache_control(no_cache=True, must_revalidate=True, max_age=0, no_store=True)
def home(request, output=None):
    if not output:
        output = dict()
    output['title'] = "Write a message"
    if 'login_form' not in output:
        output['login_form'] = LoginForm()
    if 'message_form' not in output:
        output['message_form'] = MessageForm()
    return render_to_response('front_page.html', output, context_instance=RequestContext(request))


def log_in(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = LoginForm(request.POST)  # A form bound to the POST data
        if request.POST and form.is_valid():
            user = form.login()
            if user:
                login(request, user)
                return HttpResponseRedirect("/user")  # Redirect to a success page.
        return home(request, {'login_form': form})
    else:
        if request.user.is_authenticated():
            # prevent logged in users from logging in again?
            return HttpResponseRedirect("/user")
        form = LoginForm()

    return render(request, 'front_page.html', {'form': form}, context_instance=RequestContext(request))


@never_cache
@cache_control(no_cache=True, must_revalidate=True, max_age=0, no_store=True)
def user_page(request):
    """
    We aggressively prevent caching to avoid another user on the computer viewing a cached page that
    displays a private message.
    """
    if request.user.is_authenticated():
        output = dict()
        output['success_message'] = "You are now logged in. Remember to log out when you are finished."
        return home(request, output)
    else:
        return HttpResponseRedirect("/")


def user_logout(request):
    """
    Simple logout functionality.
    """
    logout(request)

    output = dict()
    output['success_message'] = "You have been successfully logged out."
    return home(request, output)