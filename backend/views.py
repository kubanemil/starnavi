from django.shortcuts import HttpResponse
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from .models import Post, Like, UserActivity, User
from .serializer import PostSerializer, LikeSerializer, UserActivitySerializer
from .service import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def logout_user(request):
    logout(request)
    return HttpResponse("Successfully Logged Out.")


class SignUp(CreateView):
   form_class = UserCreationForm
   success_url = reverse_lazy('login')
   template_name = 'registration/signup.html'


class PostView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class CreatePost(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        post = Post.objects.create(title=request.data['title'], text=request.data['text'],\
                                   user=User.objects.get(username=request.user.username))
        post.save()
        serializer = self.serializer_class(post)
        return Response(serializer.data)
        # else:
        #     return Response("Authentication credentials were not provided.")

class LikeView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]


class Analytics(ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        date_from_str = self.request.query_params.get("date_from")
        date_to_str = self.request.query_params.get("date_to")
        date_from, date_to = convert_str_to_date(date_from_str, date_to_str)

        the_post = Post.objects.all()[int(pk)-1]
        like_dict = return_date_like_json(the_post, date_from, date_to)
        like_json = json.dumps(like_dict)
        loaded_like = json.loads(like_json)
        return Response(loaded_like)


class PutLike(CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]


class UpdateLike(RetrieveUpdateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]


class UpdateRetrievePost(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class UserActivityView(ListAPIView):
    serializer_class = UserActivitySerializer
    queryset = UserActivity.objects.all()
    permission_classes = [IsAuthenticated]


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.middleware import csrf
from django.conf import settings
from django.contrib.auth import authenticate

class LoginApiView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        print("!"*10)
        print(request.data)
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            if user.is_active:
                response = Response(serializer.validated_data, status=status.HTTP_200_OK)
                access_token = "Bearer " + str(serializer.validated_data['access'])
                refresh_token = str(serializer.validated_data['refresh'])
                response.set_cookie(
                                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                                    value=serializer.validated_data['access'],
                                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY']
                )
                # response.set_cookie(
                #     key='refresh_token',
                #     value=refresh_token,
                #     httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY']
                # )
                csrf.get_token(request)
            else:
                return Response({"No active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)
        return response

# import rest_framework_simplejwt.authentication.JWTAuthentication