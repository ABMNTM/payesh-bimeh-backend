from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from main.types import EnrollmentStatus
from main.models.enrollment import Enrollment


class DashboardView(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        queryset = Enrollment.objects.select_related("offer", "offer__contract").filter(
            guardian=request.user
        )
        for enrollment in queryset:
            if enrollment.status == EnrollmentStatus.PENDING:
                enrollment.status_color = "secondary"
            elif enrollment.status == EnrollmentStatus.SUBMITTED:
                enrollment.status_color = "primary"
            else:
                enrollment.status_color = "success"
        return render(request, "pages/dashboard.html", {"enrollments": queryset})
