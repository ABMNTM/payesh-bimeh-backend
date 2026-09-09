from django.contrib import messages
from django.db import IntegrityError, transaction

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms.person import CreatePersonForm, PersonForm, ReadOnlyPersonForm
from main.models import Person


class PersonsView(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get_context(self):
        queryset = Person.objects.filter(is_household_head=False, household__user=self.request.user)
        dependants = [
            {
                "id": person.id,
                "relation": person.get_relation_type_display,
                "form_values": ReadOnlyPersonForm(instance=person)
            } for person in queryset
        ]
        self_person = {
            "id": self.request.user.person.pk,
            "form": ReadOnlyPersonForm(instance=self.request.user.person)
        }
        return {
            "dependants": dependants, "self_person": self_person
        }

    def get(self, request):
        context = self.get_context()
        return render(request, "pages/persons.html", context)


class CreatePersonView(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        form = CreatePersonForm()
        return render(request, "pages/create_person.html", {"form": form})

    @transaction.atomic
    def post(self, request):
        form = CreatePersonForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                # redirect to persons page with success message
                messages.success(request, "اطلاعات فرد جدید با موفقیت ثبت شد.")
                return redirect("/persons")
        except IntegrityError:
            form.add_error("relation_type", "این فیلد برای سرپرست خانوار، الزامی نمی باشد.")
        return render(request, "pages/create_person.html", {"form": form})


class UpdatePersonsView(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get(self, request, pk):
        obj = get_object_or_404(Person, pk=pk)
        form = PersonForm(instance=obj)
        return render(request, "pages/update_person.html", {"form": form})

    def post(self, request, pk):
        obj = get_object_or_404(Person, pk=pk)
        form = PersonForm(request.POST, instance=obj)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "اطلاعات فردی با موفقیت بروزرسانی شد.")
                return redirect("/persons")
        except IntegrityError:
            form.add_error("relation_type", "این فیلد برای سرپرست خانوار، الزامی نمی باشد.")
        return render(request, "pages/update_person.html", {"form": form})
