from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from .serializer import PostSerializer, LikeSerializerView,\
                        UserActivitySerializer, LikeSerializerCreate
from .service import *
from rest_framework.permissions import IsAuthenticated


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


class LikeView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializerView
    permission_classes = [IsAuthenticated]


class PutLike(CreateAPIView):
    serializer_class = LikeSerializerCreate
    permission_classes = [IsAuthenticated]


class RemoveLike(RetrieveDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializerCreate
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user_id = self.request.query_params.get("user_id")
        post_id = self.request.query_params.get("post_id")
        instances = return_an_like_instances(user_id=user_id, post_id=post_id)
        if len(instances) >= 1:
            instance = instances[0]
        else:
            return Response({"error": "No matching instance with such parameters"})
        serializer = self.get_serializer(instance)
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
        like_json = return_date_like_json(the_post, date_from, date_to)
        return Response(like_json)



