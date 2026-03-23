from django.urls import path
from .views import StoreStatusAPIView
from .admin_views import AdminStoreSettingsAPIView

urlpatterns = [
    # Public
    path('status/', StoreStatusAPIView.as_view(), name='public-store-status'),

    # Admin (Requires JWT Auth)
    path('admin/settings/', AdminStoreSettingsAPIView.as_view(), name='admin-store-settings'),
]
