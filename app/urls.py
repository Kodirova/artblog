from django.urls import path

from app.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/update', UserProfileCreateView.as_view(), name='profile-update'),
    path('profile/detail/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/list', ProfileListView.as_view(), name='profile-list'),
    path('follow/create/<int:pk>/', FollowUnfollowView.as_view(), name='follow-create'),
    path('post/create', PostCreateView.as_view(), name='post-create'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('comment/create/<int:pk>/', PostCommentCreateView.as_view(), name = 'comment-create'),
    path('block/create/<int:pk>/', BlockUnblockView.as_view(), name = 'block-create')


]
