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
    recipients = forms.ModelMultipleChoiceField(Officer.objects.all())
    content = forms.CharField(widget=forms.Textarea)