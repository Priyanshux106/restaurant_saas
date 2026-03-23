import os
import logging
from twilio.rest import Client
from store.models import StoreSettings

logger = logging.getLogger('notifications')

def send_order_notification(order):
    """
    Sends a WhatsApp notification to the restaurant owner when a new order is placed.
    Fails silently (just logs) so order placement is not interrupted.
    """
    try:
        store_settings = StoreSettings.objects.first()
        if not store_settings or not store_settings.owner_whatsapp:
            logger.warning("Notification skipped: Owner WhatsApp number not configured.")
            return

        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        from_whatsapp = os.environ.get('TWILIO_WHATSAPP_FROM')
        to_whatsapp = f"whatsapp:+91{store_settings.owner_whatsapp}"

        if not all([account_sid, auth_token, from_whatsapp]):
            logger.warning("Notification skipped: Twilio credentials not fully configured.")
            return

        client = Client(account_sid, auth_token)

        # Build message
        items_str = "\n".join([f"- {item.quantity}x {item.item_name} ({item.size})" for item in order.items.all()])
        
        message_body = (
            f"🚨 *NEW ORDER RECEIVED!*\n\n"
            f"*Order ID:* {order.order_id}\n"
            f"*Customer:* {order.customer.name}\n"
            f"*Phone:* {order.customer.phone}\n"
            f"*Total:* ₹{order.total}\n"
            f"*Payment:* {order.get_payment_method_display()}\n\n"
            f"*Items:*\n"
            f"{items_str}\n\n"
            f"*Address:* {order.delivery_address}"
        )

        if order.special_instructions:
            message_body += f"\n\n*Instructions:* {order.special_instructions}"

        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        
        logger.info(f"WhatsApp notification sent for order {order.order_id}. SID: {message.sid}")

    except Exception as e:
        logger.error(f"Failed to send WhatsApp notification for order {order.order_id}: {str(e)}")
