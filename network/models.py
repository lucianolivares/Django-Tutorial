from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    image = models.ImageField(
        upload_to='images/',
        default='images/default.png'
    )
    published = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='network_post'
    )

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.description
