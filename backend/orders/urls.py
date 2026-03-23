from django.urls import path
from .views import (
    PlaceOrderAPIView, OrderDetailAPIView, CustomerLookupAPIView,
    AdminOrderAPIView, AdminOrderDetailAPIView, AdminOrderStatusUpdateAPIView,
    AdminRevenueAPIView
)

urlpatterns = [
    # Public Endpoints
    path('orders/', PlaceOrderAPIView.as_view(), name='public-place-order'),
    path('orders/<str:order_id>/', OrderDetailAPIView.as_view(), name='public-order-detail'),
    path('customers/<str:phone>/', CustomerLookupAPIView.as_view(), name='public-customer-lookup'),

    # Admin Endpoints (Require JWT Auth)
    path('admin/orders/', AdminOrderAPIView.as_view(), name='admin-order-list'),
    path('admin/orders/<str:order_id>/', AdminOrderDetailAPIView.as_view(), name='admin-order-detail'),
    path('admin/orders/<str:order_id>/status/', AdminOrderStatusUpdateAPIView.as_view(), name='admin-order-status'),
    path('admin/revenue/', AdminRevenueAPIView.as_view(), name='admin-revenue'),
]
