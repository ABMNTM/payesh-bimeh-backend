from rest_framework import serializers

from main.models import Person
from main.types import RelationshipType


class CoveredMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "first_name", "last_name")


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = ("is_household_head", "household")


class CreateUpdatePersonSerializer(serializers.ModelSerializer):
    family_relationship = serializers.ChoiceField(RelationshipType.choices)

    class Meta:
        model = Person
        exclude = ("is_household_head", "household")
