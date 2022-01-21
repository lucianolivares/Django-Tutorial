import uuid

from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.TextField()
    image = models.ImageField(
        upload_to='images/',
        default='images/default.png'
    )
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='network_post', null=True
    )
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("network:post_detail", args=[str(self.identifier)])

    @property
    def get_comments(self):
        own_comments = Comment.objects.filter(post=self)
        return own_comments
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commets', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user}-->{self.body} '
