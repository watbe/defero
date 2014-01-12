from django.contrib import admin
from messenger.models import Officer, AnonymousMessage

# Register your models here.
admin.site.register(Officer)
admin.site.register(AnonymousMessage)
