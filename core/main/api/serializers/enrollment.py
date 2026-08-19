from rest_framework import serializers

from main.models import Enrollment
from main.api.serializers.person import CoveredMemberSerializer
from main.api.serializers.insurance_contract import InsuranceContractSerializer


class ListEnrollmentSerializer(serializers.ModelSerializer):
    contract = InsuranceContractSerializer()

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "status",
            "contract",
            "terms_accepted",
            "terms_accepted_at",
        )


class RetrieveEnrollmentSerializer(serializers.ModelSerializer):
    contract = InsuranceContractSerializer()
    covered_members = CoveredMemberSerializer(many=True)

    class Meta:
        model = Enrollment
        fields = "__all__"


class CreateEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        models = Enrollment
        fields = (
            "id",
            "covered_members",
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.covered_members.add(self.context.get("user").person)
        return instance


class CalculateTotalCostSerializer(serializers.Serializer):
    total_cost = serializers.IntegerField()
