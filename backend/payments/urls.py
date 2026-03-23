from django.urls import path
from .views import CreateRazorpayOrderAPIView, VerifyPaymentAPIView

urlpatterns = [
    path('payments/create/', CreateRazorpayOrderAPIView.as_view(), name='payment-create'),
    path('payments/verify/', VerifyPaymentAPIView.as_view(), name='payment-verify'),
]
