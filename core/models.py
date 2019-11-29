from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    body = models.TextField(max_length=140)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,  related_name='author')
    date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User)
    def __str__(self):
        return self.body

class Hashtag(models.Model):
    name = models.CharField(max_length=200)
    posts = models.ManyToManyField(Post)
    def __str__(self):
        return self.name