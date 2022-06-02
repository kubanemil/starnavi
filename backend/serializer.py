from rest_framework import serializers
from .models import Post, Like, UserActivity, User
from datetime import datetime

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'timestamp', 'user', 'like_amount']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class UserActivitySerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    class Meta:
        model = UserActivity
        fields = '__all__'
