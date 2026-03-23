# Technical Requirements Document (TRD)
## Restaurant Ordering System

**Version:** 1.0  
**Date:** 2026-03-23  
**Author:** Engineering Team  
**Status:** Draft

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTS                                   │
│  ┌──────────────────┐        ┌──────────────────────────────┐   │
│  │  Customer Mobile  │        │  Admin Dashboard (Browser)   │   │
│  │  (Next.js PWA)    │        │  (Next.js — Protected)       │   │
│  └────────┬─────────┘        └──────────────┬───────────────┘   │
└───────────┼──────────────────────────────────┼──────────────────┘
            │ HTTPS                            │ HTTPS
            ▼                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (Vercel)                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Next.js Application                                      │   │
│  │  • SSR/SSG for Menu (SEO + Performance)                   │   │
│  │  • Client-side Cart (localStorage)                        │   │
│  │  • API Routes (BFF pattern for sensitive operations)      │   │
│  └──────────────────────────────┬───────────────────────────┘   │
└─────────────────────────────────┼───────────────────────────────┘
                                  │ HTTPS (REST API)
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (Render)                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Django + Django REST Framework                           │   │
│  │  • REST API Endpoints                                     │   │
│  │  • Business Logic & Validation                            │   │
│  │  • Admin Authentication (JWT)                             │   │
│  │  • Order Processing Pipeline                              │   │
│  │  • Notification Service                                   │   │
│  └──────┬──────────────┬───────────────┬────────────────────┘   │
│         │              │               │                         │
│         ▼              ▼               ▼                         │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐             │
│  │ Database │  │  WhatsApp    │  │  Payment      │             │
│  │ SQLite → │  │  API         │  │  Gateway      │             │
│  │ Postgres │  │  (Twilio)    │  │  (Razorpay)   │             │
│  └──────────┘  └──────────────┘  └───────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Breakdown

| Component | Technology | Purpose | Hosting |
|-----------|-----------|---------|---------|
| Customer Frontend | Next.js 14 (App Router) | Menu browsing, cart, checkout | Vercel |
| Admin Dashboard | Next.js 14 (same app, `/admin` route) | Order management, menu CRUD | Vercel |
| Backend API | Django 5.0 + DRF 3.15 | REST API, business logic | Render |
| Database | SQLite (dev) → PostgreSQL (prod) | Data persistence | Render Postgres |
| WhatsApp API | Twilio WhatsApp Business API | Order notifications to owner | Twilio Cloud |
| Payment Gateway | Razorpay | Online payment processing | Razorpay Cloud |
| File Storage | Cloudinary (free tier) | Menu item images | Cloudinary |

### 1.3 Why These Choices?

| Choice | Why |
|--------|-----|
| **Next.js** | SSR for fast menu loading (SEO+perf), React ecosystem, easy Vercel deploy, API routes for BFF |
| **Django + DRF** | Rapid development, built-in admin, excellent ORM, mature ecosystem, Python is easy to maintain |
| **SQLite → PostgreSQL** | Zero setup for development, seamless Django migration to PostgreSQL for production |
| **Vercel** | Free tier, edge CDN, auto-deploy from Git, perfect for Next.js |
| **Render** | Free tier for Django, managed PostgreSQL, simple deploy from Git |
| **Twilio WhatsApp** | Reliable, well-documented API, supports India, pay-per-message pricing |
| **Razorpay** | Built for India, supports UPI/cards/wallets, easy integration, good docs |

---

## 2. Frontend Architecture

### 2.1 Pages and Routing

```
/                       → Home + Menu page (tabbed: Starters/Mains/Drinks/Desserts)
/cart                   → Cart page (items, quantities, total)
/checkout               → Checkout form (name, phone, address, payment)
/order/[orderId]        → Order confirmation page
/admin                  → Admin login page
/admin/dashboard        → Live orders + sound alerts
/admin/orders           → Order history with filters
/admin/menu             → Menu management (CRUD)
/admin/revenue          → Revenue summary
/admin/settings         → Store open/close toggle, min order value
```

### 2.2 State Management

| State | Strategy | Reason |
|-------|----------|--------|
| Cart items | `localStorage` + React Context | Persists across sessions, no backend needed |
| Menu data | SWR (stale-while-revalidate) | Cached on client, revalidates from API |
| Admin auth | JWT in httpOnly cookie | Secure, persists across tabs |
| Live orders | Polling (5s interval) + Audio API | Simple, reliable, no WebSocket complexity |
| Store status | SWR with 30s revalidation | Customers see near-real-time open/close |

### 2.3 API Integration

