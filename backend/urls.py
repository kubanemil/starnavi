"""urls for API"""
from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.PostView.as_view(), name='post_view'),
    path("create_post/", views.CreatePost.as_view(), name='post_create'),
    path("likes/", views.LikeView.as_view(), name='like_view'),
    path("put_like/", views.PutLike.as_view(), name='put_like'),
    path("remove_like/", views.RemoveLike.as_view(), name='remove_like'),
    path("analytics/<pk>/", views.Analytics.as_view()),
    path("activity/<pk>/", views.UserActivityView.as_view()),
]
#
