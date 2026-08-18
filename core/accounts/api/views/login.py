from rest_framework.permissions import AllowAny
from accounts.api.serializers.login import TokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainSerializer
