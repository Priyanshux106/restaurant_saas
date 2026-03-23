from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import logging

from orders.models import Order
from .services import create_payment_order, verify_payment_signature

logger = logging.getLogger('payments')

class CreateRazorpayOrderAPIView(APIView):
    """
    Called by frontend right before opening Razorpay checkout window.
    """
    def post(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({"error": "order_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            order = Order.objects.get(order_id=order_id)
            if order.payment_method != 'online':
                return Response({"error": "Order is not marked for online payment"}, status=status.HTTP_400_BAD_REQUEST)
                
            payment_data = create_payment_order(order)
            
            return Response({
                "razorpay_order_id": payment_data['id'],
                "amount": payment_data['amount'],
                "currency": payment_data['currency'],
                "key_id": os.environ.get('RAZORPAY_KEY_ID')
            })
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyPaymentAPIView(APIView):
    """
    Called by frontend after Razorpay checkout yields a successful signature.
    """
    def post(self, request):
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return Response({"error": "Missing payment signature details"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # 1. Verify signature
            is_valid = verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature)
            
            if not is_valid:
                return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)
                
            # 2. Update Order status
            order = Order.objects.get(payment_id=razorpay_order_id)
            order.payment_status = 'paid'
            order.save(update_fields=['payment_status'])
            
            logger.info(f"Payment verified successfully for order {order.order_id}")
            return Response({"status": "Payment verified successfully"})
            
        except Order.DoesNotExist:
            return Response({"error": "Order associated with payment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
