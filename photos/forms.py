from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Photo, UserProfile, Comment, PhotoLikes, Followers


class NewPhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        exclude = ['uploaded_by']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        list_display = []


class CommentForm (forms.ModelForm):
    photo_id = forms.IntegerField()

    class Meta:
        model = Comment
        exclude = ['author', 'photo']
        list_display = []


class LikeForm(forms.ModelForm):
    photo_id = forms.IntegerField()

    class Meta:
        model = PhotoLikes
        exclude = ['photo', 'liked_by']
        list_display = []


class FollowForm(forms.ModelForm):
    class Meta:
        model = Followers
        exclude = ['follower', 'following']
        list_display = []
