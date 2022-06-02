from rest_framework import serializers
from .models import Post, Like, UserActivity, User
from datetime import datetime

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'date', 'user', 'like_amount']


class LikeSerializerModify(serializers.ModelSerializer):
    date = serializers.DateField(write_only=True)

    class Meta:
        model = Like
        fields = '__all__'


class LikeSerializerView(serializers.ModelSerializer):
    user = serializers.CharField()
    post = serializers.CharField()

    class Meta:
        model = Like
        fields = ['user', 'post', 'liked']

class UserActivitySerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    class Meta:
        model = UserActivity
        fields = '__all__'
