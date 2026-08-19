from rest_framework.viewsets import mixins
from rest_framework.permissions import IsAuthenticated
from common.utils.views import CustomGenericViewSet

from core.main.api.serializers.enrollment import (
    ListEnrollmentSerializer,
    RetrieveEnrollmentSerializer,
    CreateEnrollmentSerializer,
    CalculateTotalCostSerializer,
)
from main.models import Enrollment


class EnrollmentViewSet(
    CustomGenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    def get_queryset(self):
        if self.action == "list":
            return Enrollment.objects.select_related("contract").filter(
                guardian=self.request.user
            )
        if self.action == "retrieve":
            return (
                Enrollment.objects.select_related("contract")
                .prefetch_related("covered_members")
                .filter(guardian=self.request.user)
            )
        if self.action == "create":
            return Enrollment.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "create":
            context["user"] = self.request.user
        return context

    action_serializer_class = {
        "list": ListEnrollmentSerializer,
        "retrieve": RetrieveEnrollmentSerializer,
        "create": CreateEnrollmentSerializer,
        "calculate_total_cost": CalculateTotalCostSerializer,
    }

    permission_classes = (IsAuthenticated,)
