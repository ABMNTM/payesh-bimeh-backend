from xml.sax.handler import _EntityResolverProtocol

from rest_framework import serializers

from core.main.api.serializers.person import CoveredMemberSerializer
from core.main.models.cost_rate_rule import CostRateRule
from core.main.models.current_insurance_contract import CurrentInsuranceContract
from main.models import Enrollment
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
    total_cost = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = Enrollment
        fields = (
            "id",
            "status",
            "terms_accepted",
            "terms_accepted_at",
            "covered_members",
        )
        extra_kwargs = {
            "status": {
                "read_only": True,
            },
            "terms_accepted_at": {
                "read_only": True,
            },
        }

    def get_total_cost(self, obj: Enrollment):
        total_cost = CurrentInsuranceContract.calculate_total_cost(obj)
        return total_cost
