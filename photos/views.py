from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from .email import send_welcome_email
from django.views.generic import CreateView
from .forms import UserRegistrationForm


# Create your views here.

class RegisterUserView(CreateView):
    form = UserRegistrationForm
    template_name = 'registration/registration_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseForbidden()

        return super(RegisterUserView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form, request):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        return render(request, 'index.html')


def home(request):
    return render(request, 'index.html')
