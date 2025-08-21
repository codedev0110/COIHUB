from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class  Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    languages = models.ManyToManyField(Language, related_name="languages")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    code= models.TextField(blank=True, null=True)
    comments = models.ManyToManyField('Comment', related_name='comments')

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.text[:20]}"
