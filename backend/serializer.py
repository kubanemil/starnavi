from rest_framework import serializers
from .models import Post, Like, UserActivity


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'date', 'user', 'like_amount']


class LikeSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'liker']


class LikeSerializerView(serializers.ModelSerializer):
    liker = serializers.CharField()
    post = serializers.CharField()

    class Meta:
        model = Like
        fields = "__all__"


class UserActivitySerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = UserActivity
        fields = '__all__'
