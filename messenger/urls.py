__author__ = 'Wayne'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^user$', 'messenger.views.user_page'),

                       url(r'^logout$', 'messenger.views.user_logout'),
                       url(r'^user/login', 'messenger.views.log_in'),

                       url(r'^messages/$', 'messenger.messenger_views.list_messages'),
                       url(r'^messages/new$', 'messenger.messenger_views.new_message'),
                       url(r'^messages/(?P<uuid>.*)/reply$', 'messenger.messenger_views.reply'),
                       url(r'^messages/(?P<uuid>.*)/$', 'messenger.messenger_views.read_message'),

                       # Everything else will match home.
                       url(r'^', 'messenger.views.home'),

                       )