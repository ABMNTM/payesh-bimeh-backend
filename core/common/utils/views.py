from rest_framework.viewsets import GenericViewSet


class CustomGenericViewSet(GenericViewSet):
    action_serializer_class = dict()
    action_permission_classes = dict()

    def get_serializer_class(self):
        return self.action_serializer_class.get(self.action, self.serializer_class)

    def get_permissions(self):
        permission_classes = self.action_permission_classes.get(
            self.action, self.permission_classes
        )
        return [permission() for permission in permission_classes]