```
Frontend (Next.js)
├── /lib/api.js              → Axios instance with base URL + interceptors
├── /hooks/useMenu.js        → SWR hook for menu data
├── /hooks/useCart.js         → Cart context + localStorage sync
├── /hooks/useOrders.js      → SWR hook for admin orders (polling)
├── /hooks/useRevenue.js     → SWR hook for revenue data
└── /lib/razorpay.js         → Razorpay checkout integration
```

### 2.4 Key Frontend Libraries

| Library | Purpose |
|---------|---------|
| `next` 14.x | Framework |
| `swr` | Data fetching + caching |
| `axios` | HTTP client |
| `react-hot-toast` | Toast notifications |
| `lucide-react` | Icons |
| `razorpay` | Payment gateway JS SDK |

---

## 3. Backend Architecture

### 3.1 Django App Structure

```
restaurant_backend/
├── manage.py
├── config/                  → Project settings
│   ├── settings/
│   │   ├── base.py          → Common settings
│   │   ├── development.py   → SQLite, DEBUG=True
│   │   └── production.py    → PostgreSQL, DEBUG=False
│   ├── urls.py              → Root URL config
│   └── wsgi.py
├── menu/                    → Menu app
│   ├── models.py            → Category, MenuItem
│   ├── serializers.py       → Menu serializers
│   ├── views.py             → Menu API views
│   └── urls.py
├── orders/                  → Orders app
│   ├── models.py            → Order, OrderItem, Customer
│   ├── serializers.py       → Order serializers
│   ├── views.py             → Order API views
│   ├── services.py          → Order processing logic
│   └── urls.py
├── notifications/           → Notification app
│   ├── services.py          → WhatsApp integration (Twilio)
│   └── tasks.py             → Async notification sending
├── payments/                → Payment app
│   ├── services.py          → Razorpay integration
│   ├── views.py             → Payment verification webhook
│   └── urls.py
├── store/                   → Store settings app
│   ├── models.py            → StoreSettings (open/close, min order)
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── authentication/          → Admin auth app
    ├── views.py             → Login, logout, token refresh
    └── urls.py
```

### 3.2 Models Overview

#### menu/models.py
```python
class Category(models.Model):
    name = models.CharField(max_length=50)       # Starters, Mains, Drinks, Desserts
    display_order = models.IntegerField()
    is_active = models.BooleanField(default=True)

class MenuItem(models.Model):
    category = models.ForeignKey(Category, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)           # Cloudinary URL
    half_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    full_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)  # Soft delete
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### orders/models.py
```python
class Customer(models.Model):
    phone = models.CharField(max_length=15, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    ]
    order_id = models.CharField(max_length=20, unique=True, db_index=True)
    customer = models.ForeignKey(Customer, related_name='orders')
    delivery_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    payment_status = models.CharField(max_length=20, default='pending')
    payment_id = models.CharField(max_length=100, blank=True)  # Razorpay payment ID
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    SIZE_CHOICES = [('half', 'Half'), ('full', 'Full')]
    order = models.ForeignKey(Order, related_name='items')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.PROTECT)
    item_name = models.CharField(max_length=100)       # Snapshot at order time
    size = models.CharField(max_length=4, choices=SIZE_CHOICES)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)  # Snapshot
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
```

#### store/models.py
```python
class StoreSettings(models.Model):
    is_open = models.BooleanField(default=True)
    min_order_value = models.DecimalField(max_digits=8, decimal_places=2, default=200)
    store_name = models.CharField(max_length=200, default='Restaurant')
    store_phone = models.CharField(max_length=15)
    owner_whatsapp = models.CharField(max_length=15)   # For notifications
    estimated_delivery_time = models.IntegerField(default=45)  # minutes
    updated_at = models.DateTimeField(auto_now=True)
