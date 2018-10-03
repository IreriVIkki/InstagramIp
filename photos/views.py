from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect


# Create your views here.
def home(request):
    return render(request, 'index.html')
