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
from rest_framework.response import Response



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
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class CreatePost(LoginRequiredMixin, CreateAPIView):
    serializer_class = PostSerializer


class LikeView(LoginRequiredMixin, ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    # def get_queryset(self):
    #     date_from_str = self.request.query_params.get("date_from")
    #     date_to_str = self.request.query_params.get("date_to")
    #     date_from, date_to = convert_str_to_date(date_from_str, date_to_str)
    #     date_list = []
    #     for query in Like.objects.all():
    #         year, month, day = query.timestamp.year, query.timestamp.month, query.timestamp.day
    #         query_date = datetime(year, month, day)
    #         if date_from <= query_date <= date_to:
    #             date_list.append(query)
    #     queryset = ListAsQuerySet(date_list, model=Like)
    #     return queryset


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


# class TestList(ListAPIView):
#     serializer_class = TestSerializer
#
#     def get_queryset(self):
#         queryset = TestModel.objects.all()
#         date_from = self.request.query_params.get("date_from")
#         date_to = self.request.query_params.get("date_to")
#         if date_from is not None and date_to is not None:
#             date_from = date_from.split("-")
#             date_from_list = str_list_int(date_from)
#             date_to = date_to.split("-")
#             date_to_list = str_list_int(date_to)
#
#         print(date_from_list, date_to_list)
#         if date_from is not None and date_to is not None:
#             print("!"*10)
#             date_list = []
#             for query in TestModel.objects.all():
#                 print(query.timestamp.day)
#                 year, month, day = query.timestamp.year, query.timestamp.month, query.timestamp.day
#                 # print(type(query.timestamp.year), type(datetime(2022, 2, 2)))
#                 if datetime(date_from_list[0], date_from_list[1], date_from_list[2]) \
#                         < datetime(year, month, day) \
#                         < datetime(date_to_list[0], date_to_list[1], date_to_list[2]):
#                     date_list.append(query)
#             queryset = ListAsQuerySet(date_list, model=TestModel)
#             print(queryset)
#         return queryset

