from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MenuAPIView
from .admin_views import AdminCategoryViewSet, AdminMenuItemViewSet

router = DefaultRouter()
router.register(r'admin/categories', AdminCategoryViewSet, basename='admin-category')
router.register(r'admin/items', AdminMenuItemViewSet, basename='admin-menuitem')

urlpatterns = [
    path('menu/', MenuAPIView.as_view(), name='public-menu'),
    path('', include(router.urls)), # Adds /api/admin/categories/ and /api/admin/items/ 
]