```

### 3.3 Services Layer

| Service | Responsibility |
|---------|---------------|
| `orders/services.py` | Order creation, validation, ID generation, status transitions |
| `notifications/services.py` | Send WhatsApp via Twilio, format order message |
| `payments/services.py` | Create Razorpay order, verify payment signature |

---

## 4. Database Design

### 4.1 Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────────┐
│   Category   │       │   StoreSettings  │
│──────────────│       │──────────────────│
│ id (PK)      │       │ id (PK)          │
│ name         │       │ is_open          │
│ display_order│       │ min_order_value  │
│ is_active    │       │ store_name       │
└──────┬───────┘       │ owner_whatsapp   │
       │ 1:N           └──────────────────┘
       ▼
┌──────────────┐
│   MenuItem   │
│──────────────│
│ id (PK)      │
│ category (FK)│──────→ Category
│ name         │
│ half_price   │
│ full_price   │
│ is_available │
│ image        │
└──────┬───────┘
       │
       │ Referenced by
       ▼
┌──────────────┐       ┌──────────────────┐
│  OrderItem   │       │    Customer      │
│──────────────│       │──────────────────│
│ id (PK)      │       │ id (PK)          │
│ order (FK)   │──→    │ phone (unique)   │
│ menu_item(FK)│──→ MI │ name             │
│ item_name    │       │ address          │
│ size         │       └────────┬─────────┘
│ quantity     │                │ 1:N
│ unit_price   │                ▼
│ total_price  │       ┌──────────────────┐
└──────────────┘       │     Order        │
       ▲               │──────────────────│
       │ 1:N           │ id (PK)          │
       └───────────────│ order_id (unique)│
                       │ customer (FK)    │──→ Customer
                       │ status           │
                       │ payment_method   │
                       │ total            │
                       │ created_at       │
                       └──────────────────┘
```

### 4.2 Indexing Strategy

| Table | Index | Reason |
|-------|-------|--------|
| `Customer` | `phone` (unique) | Fast lookup for returning customers |
| `Order` | `order_id` (unique) | Fast lookup by order ID |
| `Order` | `status` | Filter orders by status in admin dashboard |
| `Order` | `created_at` | Sort orders chronologically, revenue queries |
| `Order` | `customer_id` | Order history by customer |
| `MenuItem` | `category_id` | Filter items by category |
| `MenuItem` | `is_available, is_active` | Quick filtering for available items |

### 4.3 Data Migration Path

**Development:** SQLite (zero config, file-based)  
**Production:** PostgreSQL on Render (managed, free tier available)  

Django ORM handles the switch seamlessly — just change `DATABASES` setting in `production.py`.

---

## 5. API Design

### 5.1 Endpoint List

#### Public Endpoints (No Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/menu/` | Get all menu categories with items |
| `GET` | `/api/store/status/` | Get store open/close status + settings |
| `POST` | `/api/orders/` | Place a new order |
| `GET` | `/api/orders/{order_id}/` | Get order details by order ID |
| `GET` | `/api/customers/{phone}/` | Get customer info for auto-fill |
| `POST` | `/api/payments/create/` | Create Razorpay payment order |
| `POST` | `/api/payments/verify/` | Verify Razorpay payment |

#### Admin Endpoints (JWT Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/login/` | Admin login (returns JWT) |
| `POST` | `/api/auth/refresh/` | Refresh JWT token |
| `GET` | `/api/admin/orders/` | Get all orders (filterable) |
| `GET` | `/api/admin/orders/{id}/` | Get single order detail |
| `PATCH` | `/api/admin/orders/{id}/status/` | Update order status |
| `GET` | `/api/admin/revenue/` | Revenue summary |
| `GET` | `/api/admin/menu/` | Get all menu items (including inactive) |
| `POST` | `/api/admin/menu/` | Create menu item |
| `PUT` | `/api/admin/menu/{id}/` | Update menu item |
| `DELETE` | `/api/admin/menu/{id}/` | Soft-delete menu item |
| `PATCH` | `/api/admin/menu/{id}/availability/` | Toggle item availability |
| `GET` | `/api/admin/store/settings/` | Get store settings |
| `PUT` | `/api/admin/store/settings/` | Update store settings |

### 5.2 Request/Response Formats

#### GET /api/menu/ — Response
```json
{
  "store_open": true,
  "min_order_value": 200,
  "categories": [
    {
      "id": 1,
      "name": "Starters",
      "items": [
        {
          "id": 1,
          "name": "Paneer Tikka",
          "description": "Marinated cottage cheese grilled to perfection",
          "image": "https://res.cloudinary.com/.../paneer-tikka.jpg",
          "half_price": 150.00,
          "full_price": 250.00,
          "is_available": true
        }
      ]
    }
  ]
}
```

#### POST /api/orders/ — Request
```json
{
  "customer_name": "Rahul Kumar",
  "customer_phone": "9876543210",
  "delivery_address": "42, MG Road, Near Park Hospital",
  "payment_method": "cod",
  "items": [
    {
      "menu_item_id": 1,
      "size": "full",
      "quantity": 2
    },
    {
      "menu_item_id": 5,
      "size": "half",
      "quantity": 1
    }
  ]
}
```

#### POST /api/orders/ — Response
```json
{
  "order_id": "ORD-20260323-0042",
  "status": "pending",
  "items": [
    {
      "name": "Paneer Tikka",
      "size": "full",
      "quantity": 2,
      "unit_price": 250.00,
      "total_price": 500.00
    }
  ],
  "subtotal": 650.00,
  "total": 650.00,
  "payment_method": "cod",
  "estimated_delivery_time": 45,
  "message": "Order placed successfully! You will receive a confirmation call shortly."
}
```

