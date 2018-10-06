from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Photo


class NewPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ['uploaded_by']


class ProfileForm(forms.Form):
    pass
