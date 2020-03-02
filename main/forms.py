
from django import forms
from django.contrib.auth import authenticate
from . import models

class AuthenticationForm(forms.Form):
    password = forms.CharField(
        strip=False, widget=forms.PasswordInput
    )

    