from rest_framework import serializers

from main.models import FamilyRelationship
from main.api.serializers.person import PersonSerializer


class FamilyRelationshipSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = FamilyRelationship
        fields = ("id", "person", "relationship_type")