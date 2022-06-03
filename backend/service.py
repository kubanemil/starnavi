import datetime
import json
from .models import Post, Like, UserActivity, User


class ListAsQuerySet(list):
    """Class to convert list of instances into QuerySet object."""
    def __init__(self, *args, model, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self  # filter ignoring, but you can impl custom filter

    def order_by(self, *args, **kwargs):
        return self

def str_list_int(list):
    """Function to convert list of string into list of integers."""
    int_list = []
    for element in list:
        try:
            element = int(element)
            int_list.append(element)
        except ValueError:
            pass
    return int_list


def convert_str_to_date(date_from_str, date_to_str):
    """Function to convert string date into date object.
    Example:
        '2020-12-31' ==>> datetime.date(2020, 12, 31) """
    date_from_list = date_to_list = []
    if date_from_str is not None or date_to_str is not None:
        date_from_str = date_from_str.split("-")
        date_from_list = str_list_int(date_from_str)
        date_to_str = date_to_str.split("-")
        date_to_list = str_list_int(date_to_str)

    if len(date_from_list) < 3:
        start_date = datetime.date(1990, 1, 1)
    elif len(date_from_list) >= 3:
        start_date = datetime.date(date_from_list[0],date_from_list[1],date_from_list[2])
    if len(date_to_list) < 3:
        end_date = datetime.date(3000, 1, 1)
    elif len(date_from_list) >= 3:
        end_date = datetime.date(date_to_list[0],date_to_list[1],date_to_list[2])
    return start_date, end_date


def return_date_like_json(the_post, date_from, date_to):
    """Converts date object into jsonified object."""
    post_likes = the_post.likes.all()  #Get all likes for given post
    dates = []
    for like in post_likes:
        date = like.date
        dates.append(date)
    dates = sorted(dates)
    likes_by_day_list = []
    unique_dates = list(set(dates))

    if len(unique_dates) != 0:
        for date in unique_dates:
            if date_from <= date <= date_to:
                date_like_amount = 0
                for i in range(len(dates)):
                    if dates[i] == date:
                        date_like_amount += 1
                likes_by_day_list.append([date, date_like_amount])

    date_likes_dict = {}
    for likes_by_day in likes_by_day_list:
        date = str(likes_by_day[0])
        like_amount = likes_by_day[1]
        date_likes_dict[date] = like_amount
    the_dict = {
        "post_id": the_post.id,
        "post_title": the_post.title,
        "like_analytics_by_date": date_likes_dict
    }
    like_json = json.dumps(the_dict)
    loaded_like_json = json.loads(like_json)
    return loaded_like_json


def return_an_like_instances(user_id, post_id):
    """Checks the user_id and post_id variables, and if they valid
    returns the correct instance of Like model."""
    if user_id is not None and post_id is not None:
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        instances = Like.objects.filter(post=post, liker=user)
    elif user_id is None and post_id is not None:
        post = Post.objects.get(id=post_id)
        instances = Like.objects.filter(post=post)
    elif user_id is not None and post_id is None:
        user = User.objects.get(id=user_id)
        instances = Like.objects.filter(liker=user)
    else:
        instances = [Like.objects.first(), ]
    return instances

