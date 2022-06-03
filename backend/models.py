from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import datetime
# Create your models here.


class Post(models.Model):
    """Blog model"""
    title = models.CharField(max_length=100)
    text = RichTextField()
    date = models.DateField(default=datetime.date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def like_amount(self):
        """Method that returns the amount of likes of the post."""
        return len(Like.objects.filter(post=self))


class Like(models.Model):
    """Like status object"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)

    class Meta:
        """This will guarantee that every like by user
        for the post will be unique (non-repeating)."""
        unique_together = ('post', 'liker')

    def __str__(self):
        """Example:
        'Aleksey Mashinov - 10 tips to become successful person' """
        return self.liker.username + " - " + self.post.title

class UserActivity(models.Model):
    """Model that contains last 5 requests of the user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.CharField(max_length=200, default="GET 'None'")
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.user.username + " - " + str(self.timestamp)
