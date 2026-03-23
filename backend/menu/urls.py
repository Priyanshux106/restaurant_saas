from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import MenuAPIView
from .admin_views import AdminCategoryViewSet, AdminMenuItemViewSet

router = SimpleRouter()
router.register(r'admin/categories', AdminCategoryViewSet, basename='admin-category')
router.register(r'admin/items', AdminMenuItemViewSet, basename='admin-menuitem')

urlpatterns = [
    path('', MenuAPIView.as_view(), name='public-menu'),
    path('', include(router.urls)), # Adds /api/admin/categories/ and /api/admin/items/ 
]
