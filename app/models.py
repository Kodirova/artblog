from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to='static/profile_picture')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)


    def __str__(self):
        return self.user.username


class UserFollow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return self.follower.username


class UserBlock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_user')

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_of_post')
    description = models.CharField(max_length=1024)
    cover_image = models.ImageField(upload_to='static/post', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class PostComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)

    def __str__(self):
        return self.comment
