from django.utils import timezone
import time
from .models import UserActivity


class AccountLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            the_req = "%s '%s'" % (request.method, request.build_absolute_uri())
            # request.META['Authentication'] =

            # UserActivity.objects.create(user=request.user, timestamp=timezone.now())
            print("!"*10)
            print(the_req)
            request.session['last-activity'] = timezone.now().isoformat()
        else:
            print("Bullshit")

        response = self.get_response(request)

        return response

 # "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1NDE2OTUxOSwiaWF0IjoxNjU0MDgzMTE5LCJqdGkiOiJkOGRlMGYwNWU0Zjg0MTNkYjM3NjU1ZDE3MmVlMWY3MyIsInVzZXJfaWQiOjJ9.gF4jJdub8MQsh_sgbAXtathyGO1BzhRacfG0VinDl7I",
 #    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU0MDgzNDE5LCJpYXQiOjE2NTQwODMxMTksImp0aSI6Ijg0NWNhNzRiZDI3ZTRjODY5YjRjYjJhZDZmZTk1NzZkIiwidXNlcl9pZCI6Mn0.gs1yF05Hnd5sIbc-LPZa7VGeYsGr9-I0nqJz-qempD8"