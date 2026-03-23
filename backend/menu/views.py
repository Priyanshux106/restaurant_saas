from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
from store.models import StoreSettings

class MenuAPIView(APIView):
    """
    Public API to retrieve the full menu.
    Includes categories, available items, and store status.
    """
    def get(self, request):
        # 1. Get store settings
        store_settings = StoreSettings.objects.first()
        is_open = store_settings.is_open if store_settings else False
        min_order = store_settings.min_order_value if store_settings else 0

        # 2. Get active categories
        categories = Category.objects.filter(is_active=True).order_by('display_order', 'name')
        
        # 3. Serialize data
        serializer = CategorySerializer(categories, many=True)
        
        return Response({
            'store_open': is_open,
            'min_order_value': min_order,
            'categories': serializer.data
        })
