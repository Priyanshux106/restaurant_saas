from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class LoginRateThrottle(AnonRateThrottle):
    """
    Limits the rate of login attempts per IP.
    """
    scope = 'login'

class OrderRateThrottle(AnonRateThrottle):
    """
    Limits the rate of order placement attempts per IP for anonymous users.
    """
    scope = 'order'
