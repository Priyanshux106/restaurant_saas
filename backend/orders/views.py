from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Customer
from .serializers import PlaceOrderSerializer, OrderSerializer, CustomerSerializer
from .services import create_order, ServiceError
import logging

logger = logging.getLogger('orders')

from config.throttles import OrderRateThrottle

class PlaceOrderAPIView(APIView):
    """
    Public API to place a new order.
    """
    throttle_classes = [OrderRateThrottle]

    def post(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": True, "message": "Validation failed", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 1. Core Logic to process the order
            order = create_order(serializer.validated_data)
            
            # 2. Serialize complete order for response
            order_data = OrderSerializer(order).data
            
            logger.info(f"Order {order.order_id} placed successfully using {order.payment_method}.")

            return Response({
                "error": False,
                "message": "Order placed successfully! You will receive a confirmation call shortly.",
                "data": order_data
            }, status=status.HTTP_201_CREATED)

        except ServiceError as e:
            logger.warning(f"Order placement failed: {str(e)}")
            return Response({
                "error": True,
                "code": e.code,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error creating order: {str(e)}")
            return Response({
                "error": True,
                "message": "An unexpected error occurred while placing your order. Please try again or call us."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderDetailAPIView(APIView):
    """
    Public API to retrieve order details by order_id.
    """
    def get(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": True, "message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class CustomerLookupAPIView(APIView):
    """
    Public API to lookup customer details by phone number (for auto-filling checkout form).
    """
    def get(self, request, phone):
        try:
            customer = Customer.objects.get(phone=phone)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({"error": True, "message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum, Count

class AdminOrderPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class AdminOrderAPIView(APIView):
    """
    Admin API to list orders with filters. 
    Requires JWT Authentication.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        status_filter = request.query_params.get('status')
        date_filter = request.query_params.get('date') # YYYY-MM-DD
        search_query = request.query_params.get('search')
        
        orders = Order.objects.all().order_by('-created_at')
        
        if status_filter:
            orders = orders.filter(status=status_filter)
        if date_filter:
            orders = orders.filter(created_at__date=date_filter)
        if search_query:
            orders = orders.filter(
                models.Q(order_id__icontains=search_query) |
                models.Q(customer__phone__icontains=search_query) |
                models.Q(customer__name__icontains=search_query)
            )
            
        paginator = AdminOrderPagination()
        paginated_orders = paginator.paginate_queryset(orders, request)
        serializer = OrderSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)

class AdminOrderDetailAPIView(APIView):
    """
    Admin API to retrieve full order detail.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": True, "message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class AdminOrderStatusUpdateAPIView(APIView):
    """
    Admin API to update order status.
    """
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
            new_status = request.data.get('status')
            
            # Simple validation on status choice
            valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
            if new_status not in valid_statuses:
                return Response(
                    {"error": True, "message": f"Invalid status. Must be one of {valid_statuses}."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            order.status = new_status
            order.save()
            
            # Optionally: Trigger WhatsApp notification here for status updates (e.g. "Your order is ready")
            
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": True, "message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

from django.utils import timezone
from datetime import timedelta

class AdminRevenueAPIView(APIView):
    """
    Admin API to get revenue statistics (Today, This Week, This Month, Total).
    Requires JWT Authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=now.weekday())
        month_start = today_start.replace(day=1)

        # Base queryset for valid orders (e.g. not cancelled)
        valid_orders = Order.objects.exclude(status='cancelled')

        def aggregate_revenue(queryset):
            from django.db.models import Sum, Count
            result = queryset.aggregate(total=Sum('total'), count=Count('id'))
            return {
                'revenue': result['total'] or 0.00,
                'orders_count': result['count']
            }

        return Response({
            'today': aggregate_revenue(valid_orders.filter(created_at__gte=today_start)),
            'this_week': aggregate_revenue(valid_orders.filter(created_at__gte=week_start)),
            'this_month': aggregate_revenue(valid_orders.filter(created_at__gte=month_start)),
            'all_time': aggregate_revenue(valid_orders)
        })
