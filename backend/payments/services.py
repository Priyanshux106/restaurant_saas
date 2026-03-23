import razorpay
import os
import logging
from orders.models import Order

logger = logging.getLogger('payments')

def get_razorpay_client():
    key_id = os.environ.get('RAZORPAY_KEY_ID')
    key_secret = os.environ.get('RAZORPAY_KEY_SECRET')
    
    if not key_id or not key_secret:
        return None
        
    return razorpay.Client(auth=(key_id, key_secret))

def create_payment_order(order):
    """
    Creates a Razorpay order for an existing system Order.
    Razorpay expects amounts in minimum currency denomination (paise).
    """
    client = get_razorpay_client()
    if not client:
        raise ValueError("Razorpay credentials not configured")
        
    amount_in_paise = int(order.total * 100)
    
    data = {
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": order.order_id,
        "notes": {
            "customer_phone": order.customer.phone
        }
    }
    
    try:
        payment_data = client.order.create(data=data)
        # Store the razorpay order id in our order record
        order.payment_id = payment_data['id']
        order.save(update_fields=['payment_id'])
        return payment_data
    except Exception as e:
        logger.error(f"Failed to create Razorpay order for {order.order_id}: {str(e)}")
        raise

def verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """
    Verifies the payment signature sent by frontend after successful payment.
    """
    client = get_razorpay_client()
    if not client:
        raise ValueError("Razorpay credentials not configured")
        
    try:
        # verify_payment_signature returns None on success, raises Exception on failure
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
        return True
    except razorpay.errors.SignatureVerificationError:
        logger.warning(f"Signature verification failed for order {razorpay_order_id}")
        return False
    except Exception as e:
        logger.error(f"Error verifying payment signature: {str(e)}")
        return False
