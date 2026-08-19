from django.db.models import Q
from rest_framework.viewsets import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from common.utils.views import CustomGenericViewSet

from main.api.serializers.family_relationship import FamilyRelationshipSerializer

from main.models import FamilyRelationship


class PersonViewSet(
    CustomGenericViewSet,
    mixins.ListModelMixin,
):
    http_method_names = ("get",)

    def get_queryset(self):
        if self.action == "list":
            person_id = self.request.user.person_id
            return FamilyRelationship.objects.select_related("person").filter(
                Q(related_person_id=person_id) | Q(person__household_id=person_id)
            )

    permission_classes = (IsAuthenticated,)

    action_serializer_class = {
        "list": FamilyRelationshipSerializer,
    }
