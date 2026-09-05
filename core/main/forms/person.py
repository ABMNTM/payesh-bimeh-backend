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
    relationship = forms.ChoiceField(choices=RelationshipType.choices, label="رابطه با شما:")

    class Meta:
        model = Person
        exclude = ("is_household_head", "household")
