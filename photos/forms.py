from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password(self):
        cd = self.cleaned_data

        if cd['confirm_password'] != cd['password']:
            raise ValidationError("Passwords don't match")
        return cd['confirm_password']
