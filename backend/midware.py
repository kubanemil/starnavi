from django.utils import timezone
import time
from .models import UserActivity


class AccountLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            the_req = "%s '%s'" % (request.method, request.build_absolute_uri())
            UserActivity.objects.create(user=request.user, request=the_req, timestamp=timezone.now())
            while len(UserActivity.objects.filter(user=request.user)) > 5:
                UserActivity.objects.filter(user=request.user)[0].delete()
            request.session['last-activity'] = timezone.now().isoformat()

        response = self.get_response(request)

        return response
