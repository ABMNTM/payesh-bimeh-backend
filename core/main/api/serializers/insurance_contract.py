from rest_framework import serializers

from main.models import InsuranceContract


class InsuranceContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceContract
        fields = "__all__"
