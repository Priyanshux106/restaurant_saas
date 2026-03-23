import uuid
from django.utils import timezone
from django.db import transaction
from rest_framework.exceptions import ValidationError, APIException

from .models import Order, OrderItem, Customer
from menu.models import MenuItem
from store.models import StoreSettings

class ServiceError(APIException):
    status_code = 400
    default_detail = 'Service error occurred.'

    def __init__(self, detail, code=None):
        super().__init__(detail, code)
        self.code = code

def generate_order_id():
    """Generates an order id like ORD-YYYYMMDD-ABCD"""
    date_str = timezone.now().strftime('%Y%m%d')
    unique_id = uuid.uuid4().hex[:4].upper()
    return f"ORD-{date_str}-{unique_id}"

@transaction.atomic
def create_order(data):
    """
    Core business logic to place an order.
    """
    # 1. Validate Store Status
    store_settings = StoreSettings.objects.first()
    if not store_settings or not store_settings.is_open:
        raise ServiceError("The store is currently closed. Please try again later.", code="STORE_CLOSED")

    # 2. Extract Data
    customer_phone = data['customer_phone']
    customer_name = data['customer_name']
    delivery_address = data['delivery_address']
    payment_method = data['payment_method']
    items_data = data['items']
    special_instructions = data.get('special_instructions', '')

    # 3. Calculate Totals & Validate Items
    subtotal = 0
    order_items_to_create = []

    for item_data in items_data:
        try:
            menu_item = MenuItem.objects.get(id=item_data['menu_item_id'])
        except MenuItem.DoesNotExist:
            raise ServiceError(f"Menu item {item_data['menu_item_id']} does not exist.", code="INVALID_ITEM")

        if not menu_item.is_available or not menu_item.is_active:
            raise ServiceError(f"Item '{menu_item.name}' is currently unavailable.", code="ITEM_UNAVAILABLE")

        size = item_data['size']
        quantity = item_data['quantity']

        # Determine unit price based on size
        unit_price = None
        if size == 'half':
            if menu_item.half_price is None:
                raise ServiceError(f"Item '{menu_item.name}' does not have a half size option.", code="INVALID_SIZE")
            unit_price = menu_item.half_price
        else:
            unit_price = menu_item.full_price

        total_price = unit_price * quantity
        subtotal += total_price

        order_items_to_create.append({
            'menu_item': menu_item,
            'item_name': menu_item.name,
            'size': size,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price
        })

    # 4. Check Minimum Order Value
    if store_settings and subtotal < store_settings.min_order_value:
        raise ServiceError(
            f"Minimum order value is ₹{store_settings.min_order_value}. Your current total is ₹{subtotal}.",
            code="MIN_ORDER_VALUE"
        )

    # 5. Get or Create Customer (update details if returning)
    customer, created = Customer.objects.update_or_create(
        phone=customer_phone,
        defaults={
            'name': customer_name,
            'address': delivery_address
        }
    )

    # 6. Create Order
    order_id = generate_order_id()
    # Check for extremely rare UUID collision
    while Order.objects.filter(order_id=order_id).exists():
        order_id = generate_order_id()

    order = Order.objects.create(
        order_id=order_id,
        customer=customer,
        delivery_address=delivery_address,
        payment_method=payment_method,
        subtotal=subtotal,
        total=subtotal,  # We can add taxes/delivery fees here later
        special_instructions=special_instructions
    )

    # 7. Create Order Items
    for item_dict in order_items_to_create:
        OrderItem.objects.create(
            order=order,
            **item_dict
        )

    # 8. Trigger WhatsApp Notification (Async / non-blocking placeholder)
    # We will implement this in Task B11. For now, try to import and call if it exists.
    try:
        from notifications.services import send_order_notification
        send_order_notification(order)
    except Exception as e:
        # We catch all exceptions here because we never want a failed 
        # WhatsApp message to rollback the successful order.
        import logging
        logger = logging.getLogger('notifications')
        logger.error(f"Failed to trigger notification for order {order.order_id}: {str(e)}")

    return order
