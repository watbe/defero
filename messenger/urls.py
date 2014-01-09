__author__ = 'Wayne'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'defero.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^user$', 'messenger.views.user_page'),

                       url(r'^logout$', 'messenger.views.user_logout'),
                       url(r'^login', 'messenger.views.log_in'),

                       url(r'^messages/new$', 'messenger.messages.new_message'),

                       # Everything else will match home.
                       url(r'^', 'messenger.views.home'),

                       )