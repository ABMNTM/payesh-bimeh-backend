from django import forms
from common.utils.forms import BootstrapModelForm, BootstrapReadOnlyModelForm

from main.types import RelationshipType
from main.models import Person


class ReadOnlyPersonForm(BootstrapReadOnlyModelForm):
    class Meta:
        model = Person
        exclude = ("is_household_head", "household")


class PersonForm(BootstrapModelForm):
    class Meta:
        model = Person
        exclude = ("is_household_head", "household")


class CreatePersonForm(BootstrapModelForm):
    class Meta:
        model = Person
        exclude = ("is_household_head", "household")


class CreateHouseholdPersonForm(BootstrapModelForm):
    class Meta:
        model = Person
        exclude = ("national_code", "household", "is_household_head", "relation_type")
