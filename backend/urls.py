from django.urls import path
from . import views
from . import token_views

urlpatterns = [
    path('login/', token_views.LoginApiView.as_view(), name='token_obtain_pair'),
    path('refresh/', token_views.RefreshApi.as_view(), name='token_refresh'),
    path("signup/", views.SignUp.as_view(), name='signup'),
    path("logout/", views.logout_user),
    path("posts/", views.PostView.as_view(), name='post_view'),
    path("create_post/", views.CreatePost.as_view(), name='post_create'),
    path("update_post/<pk>", views.UpdateRetrievePost.as_view(), name='post_update'),
    path("likes/", views.LikeView.as_view(), name='like_view'),
    path("put_like/", views.PutLike.as_view(), name='put_like'),
    path("analytics/<pk>/", views.Analytics.as_view()),
    path("activity/<pk>/", views.UserActivityView.as_view()),
]