#### PATCH /api/admin/orders/{id}/status/ — Request
```json
{
  "status": "preparing"
}
```

#### GET /api/admin/revenue/?period=daily — Response
```json
{
  "period": "daily",
  "date": "2026-03-23",
  "total_orders": 42,
  "total_revenue": 18750.00,
  "completed_orders": 38,
  "cancelled_orders": 2,
  "pending_orders": 2,
  "average_order_value": 446.43,
  "payment_breakdown": {
    "cod": 12500.00,
    "online": 6250.00
  }
}
```

### 5.3 Authentication Strategy

| User | Method | Details |
|------|--------|---------|
| Customer | None | No authentication for MVP — identified by phone number |
| Admin | JWT (JSON Web Token) | Simple username/password login → JWT issued → stored in httpOnly cookie |

**JWT Flow:**
1. Admin enters password on `/admin` login page
2. Backend validates → returns `access_token` (15min) + `refresh_token` (7days)
3. Frontend stores tokens in httpOnly secure cookies
4. Every admin API request includes `Authorization: Bearer <access_token>`
5. On expiry → auto-refresh using refresh token

---

## 6. Notification System

### 6.1 Notification Flow

```
Order Placed
    │
    ├──→ Save to Database
    │
    ├──→ Send WhatsApp (async)
    │       │
    │       ├── Success → Log "whatsapp_sent"
    │       └── Failure → Log "whatsapp_failed" (dashboard is fallback)
    │
    └──→ Dashboard Polling detects new order
            │
            └── Play sound alert 🔔
```

### 6.2 WhatsApp Integration (Twilio)

**Setup:**
1. Create Twilio account
2. Enable WhatsApp Sandbox (dev) or WhatsApp Business API (prod)
3. Get Account SID, Auth Token, and WhatsApp-enabled phone number

**Message Template:**
```
🍽️ NEW ORDER — #{order_id}

📱 Customer: {name} ({phone})
📍 Address: {address}
💰 Total: ₹{total} ({payment_method})

🛒 Items:
{item_list}

⏰ Placed at: {time}
```

**Implementation:**
```python
# notifications/services.py
from twilio.rest import Client

def send_order_whatsapp(order):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message_body = format_order_message(order)

    try:
        message = client.messages.create(
            body=message_body,
            from_='whatsapp:+14155238886',  # Twilio sandbox
            to=f'whatsapp:+91{OWNER_WHATSAPP}'
        )
        return {"success": True, "sid": message.sid}
    except Exception as e:
        logger.error(f"WhatsApp failed for order {order.order_id}: {e}")
        return {"success": False, "error": str(e)}
```

### 6.3 Dashboard Sound Alert

```javascript
// Frontend: useOrders hook
const playNotificationSound = () => {
  const audio = new Audio('/sounds/new-order.mp3');
  audio.play().catch(e => console.log('Audio play failed:', e));
};

// Poll every 5 seconds
const { data: orders } = useSWR('/api/admin/orders/?status=pending', fetcher, {
  refreshInterval: 5000,
  onSuccess: (newData, key, config) => {
    if (newData.count > previousCount) {
      playNotificationSound();
    }
  }
});
```

---

## 7. Security

### 7.1 Input Validation

| Field | Validation |
|-------|-----------|
| Phone number | Regex: `^[6-9]\d{9}$` (Indian mobile) |
| Customer name | 2-100 chars, alphanumeric + spaces |
| Address | 10-500 chars, required |
| Order items | At least 1 item, valid menu_item_id, valid size |
| Quantity | 1-20 per item |
| Payment method | Must be 'cod' or 'online' |

### 7.2 Rate Limiting

| Endpoint | Limit | Reason |
|----------|-------|--------|
| `POST /api/orders/` | 5 per phone per hour | Prevent spam orders |
| `POST /api/auth/login/` | 5 attempts per IP per 15min | Prevent brute force |
| All public endpoints | 100 requests per IP per minute | General protection |

**Implementation:** `django-ratelimit` or DRF throttling classes.

### 7.3 Data Protection

- Admin passwords hashed with Django's PBKDF2
- JWT tokens in httpOnly, secure, SameSite cookies
- CORS restricted to frontend domain only
- HTTPS enforced in production (Vercel + Render provide this)
- No sensitive data logged (phone numbers partially masked in logs)
- Database backups: Render automated daily backups

---

## 8. Deployment Architecture

