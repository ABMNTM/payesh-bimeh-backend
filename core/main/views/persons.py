from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import OuterRef
from django.db import transaction

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from main.types import RelationshipType
from main.forms.person import CreatePersonForm, PersonForm, ReadOnlyPersonForm
from main.models import Person, FamilyRelationship


class PersonsView(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get_context(self):
        queryset = Person.objects.annotate(
            relation=FamilyRelationship.objects.filter(
                related_person=self.request.user.person,
                person_id=OuterRef("id")
            ).values("relationship_type")[:1]
        ).filter(is_household_head=False, household__user=self.request.user)
        dependants = [
            {
                "id": person.id,
                "relation": (
                    RelationshipType(person.relation).label
                    if person.relation else ""
                ),
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

    def safe_clean(self, obj, form):
        try:
            obj.full_clean()
        except ValidationError as e:
            self.rebase_errors(e.error_dict, form)

    def rebase_errors(self, errors, form):
        for errors in errors.values():
            for error in errors:
                form.add_error("relationship", error)

    def get(self, request):
        form = CreatePersonForm()
        form.fields.get("relationship").error_messages
        return render(request, "pages/create_person.html", {"form": form})

    @transaction.atomic
    def post(self, request):
        form = CreatePersonForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            household_person = self.request.user.person
            relationship = data.pop("relationship")

            # make person instance without saving
            person = Person.objects.create(
                **data, is_household_head=False,
                household=household_person
            )

            # make relationship instance without saving
            relationship_instance = FamilyRelationship(
                person=person,
                related_person=household_person,
                relationship_type=relationship,
            )
            # check constraints
            self.safe_clean(relationship_instance, form)
            # save instance
            relationship_instance.save()

            # redirect to persons page with success message
            messages.success(request, "اطلاعات فرد جدید با موفقیت ثبت شد.")
            return redirect("/persons")
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
        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات فردی با موفقیت بروزرسانی شد.")
            return redirect("/persons")
        return render(request, "pages/update_person.html", {"form": form})
