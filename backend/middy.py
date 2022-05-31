from datetime import timedelta as td
from datetime import datetime
from django.utils import timezone
# from django.conf import settings
# from django.db.models.expressions import F
import time
from .models import UserActivity

class AccountLoginMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # last_activity = request.session.get('last-activity')
            # not last_activity or
            # too_old_time = timezone.now() - td(seconds=10)
            if True:
                UserActivity.objects.create(user=request.user, timestamp=datetime.now())
                time.sleep(10)
            request.session['last-activity'] = timezone.now().isoformat()

        response = self.get_response(request)

        return response
