from django.contrib import admin

# Register your models here.
from app.models import *


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ['follower']


@admin.register(UserBlock)
class UserBlockAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'description','cover_image', 'created_at']