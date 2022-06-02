import datetime
import json

class ListAsQuerySet(list):

    def __init__(self, *args, model, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self  # filter ignoring, but you can impl custom filter

    def order_by(self, *args, **kwargs):
        return self

def str_list_int(list):
    int_list = []
    for l in list:
        try:
            l = int(l)
            int_list.append(l)
        except:
            pass
    return int_list


def convert_str_to_date(date_from_str, date_to_str):
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
    post_likes = the_post.likes.all()  #Get all likes for given post
    dates = []
    for like in post_likes:
        date = like.timestamp
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
    like_json = json.dumps(date_likes_dict)
    loaded_like_json = json.loads(like_json)
    return like_json

# start_date_likes_amount = 0
#         for i in range(len(dates)): #every dateobject is one like
#             the_date = datetime.date(dates[i].year, dates[i].month, dates[i].day)
#             if the_date.year == start_date.year and the_date.month == start_date.month \
#                     and the_date.day == start_date.day:
#                 if date_from <= the_date <= date_to:
#                     start_date_likes_amount += 1
#             else:
#                 day_likes = [start_date, start_date_likes_amount]
#                 likes_by_day_list.append(day_likes)
#                 print("likes_by_day_list:")
#                 print(likes_by_day_list)
#                 start_date = dates[i]
#                 start_date_likes_amount = 0
#         day_likes = [start_date, start_date_likes_amount]
#         likes_by_day_list.append(day_likes)