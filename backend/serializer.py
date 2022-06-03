from rest_framework import serializers
from .models import Post, Like, UserActivity


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model."""
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'date', 'user', 'like_amount']


class LikeSerializerCreate(serializers.ModelSerializer):
    """Serializer for Like model while creating/deleting an instance."""
    class Meta:
        model = Like
        fields = ['id', 'post', 'liker']


class LikeSerializerView(serializers.ModelSerializer):
    """Serializer for Like model to view only."""
    liker = serializers.CharField()
    post = serializers.CharField()

    class Meta:
        model = Like
        fields = "__all__"


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for UserActivity model."""
    user = serializers.CharField()

    class Meta:
        model = UserActivity
        fields = '__all__'
