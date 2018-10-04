from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from .email import send_welcome_email
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from .models import User


# Create your views here.

def signup(request):

    if request.user.is_authenticated:
        return redirect('djangobin:profile', username=request.user.username)

    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('signup')

    else:
        f = UserCreationForm()

    return render(request, 'account/register.html', {'form': f})


def home(request):
    return render(request, 'index.html')