### 8.1 Frontend (Vercel)

```
GitHub Push → Vercel Auto-Build → CDN Distribution
```

**Configuration:**
- Framework: Next.js
- Build command: `npm run build`
- Output: `.next`
- Environment variables set in Vercel dashboard

### 8.2 Backend (Render)

```
GitHub Push → Render Auto-Build → Gunicorn WSGI Server
```

**Configuration:**
- Runtime: Python 3.12
- Build command: `pip install -r requirements.txt && python manage.py migrate`
- Start command: `gunicorn config.wsgi:application`
- Free tier: spins down after inactivity (upgrade to Starter for always-on)

### 8.3 Database (Render PostgreSQL)

- Managed PostgreSQL instance
- Auto backups
- Connection string provided as environment variable

### 8.4 Environment Variables

#### Frontend (Vercel)
```
NEXT_PUBLIC_API_URL=https://restaurant-api.onrender.com
NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_live_xxxxx
```

#### Backend (Render)
```
SECRET_KEY=django-secure-random-key
DEBUG=False
ALLOWED_HOSTS=restaurant-api.onrender.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
CORS_ALLOWED_ORIGINS=https://restaurant-site.vercel.app
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
OWNER_WHATSAPP_NUMBER=+919876543210
RAZORPAY_KEY_ID=rzp_live_xxxxx
RAZORPAY_KEY_SECRET=xxxxx
ADMIN_PASSWORD=secure-admin-password
```

---

## 9. Scalability Plan

### 9.1 Current Scale (MVP)

- Expected: 50-200 orders/day
- SQLite is fine for dev, PostgreSQL for production
- Vercel + Render free tiers handle this workload

### 9.2 Database Scaling

| Stage | Orders/Day | Strategy |
|-------|-----------|----------|
| MVP | < 200 | Single PostgreSQL (Render free) |
| Growth | 200-1000 | Render Starter plan, add read replica |
| Scale | 1000+ | Managed PostgreSQL (AWS RDS / Supabase) |

### 9.3 Caching Strategy

| Data | Cache | TTL | Reason |
|------|-------|-----|--------|
| Menu items | SWR client-side | 60s | Menu rarely changes, reduce API calls |
| Store status | SWR client-side | 30s | Near-real-time is sufficient |
| Revenue data | Server-side Django cache | 5min | Expensive queries, not real-time critical |

### 9.4 Handling Increased Traffic

1. **CDN:** Vercel edge network handles frontend globally
2. **Static Generation:** Menu page can be statically generated, rebuild on menu change
3. **Connection Pooling:** Use `django-db-connection-pool` for PostgreSQL
4. **Background Tasks:** Move WhatsApp sending to Celery + Redis if needed
5. **Upgrade Path:** Render Starter ($7/mo) → Professional ($25/mo)

---

## 10. Error Handling & Logging

### 10.1 Error Handling Strategy

| Layer | Strategy |
|-------|----------|
| Frontend | Try-catch on API calls, toast notifications, fallback UI states |
| API | DRF exception handler, consistent error response format |
| Backend services | Try-except with logging, graceful degradation |
| Notifications | Retry once, log failure, dashboard is fallback |
| Payments | Never create order for failed payment, log all payment events |

**Standard Error Response:**
```json
{
  "error": true,
  "code": "STORE_CLOSED",
  "message": "The store is currently closed. Please try again during business hours.",
  "details": {}
}
```

### 10.2 Logging Strategy

```python
# config/settings/base.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {'class': 'logging.FileHandler', 'filename': 'app.log'},
    },
    'loggers': {
        'orders': {'level': 'INFO'},      # Log all order events
        'notifications': {'level': 'WARNING'},  # Log failures
        'payments': {'level': 'INFO'},     # Log all payment events
    }
}
```

**What Gets Logged:**

| Event | Level | Details |
|-------|-------|---------|
| Order placed | INFO | Order ID, total, payment method |
| Order status change | INFO | Order ID, old → new status |
| WhatsApp sent | INFO | Order ID, Twilio SID |
| WhatsApp failed | ERROR | Order ID, error message |
| Payment created | INFO | Order ID, Razorpay order ID |
| Payment verified | INFO | Order ID, payment ID |
| Payment failed | ERROR | Order ID, error details |
| Admin login | INFO | IP address, success/fail |
| Rate limit hit | WARNING | IP address, endpoint |

### 10.3 Monitoring

- **Render Dashboard:** Built-in metrics (response times, errors)
- **Vercel Analytics:** Frontend performance metrics
- **Future:** Sentry for error tracking (free tier, 5000 events/month)

---

*End of TRD — Version 1.0*
