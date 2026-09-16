from django.views import View
from django.shortcuts import redirect
from django.utils import timezone as tz

from main.models import Enrollment
from main.types import EnrollmentStatus


class OIDCLoginView(View):
    def get(self, request):
        current_enrollment = Enrollment.objects.filter(
            guardian=request.user,
            status=EnrollmentStatus.PENDING,
            offer__contract__poll_start_date__lt=tz.now(),
            offer__contract__poll_end_date__gt=tz.now(),
        ).order_by("id").last()
        if not current_enrollment:
            return redirect("/dashboard")
        return redirect("/survey")
