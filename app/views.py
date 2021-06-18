from django.contrib.auth.mixins import LoginRequiredMixin
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
from app.models import UserProfile, UserFollow, Post, PostComments, UserBlock


class Index(LoginRequiredMixin, TemplateView):
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

class UserProfileCreateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'profile.html'
    fields = ['picture']

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('index')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'profile-detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = User.objects.filter(profile__id=self.kwargs['pk']).first()

        context['following'] = UserFollow.objects.filter(following=user,
                                                         follower=self.request.user).exists()
        context['blocked'] = UserBlock.objects.filter(blocked = user, user =self.request.user ).exists()
        context['profile'] = self.request.user.profile
        context['posts'] = Post.objects.all()

        context['comments'] = PostComments.objects.all()
        return context


class ProfileListView(LoginRequiredMixin, ListView):
    model = UserProfile
    fields = '__all__'
    template_name = 'profile_list.html'
    ordering = ['-id']

    def get_queryset(self):
        objects = UserProfile.objects.filter(user__is_superuser=False)
        user = self.request.user
        following = UserFollow.objects.filter(follower=user).values_list('following', flat=True)
        blocked =  UserBlock.objects.filter(user=user).values_list('blocked', flat=True)
        for object in objects:
            setattr(object, 'following', object.id in following)
            setattr(object, 'blocked', object.id in blocked)
        return objects


# ____________________________________________________________________________________________________
class FollowUnfollowView(LoginRequiredMixin, View):
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


# ____________________________________________________________________________________________________________________

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['description', 'cover_image']
    template_name = 'post-create.html'

    def form_valid(self, form):
        print(1)
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        object = UserProfile.objects.filter(user__id=self.kwargs['pk'])
        return object

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile-detail', kwargs={'pk': self.request.user.profile.pk})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = '__all__'
    template_name = 'post-update.html'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    fields = '__all__'
    template_name = 'profile-detail.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile-detail', kwargs={'pk': self.request.user.profile.pk})


class PostCommentCreateView(LoginRequiredMixin, CreateView):
    model = PostComments
    fields = ['comment']
    template_name = 'comment-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(id=self.kwargs['pk'])
        context['comments'] = PostComments.objects.filter(post=self.kwargs['pk'])
        print(context)
        return context

    def form_valid(self, form):
        print(1)
        comment = form.save(commit=False)
        user = self.request.user
        comment.user = user
        comment.post = Post.objects.get(id=self.kwargs['pk'])
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile-detail', kwargs={'pk': self.request.user.profile.pk})


# _____________________________________________________________________________________________________________________
class BlockUnblockView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, pk, *args, **kwargs):
        blocked = User.objects.get(pk=pk)
        user = request.user
        user_block = UserBlock.objects.filter(user=user, blocked=blocked).first()
        if user_block is None:
            UserBlock.objects.create(user=user, blocked=blocked)
        else:
            user_block.delete()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    def get_success_url(self):
        return reverse('profile-list')