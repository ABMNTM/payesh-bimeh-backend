from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms.user import UserProfileForm
from accounts.models.user import User


class ProfileView(LoginRequiredMixin, UpdateView):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    model = User
    form_class = UserProfileForm
    template_name = "pages/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "اطلاعات پروفایل با موفقیت بروزرسانی شد.")
        return super().form_valid(form)
