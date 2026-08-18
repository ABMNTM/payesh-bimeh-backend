from rest_framework import serializers

from main.models import Person


class CoveredMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "first_name", "last_name")
