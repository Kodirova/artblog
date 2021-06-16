
from django.contrib.auth.views import LoginView as DjangoLoginView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import *

from app.forms import RegisterForm
from app.models import UserProfile


class Index(TemplateView):
    template_name = 'index.html'


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'signup.html'


    def get_success_url(self):
        return reverse('login')


class LoginView(DjangoLoginView):
    template_name = 'signin.html'

    def get_success_url(self):
        return reverse('index')


class PasswordResetView(PasswordResetView):
    template_name = 'restore.html'



class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'restore-email-sent.html'



class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.htm'



# ________________________________________________________________________________________________________________

class UserProfileCreateView(UpdateView):
    model = UserProfile
    template_name = 'profile.html'
    fields = ['picture']

    def get_object(self, queryset=None):
        return self.request.user.profile


    def get_success_url(self):
        return reverse('index')


class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'profile-detail.html'
    fields = '__all__'

    def get_object(self):
        print(self.request.user.profile)
        print(self.request.user.profile.__dict__)
        return self.request.user.profile

# ____________________________________________________________________________________________________
