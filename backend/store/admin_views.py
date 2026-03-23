from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import StoreSettings
from .admin_serializers import AdminStoreSettingsSerializer

class AdminStoreSettingsAPIView(APIView):
    """
    Admin API to Read/Update the singleton StoreSettings.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self):
        settings, _ = StoreSettings.objects.get_or_create(id=1)
        return settings

    def get(self, request):
        serializer = AdminStoreSettingsSerializer(self.get_object())
        return Response(serializer.data)

    def put(self, request):
        settings = self.get_object()
        serializer = AdminStoreSettingsSerializer(settings, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return Response(
            {"error": True, "message": "Validation failed", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
