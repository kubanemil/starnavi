from django.shortcuts import HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from .models import Post, Like, UserActivity
from .serializer import PostSerializer, LikeSerializer, UserActivitySerializer
from .service import *
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.middleware import csrf
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status


def logout_user(request):
    logout(request)
    return HttpResponse("Successfully Logged Out.")


class SignUp(CreateView):
   form_class = UserCreationForm
   success_url = reverse_lazy('login')
   template_name = 'registration/signup.html'


@login_required
def main(request):
    hi = "Hi, There!"
    return HttpResponse(hi)


def redirect_to_main(request):
    return redirect('main')


class PostView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class CreatePost(LoginRequiredMixin, CreateAPIView):
    serializer_class = PostSerializer


class LikeView(LoginRequiredMixin, ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class Analytics(LoginRequiredMixin, ListAPIView):

    def get(self, request, pk, format=None):
        date_from_str = self.request.query_params.get("date_from")
        date_to_str = self.request.query_params.get("date_to")
        date_from, date_to = convert_str_to_date(date_from_str, date_to_str)

        the_post = Post.objects.all()[int(pk)-1]
        like_dict = return_date_like_json(the_post, date_from, date_to)
        like_json = json.dumps(like_dict)
        loaded_like = json.loads(like_json)
        return Response(loaded_like)


class PutLike(LoginRequiredMixin, CreateAPIView):
    serializer_class = LikeSerializer


class UpdateRetrievePost(LoginRequiredMixin, RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UserActivityView(LoginRequiredMixin, ListAPIView):
    serializer_class = UserActivitySerializer
    queryset = UserActivity.objects.all()


# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }
#
# from rest_framework_simplejwt.views import TokenObtainPairView
# class APILoginView(TokenObtainPairView):
#     def post(self, request, format=None):
#         data = request.data
#         response = Response()
#         username = data.get('username', None)
#         password = data.get('password', None)
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 data = get_tokens_for_user(user)
#                 response.set_cookie(
#                     key=settings.SIMPLE_JWT['AUTH_COOKIE'],
#                     value=data["access"],
#                     expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
#                     secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
#                     httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
#                     samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
#                 )
#                 csrf.get_token(request)
#                 response.data = {"Success": "Login successfully", "data": data}
#                 return response
#             else:
#                 return Response({"No active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)
