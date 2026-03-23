from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom claims or format to the response
        return {
            'error': False,
            'message': 'Login successful',
            'data': {
                'access': data['access'],
                'refresh': data['refresh'],
                'user': {
                    'username': self.user.username,
                    'is_staff': self.user.is_staff,
                }
            }
        }

from config.throttles import LoginRateThrottle

class AdminLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]

class AdminLogoutView(APIView):
    """
    Optional: Blacklist refresh token if implementing logout on the backend.
    Most JWT client-side implementations just throw away the token.
    """
    def post(self, request):
        # We can implement token blacklisting here if needed
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
