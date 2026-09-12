from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils import timezone as tz

from main.models import Enrollment
from main.types import EnrollmentStatus


class LoginView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect("/dashboard")
        return render(request, "pages/login.html")

    def handle_login_redirect(self, request):
        current_enrollment = Enrollment.objects.filter(
            guardian=request.user,
            status=EnrollmentStatus.PENDING,
            offer__contract__poll_start_date__lt=tz.now(),
            offer__contract__poll_end_date__gt=tz.now(),
        ).order_by("id").last()
        if not current_enrollment:
            return redirect("/dashboard")
        return redirect("/survey")

    def post(self, request):
        personnel_code = request.POST.get("personnel_code")
        password = request.POST.get("password")
        user = authenticate(request, personnel_code=personnel_code, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "با موفقیت وارد شدید.")
            return self.handle_login_redirect(request)
        else:
            messages.error(request, "کد پرسنلی یا رمز عبور نادرست است.")
            return render(request, "pages/login.html")
