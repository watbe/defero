from django.shortcuts import render_to_response, HttpResponseRedirect, render, RequestContext
from messenger.forms import LoginForm, MessageForm
from django.views.decorators.cache import never_cache, cache_control
from django.contrib.auth import logout
from django.contrib.auth import login


@never_cache
@cache_control(no_cache=True, must_revalidate=True, max_age=0, no_store=True)
def home(request):
    output = dict({})
    output['content'] = "hello"
    output['title'] = "Send a message"
    output['login_form'] = LoginForm()
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
        return render(request, 'front_page.html', {'form': form})
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
        output = dict({})
        output['content'] = "Logged in"
        return render_to_response('front_page.html', output, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")


def user_logout(request):
    """
    Simple logout functionality.
    """
    logout(request)
    return render_to_response('logged_out.html', context_instance=RequestContext(request))
