from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate


class LoginView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect("/dashboard")
        return render(request, "pages/login.html")

    def post(self, request):
        personnel_code = request.POST.get("personnel_code")
        password = request.POST.get("password")
        user = authenticate(request, personnel_code=personnel_code, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            messages.error(request, "کد پرسنلی یا رمز عبور نادرست است.")
            return render(request, "pages/login.html")
