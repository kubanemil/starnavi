from rest_framework import serializers
from .models import Post, Like
from datetime import datetime

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'timestamp', 'user', 'like_amount']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'