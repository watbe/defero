__author__ = 'Wayne'
from django import forms
from django.contrib.auth import authenticate
from messenger.models import Officer


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        user = self.login()
        if not user or not user.is_active:
            raise forms.ValidationError('Sorry, that login was invalid. Please try again.')
        return self.cleaned_data

    def login(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class MessageForm(forms.Form):
    recipients = forms.ModelMultipleChoiceField(Officer.objects.all(),
                                                help_text='You can send messages to any officer(s) you feel comfortable'
                                                          ' with, and only the specified people will be able to view '
                                                          'your message. ')
    content = forms.CharField(widget=forms.Textarea, help_text='A message can be as long or as short as you like. '
                                                               'Please be as descriptive as possible where necessary.')


class ReplyForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, help_text='Reply to this conversation. People who can view this '
                                                               'conversation will be able to see your message.')