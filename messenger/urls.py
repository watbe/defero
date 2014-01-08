__author__ = 'Wayne'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'defero.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', 'messenger.views.home'),
                       )