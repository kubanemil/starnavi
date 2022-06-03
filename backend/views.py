from .service import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveDestroyAPIView
from .serializer import PostSerializer, LikeSerializerView,\
    UserActivitySerializer, LikeSerializerCreate


class PostView(ListAPIView):
    """API page that returns list of Blog model's instances."""
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class CreatePost(CreateAPIView):
    """Endpoint to create Blog instances."""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Custom create method that defaults user field to user that made this request."""
        post = Post.objects.create(title=request.data['title'], text=request.data['text'],\
                                   user=User.objects.get(username=request.user.username))
        post.save()
        serializer = self.serializer_class(post)
        return Response(serializer.data)


class LikeView(ListAPIView):
    """API that returns Like model's instances."""
    queryset = Like.objects.all()
    serializer_class = LikeSerializerView
    permission_classes = [IsAuthenticated]


class PutLike(CreateAPIView):
    """API to create Like model's instance"""
    serializer_class = LikeSerializerCreate
    permission_classes = [IsAuthenticated]


class RemoveLike(RetrieveDestroyAPIView):
    """API to remove Like model's instance"""
    queryset = Like.objects.all()
    serializer_class = LikeSerializerCreate
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """Custom retrieve method that uses URL parameters.
        URL should looks like this:
        'api/remove_like/?user_id=23&post_id=47'
        All parameters are optional and if no parametes are given,
        then it will return first Like object.
        """
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
    """API that returns UserActivity model's instances."""
    serializer_class = UserActivitySerializer
    queryset = UserActivity.objects.all()
    permission_classes = [IsAuthenticated]


class Analytics(ListAPIView):
    """API to monitor how many likes was made to the post in some period.
    URL Example:
    'api/analytics/77/?date_from=2022-02-30&date_to=2022-04-31'
    where 77 is ID of the post to monitor, date_from is the date from which
    to monitor, and date_to is the end date.
    date_from and date_to are optional parameters. IF they are not specified,
    API will return all existing analytics of the post.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        date_from_str = self.request.query_params.get("date_from")
        date_to_str = self.request.query_params.get("date_to")
        date_from, date_to = convert_str_to_date(date_from_str, date_to_str)

        the_post = Post.objects.all()[int(pk)-1]
        like_json = return_date_like_json(the_post, date_from, date_to)
        return Response(like_json)
