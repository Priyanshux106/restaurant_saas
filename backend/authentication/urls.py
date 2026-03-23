from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AdminLoginView, AdminLogoutView

urlpatterns = [
    path('auth/login/', AdminLoginView.as_view(), name='admin-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='admin-token-refresh'),
    path('auth/logout/', AdminLogoutView.as_view(), name='admin-logout'),
]
