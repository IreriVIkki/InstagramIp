from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from .email import send_welcome_email
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import User, Photo, UserProfile
from .forms import NewPhotoForm, ProfileForm


# Create your views here.

def new_post(request):
    user = request.user
    if request.user.is_authenticated:
        if request.method == 'POST':
            f = NewPhotoForm(request.POST, request.FILES)
            if f.is_valid():
                f.save()
                cap = f.cleaned_data['caption']
                photo = Photo.objects.get(caption=cap)
                print(photo)
                photo.upladed_by = user
                photo.save()
                return redirect('home')
        else:
            f = NewPhotoForm()
        return render(request, 'new_upload.html', {'form': f})
    return redirect('home')


def signup(request):

    if request.user.is_authenticated:
        return redirect('home', username=request.user.username)

    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('signup')

    else:
        f = UserCreationForm()

    return render(request, 'account/register.html', {'form': f})


def home(request):
    if request.user.is_authenticated:
        user = request.user
        photos = Photo.all_photos()
        context = {
            'user': user,
            'photos': photos
        }
    return render(request, 'index.html', context)


def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            print(form.is_valid())
            if form.is_valid():
                form.save()
                name = form.cleaned_data['name']
                profile = UserProfile.objects.get(name=name)
                print(profile)
                profile.user = user
                profile.save()
                return redirect('home')
        else:
            form = ProfileForm()

        context = {
            'form': form,
            'user': user,
        }
    return render(request, 'profile_edit.html', context)


def profile(request, username):
    if request.user.is_authenticated:
        user = request.user
        photos = Photo.user_photos(username)
        print(photos)
        context = {
            'user': user,
            'photos': photos
        }
    return render(request, 'profile.html', context)
