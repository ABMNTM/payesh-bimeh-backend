from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models.enrollment import Enrollment


class DashboardView(LoginRequiredMixin, View):
    login_url = "login/"
    redirect_field_name = "redirect_to"

    def get(self, request):
        queryset = Enrollment.objects.select_related("contract").filter(
            guardian=request.user
        )
        return render(request, "dashboard.html", {"enrollments": queryset})
