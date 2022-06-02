from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import datetime
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = RichTextField()
    date = models.DateField(default=datetime.date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    @property
    def like_amount(self):
        return len(Like.objects.filter(post=self))

    def like_amount_daily(self, date):
        return len(Like.objects.filter(post=self, timestamp=date))


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    liked = models.BooleanField(default=False)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.user.username + " - " + self.post.title

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.CharField(max_length=200, default="GET 'None'")
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.user.username + " - " + str(self.timestamp)
