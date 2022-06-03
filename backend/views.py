from django.shortcuts import redirect
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from .models import Post, Like, UserActivity, User
from .serializer import PostSerializer, LikeSerializerView,\
                            LikeSerializerModify, UserActivitySerializer, LikeSerializerCreate
from .service import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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


class UpdateRetrievePost(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class LikeView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializerView
    permission_classes = [IsAuthenticated]


class PutLike(CreateAPIView):
    serializer_class = LikeSerializerCreate
    permission_classes = [IsAuthenticated]
    # def post(self, request, *args, **kwargs):
    #     try:
    #         self.create(request, *args, **kwargs)
    #     except:
    #         return redirect('update_like', pk=1)



class UpdateLike(RetrieveUpdateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializerModify
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserActivityView(ListAPIView):
    serializer_class = UserActivitySerializer
    queryset = UserActivity.objects.all()
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



