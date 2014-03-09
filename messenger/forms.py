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
                                                help_text='You can select more than one person.',
                                                widget=forms.CheckboxSelectMultiple)
    content = forms.CharField(widget=forms.Textarea, help_text='Be as detailed or brief as you want. '
                                                               'Messages are always anonymous.',
                              label='Message')

    password = forms.CharField(widget=forms.PasswordInput, help_text='If you would like to see replies and continue '
                                                                     'communications with the officer, please enter '
                                                                     'a password here. You will be assigned a random '
                                                                     'user ID.', required=False)
    password_again = forms.CharField(widget=forms.PasswordInput, required=False,
                                     help_text='Type your password again to make sure you have it right.')

    def clean(self):
        cleaned_data = super(MessageForm, self).clean()
        password = cleaned_data.get('password')
        password_again = cleaned_data.get('password_again')

        if password:
            if password_again:
                if password != password_again:
                    # Only do something if both passwords do not match.
                    msg = "Passwords must match."
                    self._errors["password"] = self.error_class([msg])
                    self._errors["password_again"] = self.error_class([msg])

                    # These fields are no longer valid. Remove them from the
                    # cleaned data.
                    del cleaned_data["password"]
                    del cleaned_data["password_again"]
            else:

                # Only do something if both passwords do not match.
                msg = "Please type your password twice to ensure correctness"
                self._errors["password"] = self.error_class([msg])
                self._errors["password_again"] = self.error_class([msg])

                # These fields are no longer valid. Remove them from the
                # cleaned data.
                del cleaned_data["password"]
                del cleaned_data["password_again"]

        return cleaned_data


class ReplyForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, help_text='Reply to this conversation. People who can view this '
                                                               'conversation will be able to see your message.',
                              label='Message')