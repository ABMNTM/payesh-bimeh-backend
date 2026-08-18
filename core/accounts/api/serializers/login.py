from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        tokens = super().validate(attrs)
        tokens.pop("refresh")
        return tokens
