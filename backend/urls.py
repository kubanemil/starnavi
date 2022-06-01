from django.urls import path, re_path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('main/', views.main, name='main'),
    path('accounts/', include('django.contrib.auth.urls'), name="login"),
    path("signup/", views.SignUp.as_view(), name='signup'),
    path("accounts/profile/", views.redirect_to_main),
    path("logout/", views.logout_user),
    path("posts/", views.PostView.as_view(), name='post_view'),
    path("create_post/", views.CreatePost.as_view(), name='post_create'),
    path("update_post/<pk>", views.UpdateRetrievePost.as_view(), name='post_update'),
    path("likes/", views.LikeView.as_view(), name='like_view'),
    path("put_like/", views.PutLike.as_view(), name='put_like'),
    path("analytics/<pk>/", views.Analytics.as_view()),
    path("activity/<pk>/", views.UserActivityView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
