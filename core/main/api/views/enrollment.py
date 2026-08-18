from rest_framework.viewsets import mixins
from rest_framework.permissions import IsAuthenticated
from common.utils.views import CustomGenericViewSet

from core.main.api.serializers.enrollment import (
    ListEnrollmentSerializer,
    RetrieveEnrollmentSerializer,
)
from main.models import Enrollment


class EnrollmentViewSet(
    CustomGenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
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

    action_serializer_class = {
        "list": ListEnrollmentSerializer,
        "retrieve": RetrieveEnrollmentSerializer,
    }

    permission_classes = (IsAuthenticated,)
