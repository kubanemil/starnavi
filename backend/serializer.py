from rest_framework import serializers
from .models import Post, Like, UserActivity
import datetime


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'date', 'user', 'like_amount']


class LikeSerializerCreate(serializers.ModelSerializer):
    # date = serializers.DateField(write_only=True, default=datetime.date.today)
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'liked']

class LikeSerializerModify(serializers.ModelSerializer):
    # date = serializers.DateField(write_only=True, default=datetime.date.today)
    post = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    date = serializers.CharField(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'date', 'liked', ]
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
