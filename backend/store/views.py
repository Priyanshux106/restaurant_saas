from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StoreSettings
from .serializers import StoreStatusSerializer

class StoreStatusAPIView(APIView):
    """
    Public API to retrieve the current store status (open/closed, etc)
    """
    def get(self, request):
        store_settings = StoreSettings.objects.first()
        if not store_settings:
            # Fallback if somehow there's no settings record
            return Response({
                'is_open': False,
                'min_order_value': 200.00,
                'store_name': 'Restaurant',
                'estimated_delivery_time': 45
            })
            
        serializer = StoreStatusSerializer(store_settings)
        return Response(serializer.data)
