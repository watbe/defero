__author__ = 'Wayne'
from django.shortcuts import render_to_response, RequestContext


def privacy(request):
    return render_to_response('privacy_security.html', context_instance=RequestContext(request))


def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))


def faq(request):
    return render_to_response('faq.html', context_instance=RequestContext(request))