from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as DjangoLoginView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from django.views.generic.list import MultipleObjectMixin

from app.forms import RegisterForm, FollowerForm
from app.models import UserProfile, UserFollow


class Index(TemplateView):
    template_name = 'index.html'


    def get_object(self):
        print(self.request.user.profile)
        print(self.request.user.profile.__dict__)
        user = self.request.user.profile
        return user



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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = UserProfile.objects.filter(user__id = self.kwargs['pk'])
        return context





class ProfileListView(ListView):
    model = UserProfile
    form_class = FollowerForm
    fields = '__all__'
    template_name = 'profile_list.html'
    ordering = ['-id']

    def get_queryset(self):
        objects = UserProfile.objects.filter(user__is_superuser=False)
        user = self.request.user
        following = UserFollow.objects.filter(follower=user).values_list('following', flat=True)
        for object in objects:
            setattr(object, 'following', object.id in following)
        return objects

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FollowerForm
        return context













# ____________________________________________________________________________________________________



class FollowUnfollowView(View):
    http_method_names = ['post']

    def post(self, request, pk, *args, **kwargs):
        following = User.objects.get(pk=pk)
        user = request.user
        user_follow = UserFollow.objects.filter(follower=user, following=following).first()
        if user_follow is None:
            UserFollow.objects.create(follower=user, following=following)
        else:
            user_follow.delete()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)






    def get_success_url(self):
        return reverse('profile-list')






