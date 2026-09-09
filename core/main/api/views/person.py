from django.db.models import Q
from rest_framework.viewsets import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from common.utils.views import CustomGenericViewSet

from main.api.serializers.person import CreateUpdatePersonSerializer, PersonSerializer

from main.models import Person


class PersonViewSet(
    CustomGenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    http_method_names = ("post", "patch")

    def get_queryset(self):
        person_id = self.request.user.person_id
        if self.action == "list":
            return Person.objects.filter(household_id=person_id)
        if self.action == "partial_update":
            return Person.objects.filter(Q(id=person_id) | Q(household_id=person_id))
        if self.action == "create" | "mine":
            return Person.objects.all()

    permission_classes = (IsAuthenticated,)

    action_serializer_class = {
        "list": PersonSerializer,
        "create": CreateUpdatePersonSerializer,
        "mine": CreateUpdatePersonSerializer,
        "partial_update": CreateUpdatePersonSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(household_id=self.request.user.person_id)

    @action(methods=["post"], detail=False)
    def mine(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(is_household_head=True)
        request.user.person = serializer.instance
        request.user.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
