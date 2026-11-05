from django import forms
from django.contrib.auth.models import User

class MessageForm(forms.Form):
    message = forms.CharField(
        label="",
        max_length=1000,
        widget=forms.Textarea(attrs={'placeholder': 'Write message here...', 'class': 'message-input-field'})
    )

class ThreadForm(forms.Form):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'select2-widget',
                'data-ajax-url': '/messages/inbox/search-users/',
                'data-maximum-selection-length': '6',
            }
        ),
        label="Select up to 6 users to chat with:",
        required=False
    )