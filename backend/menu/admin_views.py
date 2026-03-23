from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Category, MenuItem
from .admin_serializers import AdminCategorySerializer, AdminMenuItemSerializer

class AdminCategoryViewSet(viewsets.ModelViewSet):
    """
    Admin API for Category CRUD.
    """
    queryset = Category.objects.all().order_by('display_order', 'name')
    serializer_class = AdminCategorySerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        # Implement soft delete for Category
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        
        # Soft delete related items too
        instance.items.update(is_active=False)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminMenuItemViewSet(viewsets.ModelViewSet):
    """
    Admin API for MenuItem CRUD.
    """
    queryset = MenuItem.objects.all().order_by('category__display_order', 'display_order', 'name')
    serializer_class = AdminMenuItemSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        # Implement soft delete for MenuItem
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'])
    def toggle_availability(self, request, pk=None):
        """
        Quick toggle for item availability (in/out of stock).
        """
        item = self.get_object()
        item.is_available = not item.is_available
        item.save()
        return Response({'status': 'success', 'is_available': item.is_available})
