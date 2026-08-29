from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models.person import Person


class PersonsView(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        dependants = Person.objects.filter(
            is_household_head=False, household__user=self.request.user
        )
        self_person = self.request.user.person
        context = {"dependants": dependants, "self_person": self_person}
        return render(request, "pages/persons.html", context)
