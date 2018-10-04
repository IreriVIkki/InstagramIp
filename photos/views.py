from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .email import send_welcome_email
from django.views.generic import CreateView
from .forms import UserRegistrationForm


# Create your views here.

class RegisterUserView(CreateView):


def home(request):
    return render(request, 'index.html')
