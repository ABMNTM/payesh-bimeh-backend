from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "با موفقیت خارج شدید.")
        return redirect("login")
