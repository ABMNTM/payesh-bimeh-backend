from django.contrib import messages
from django.db import IntegrityError, transaction

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms.person import CreateHouseholdPersonForm, CreatePersonForm, PersonForm, ReadOnlyPersonForm
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
        if self.request.user.person_id:
            self_person = {
                "id": self.request.user.person.pk,
                "person_exists": True,
                "form": ReadOnlyPersonForm(instance=self.request.user.person)
            }
        else:
            self_person = {
                "person_exists": False,
            }
        return {
            "dependants": dependants, "self_person": self_person
        }

    def get(self, request):
        context = self.get_context()
        return render(request, "pages/persons.html", context)


class CreateHouseholdView(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        form = CreateHouseholdPersonForm()
        return render(request, "pages/create_person.html", {"form": form})

    def get_tracking_code(self):
        import random

        random_code = random.randint(10000000, 99999999)
        while Person.objects.filter(is_household_head=True, tracking_code=random_code).exists():
            random_code = random.randint(10000000, 99999999)
        return str(random_code)

    @transaction.atomic
    def post(self, request):
        form = CreateHouseholdPersonForm(request.POST)
        try:
            if form.is_valid():
                data = form.cleaned_data
                new_person = Person.objects.create(
                    **data,
                    is_household_head=True,
                    household=None,
                    tracking_code=self.get_tracking_code(),
                    national_code=self.request.user.national_code,
                )
                self.request.user.person = new_person
                self.request.user.save()
                # redirect to persons page with success message
                messages.success(request, "اطلاعات فرد جدید با موفقیت ثبت شد.")
                return redirect("/persons")
        except IntegrityError:
            form.add_error("relation_type", "این فیلد برای سرپرست خانوار، الزامی نمی باشد.")
        return render(request, "pages/create_person.html", {"form": form})


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
                data = form.cleaned_data
                Person.objects.create(
                    **data,
                    is_household_head=False,
                    household=request.user.person,
                    tracking_code=request.user.person.tracking_code
                )
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
