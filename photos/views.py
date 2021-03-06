from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from .email import send_welcome_email
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import User, Photo, UserProfile, Comment, PhotoLikes, Followers
from .forms import NewPhotoForm, ProfileForm, CommentForm, LikeForm, FollowForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage


def new_post(request):
    user = request.user
    if request.user.is_authenticated:
        if request.method == 'POST':
            f = NewPhotoForm(request.POST, request.FILES)
            print(f.is_valid())
            if f.is_valid():
                f.save()
                photo = Photo.objects.last()
                photo.save_photo(user)
                return redirect('home')
        else:
            f = NewPhotoForm()
        return render(request, 'new_upload.html', {'form': f})
    return redirect('home')


def signup(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            print('trinh')
            return redirect('login')

    else:
        f = UserCreationForm()

    return render(request, 'registration/registration_form.html', {'form': f})


def home(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            like_form = LikeForm(request.POST)
            print(like_form.is_valid())
            if comment_form.is_valid():
                comment_form.save()
                photo_id = comment_form.cleaned_data['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                comment = Comment.objects.last()
                comment.save_comment(user, photo)
                print('comment')
                return redirect('home')
            elif like_form.is_valid():
                print('like')
                like_form.save()
                photo_id = like_form.cleaned_data['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                like = PhotoLikes.objects.last()
                like.save_like(photo, user)
                return redirect('home')
        else:
            comment_form = CommentForm()
            like_form = CommentForm()
        user = User.objects.get(pk=user.id)
        f = Photo.all_photos()
        # fol = user.following.all()
        # f = [i for i in Photo.user_photos(user)]
        # for i in fol:
        #     for p in i.photos.all():
        #         f.append(p)
        # print(fol)
        context = {
            'user': user,
            'photos': f,
            'c_form': comment_form,
            'l_form': like_form,
        }
    else:
        return redirect('signup')
    return render(request, 'index.html', context)


def edit_profile(request):
    form = ProfileForm()
    user = request.user
    if request.user.is_authenticated():
        if request.method == "POST":
            try:
                profile = user.profile
                form = ProfileForm(instance=profile)
                form = ProfileForm(
                    request.POST, request.FILES, instance=profile)
                if form.is_valid():
                    update = form.save(commit=False)
                    update.user = user
                    update.save()
            except:
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


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        photos = Photo.user_photos(user.username)
        print(photos)
        context = {
            'user': user,
            'photos': photos
        }
    return render(request, 'profile.html', context)


def other_profile(request, user_id):
    user = request.user
    o_user = User.objects.get(pk=user_id)
    photos = Photo.objects.filter(uploaded_by=o_user)
    if request.method == 'POST':
        f_form = FollowForm(request.POST)
        print(f_form.is_valid())
        if f_form.is_valid():
            if len(user.followers.all()) > 0:
                follow = Followers.objects.get(follower=user)
                follow.unfollow_user(user)
                print(follow)
            else:
                f_form.save()
                follow = Followers.objects.last()
                follow.follow_user(user, o_user)
                print(follow)
            return redirect('home')
    context = {
        'o_user': o_user,
        'photos': photos
    }
    return render(request, 'other_profile.html', context)


def search_results(request):
    # check if the input field exists and that ic contains data
    if 'photo' in request.GET and request.GET['photo']:
        # get the data from the search input field
        search_term = request.GET.get('photo')
        searched_photos = Photo.filter_by_search_term(search_term)
        caption = f'Search results for {search_term}'
        if len(searched_photos) == 0:
            searched_photos = Photo.all_photos()
            caption = 'No Results Found'
        search_context = {
            'photos': searched_photos,
            'caption': caption,
        }
        return render(request, 'search.html', search_context)
    else:
        photos = Photo.all_photos()
        search_context = {
            'photos': photos,
            'caption': 'No Results Matched Your Search!! Discover More Photos'
        }
        return render(request, 'explore.html', search_context)


def explore(request):
    photos = Photo.all_photos()
    search_context = {
        'photos': photos,
    }
    return render(request, 'explore.html', search_context)
