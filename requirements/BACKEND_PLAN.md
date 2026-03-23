# Backend Implementation Plan
## Restaurant Ordering System — Django + DRF

**Version:** 1.0  
**Date:** 2026-03-23  
**Scope:** Backend only (`/backend` folder)

---

## Overview

Build a production-ready Django REST API backend for the restaurant ordering system. The backend exposes all endpoints consumed by the Next.js frontend, handles order processing, WhatsApp notifications, and Razorpay payments.

**Tech Stack:** Python 3.12, Django 5.x, Django REST Framework 3.15, SQLite (dev) → PostgreSQL (prod), Twilio WhatsApp, Razorpay, Gunicorn

---

## Folder Structure (Target)

```
backend/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Procfile                      ← Render deploy config
├── render.yaml                   ← Render IaC config
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── menu/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── orders/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py              ← Order creation logic
│   ├── views.py
│   └── urls.py
├── store/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── authentication/
│   ├── __init__.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── notifications/
│   ├── __init__.py
│   └── services.py              ← Twilio WhatsApp
├── payments/
│   ├── __init__.py
│   ├── services.py              ← Razorpay
│   ├── views.py
│   └── urls.py
└── fixtures/
    └── initial_data.json         ← Seed data (menu items)
```

---

## Sub-Task Breakdown

### 🟦 Task B1: Project Setup & Configuration
**Files:** `requirements.txt`, `config/settings/*.py`, `config/urls.py`, `.env.example`, `.gitignore`

- Initialize Django project with `django-admin startproject config .`
- Split settings into `base.py` / `development.py` / `production.py`
- Install and configure: `djangorestframework`, `django-cors-headers`, `python-dotenv`, `djangorestframework-simplejwt`
- Set `DJANGO_SETTINGS_MODULE=config.settings.development` in dev
- Configure CORS: allow all origins in dev, restrict in prod
- Configure logging (console + file)
- Create `.env.example` with all required variables
- Create `requirements.txt`

**Packages:**
```
django==5.1
djangorestframework==3.15
django-cors-headers==4.4
python-dotenv==1.0
djangorestframework-simplejwt==5.3
twilio==9.3
razorpay==1.4
gunicorn==22.0
dj-database-url==2.2          ← PostgreSQL URL parsing for Render
whitenoise==6.7                ← Static files serving
```

---

### 🟦 Task B2: Database Models
**Files:** `menu/models.py`, `orders/models.py`, `store/models.py`

**menu/models.py:**
- `Category`: id, name, display_order, is_active
- `MenuItem`: id, category(FK), name, description, image(URL), half_price(nullable), full_price, is_available, is_active, display_order, created_at, updated_at

**orders/models.py:**
- `Customer`: id, phone(unique, indexed), name, address, created_at, updated_at
- `Order`: id, order_id(unique, indexed), customer(FK), delivery_address, status(choices), payment_method(choices), payment_status, payment_id, subtotal, total, special_instructions, created_at, updated_at
- `OrderItem`: id, order(FK), menu_item(FK→PROTECT), item_name(snapshot), size(choices), quantity, unit_price(snapshot), total_price

**store/models.py:**
- `StoreSettings`: id, is_open, min_order_value, store_name, store_phone, owner_whatsapp, estimated_delivery_time, updated_at

Run migrations. Create initial `StoreSettings` object via migration.

---

### 🟦 Task B3: Menu API
**Files:** `menu/serializers.py`, `menu/views.py`, `menu/urls.py`

**Endpoints:**
- `GET /api/menu/` → Returns all active categories + available items + store open status + min_order_value

**Logic:**
- `CategorySerializer` (nested `MenuItemSerializer`)
- Filter: `is_active=True` for category, `is_active=True` for menu items
- Include `store_open` and `min_order_value` from `StoreSettings` in response
- `MenuItemSerializer` excludes admin-only fields like `is_active`

---

### 🟦 Task B4: Store Status API
**Files:** `store/serializers.py`, `store/views.py`, `store/urls.py`

**Endpoints:**
- `GET /api/store/status/` → `{is_open, min_order_value, store_name, estimated_delivery_time}`

**Logic:**
- Singleton pattern: always return first `StoreSettings` record

---

### 🟦 Task B5: Order API (Public)
**Files:** `orders/models.py`, `orders/serializers.py`, `orders/services.py`, `orders/views.py`, `orders/urls.py`

**Endpoints:**
- `POST /api/orders/` → Place new order
- `GET /api/orders/{order_id}/` → Get order by order_id
- `GET /api/customers/{phone}/` → Get customer for auto-fill

**Order Placement Logic (`orders/services.py`):**
1. Validate store is open → raise `ServiceError("STORE_CLOSED")` if not
2. Validate each item: exists, `is_available=True`, valid size
3. Calculate item totals (snapshot prices from DB)
4. Calculate subtotal + total
5. Check total ≥ min_order_value
6. Upsert `Customer` (update name/address if phone exists)
7. Generate unique `order_id`: `ORD-{YYYYMMDD}-{4-digit-seq}`
8. Create `Order` record
9. Create `OrderItem` records (bulk_create)
10. Trigger WhatsApp notification (non-blocking, try/except)
11. Return order data

**Validation Rules (in serializer):**
- `customer_phone`: regex `^[6-9]\d{9}$`
- `customer_name`: 2-100 chars
- `delivery_address`: 10-500 chars
- `items`: min 1 item
- `quantity`: 1-20
- `payment_method`: `cod` or `online`
- `size`: `half` or `full`
- If `size=half` and `half_price` is null → validation error

**Custom Exception Handler:**
```python
# config/exceptions.py
def custom_exception_handler(exc, context):
    # Returns: {"error": true, "code": "...", "message": "..."}
```

---

### 🟦 Task B6: Authentication
**Files:** `authentication/views.py`, `authentication/serializers.py`, `authentication/urls.py`

**Endpoints:**
- `POST /api/auth/login/` → takes `{username, password}`, returns JWT pair
- `POST /api/auth/refresh/` → takes `{refresh}`, returns new access token
- `POST /api/auth/logout/` → blacklist refresh token

**Logic:**
- Use Django's default `User` model + `djangorestframework-simplejwt`
- Create superuser via management command or `createsuperuser`
- JWT settings: access token 15min, refresh token 7 days
- Custom login view to return `{access, refresh, username}`

---

### 🟦 Task B7: Admin Order Management APIs
**Files:** `orders/views.py` (admin section), `orders/serializers.py`

**Endpoints (all require `IsAuthenticated`):**
- `GET /api/admin/orders/` → list orders with filters (`status`, `date`, `search`)
  - Query params: `?status=pending&date=2026-03-23&search=phone/order_id`
  - Order by: `-created_at` (newest first)
  - Pagination: 20 per page
- `GET /api/admin/orders/{id}/` → single order detail
- `PATCH /api/admin/orders/{id}/status/` → update status
  - Validates status transition: pending→confirmed/preparing, preparing→ready, ready→delivered
  - Logs the status change

**AdminOrderSerializer:** Full detail including customer phone, address, payment info.

---

### 🟦 Task B8: Admin Menu Management APIs
**Files:** `menu/views.py` (admin section), `menu/serializers.py`

**Endpoints (all require `IsAuthenticated`):**
- `GET /api/admin/menu/` → all items (including unavailable + inactive)
- `POST /api/admin/menu/` → create item
- `PUT /api/admin/menu/{id}/` → full update
- `PATCH /api/admin/menu/{id}/availability/` → toggle `is_available`
- `DELETE /api/admin/menu/{id}/` → soft delete (set `is_active=False`)

**AdminMenuItemSerializer:** All fields including `is_available`, `is_active`, `display_order`.

---

### 🟦 Task B9: Admin Revenue API
**Files:** `orders/views.py` (revenue section)

**Endpoint:**
- `GET /api/admin/revenue/?period=daily|weekly|monthly`

**Logic (using Django ORM aggregation):**
```python
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncDate

Order.objects.filter(
    created_at__date=today,
    status__in=['delivered', 'ready']
).aggregate(
    total_revenue=Sum('total'),
    total_orders=Count('id'),
    avg_order_value=Avg('total')
)
```
- `daily`: filter by today
- `weekly`: filter by last 7 days (grouped by day for chart data)
- `monthly`: filter by current month (grouped by day)
- Payment breakdown: COD vs Online totals separately

---

### 🟦 Task B10: Admin Store Settings API
**Files:** `store/views.py`, `store/serializers.py`

**Endpoints (require `IsAuthenticated`):**
- `GET /api/admin/store/settings/` → full store settings
- `PUT /api/admin/store/settings/` → update settings (open/close, min_order, times)

---

### 🟦 Task B11: Notification Service (WhatsApp)
**Files:** `notifications/services.py`

**Function:** `send_order_notification(order)`
- Format WhatsApp message using template from TRD
- Send via Twilio Client
- Log success (INFO) or failure (ERROR)
- On failure: **do NOT raise exception** — order is already placed, dashboard is fallback

**Message includes:** Order ID, customer name+phone, delivery address, item list with size+qty+price, total, payment method, timestamp

---

### 🟦 Task B12: Payment Integration (Razorpay)
**Files:** `payments/services.py`, `payments/views.py`, `payments/urls.py`

**Endpoints:**
- `POST /api/payments/create/` → Create Razorpay order
  - Request: `{order_total, currency: "INR"}`
  - Response: `{razorpay_order_id, amount, currency, key_id}`
- `POST /api/payments/verify/` → Verify payment signature
  - Request: `{razorpay_order_id, razorpay_payment_id, razorpay_signature, our_order_id}`
  - On success: update `Order.payment_status = 'paid'`, `payment_id = razorpay_payment_id`
  - On failure: return error, do NOT mark order as paid

**Signature Verification:**
```python
import hmac, hashlib
generated = hmac.new(
    key_secret.encode(),
    f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
    hashlib.sha256
).hexdigest()
assert generated == razorpay_signature
```

---

### 🟦 Task B13: Seed Data & Django Admin
**Files:** `fixtures/initial_data.json`, `menu/admin.py`, `orders/admin.py`

- Register all models in Django admin (for direct management if needed)
- Create `fixtures/initial_data.json` with:
  - 4 categories (Starters, Mains, Drinks, Desserts)
  - ~15 sample menu items across categories
  - Initial `StoreSettings` record
- Load with: `python manage.py loaddata fixtures/initial_data.json`

---

### 🟦 Task B14: Rate Limiting & Security
**Files:** `config/settings/base.py`

- DRF throttling for order endpoint: 5/hour per phone (custom throttle class)
- DRF throttling for login: 5/15min per IP
- `ALLOWED_HOSTS` set correctly in production
- `SECRET_KEY` from env var
- `DEBUG=False` in production

---

### 🟦 Task B15: Deployment Config
**Files:** `Procfile`, `render.yaml`, `.env.example`

```
# Procfile
web: gunicorn config.wsgi:application --workers 2 --bind 0.0.0.0:$PORT
```

---

## API Summary Table

| # | Method | Endpoint | Auth | Description |
|---|--------|----------|------|-------------|
| 1 | GET | `/api/menu/` | None | Full menu + store status |
| 2 | GET | `/api/store/status/` | None | Store open/close |
| 3 | POST | `/api/orders/` | None | Place order |
| 4 | GET | `/api/orders/{order_id}/` | None | Get order by ID |
| 5 | GET | `/api/customers/{phone}/` | None | Auto-fill customer |
| 6 | POST | `/api/payments/create/` | None | Create Razorpay order |
| 7 | POST | `/api/payments/verify/` | None | Verify payment |
| 8 | POST | `/api/auth/login/` | None | Admin login |
| 9 | POST | `/api/auth/refresh/` | None | Refresh token |
| 10 | GET | `/api/admin/orders/` | JWT | List all orders |
| 11 | GET | `/api/admin/orders/{id}/` | JWT | Order detail |
| 12 | PATCH | `/api/admin/orders/{id}/status/` | JWT | Update status |
| 13 | GET | `/api/admin/revenue/` | JWT | Revenue summary |
| 14 | GET | `/api/admin/menu/` | JWT | All menu items |
| 15 | POST | `/api/admin/menu/` | JWT | Create item |
| 16 | PUT | `/api/admin/menu/{id}/` | JWT | Update item |
| 17 | PATCH | `/api/admin/menu/{id}/availability/` | JWT | Toggle availability |
| 18 | DELETE | `/api/admin/menu/{id}/` | JWT | Soft delete |
| 19 | GET | `/api/admin/store/settings/` | JWT | Get settings |
| 20 | PUT | `/api/admin/store/settings/` | JWT | Update settings |

---

## Verification Plan

### Automated Testing (using Django TestCase + DRF APIClient)

Run all tests with:
```bash
cd backend
python manage.py test --verbosity=2
```

**Test file locations:**
- `menu/tests.py` — Menu API tests
- `orders/tests.py` — Order placement, validation, customer upsert
- `store/tests.py` — Store status API
- `authentication/tests.py` — Login, JWT, protected routes
- `payments/tests/test_services.py` — Razorpay signature verification

**Key test cases:**
1. `GET /api/menu/` returns correct structure (categories + items)
2. `POST /api/orders/` with valid data → creates order, returns order_id
3. `POST /api/orders/` when store is closed → 400 error with `STORE_CLOSED`
4. `POST /api/orders/` with invalid phone → 400 validation error
5. `POST /api/orders/` below min order value → 400 error
6. `POST /api/orders/` with unavailable item → 400 error
7. `GET /api/admin/orders/` without auth → 401
8. `GET /api/admin/orders/` with valid JWT → 200 with order list
9. `PATCH /api/admin/orders/{id}/status/` → status updated correctly
10. Payment verification: valid signature → success, invalid → 400

### Manual API Testing (Postman/curl)

After running `python manage.py runserver`:

```bash
# 1. Get menu
curl http://localhost:8000/api/menu/

# 2. Place order
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"Test","customer_phone":"9876543210","delivery_address":"Test address here 123","payment_method":"cod","items":[{"menu_item_id":1,"size":"full","quantity":1}]}'

# 3. Admin login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your-password"}'

# 4. Get admin orders (use token from step 3)
curl http://localhost:8000/api/admin/orders/ \
  -H "Authorization: Bearer <token>"
```

---

## Build Order (sequence matters)

```
B1 (setup) → B2 (models) → B3 (menu API) → B4 (store API) → B6 (auth) →
B5 (order API + services) → B7 (admin orders) → B8 (admin menu) →
B9 (revenue) → B10 (admin settings) → B11 (WhatsApp) → B12 (payments) →
B13 (seed data) → B14 (rate limiting) → B15 (deploy config)
```

---

*End of Backend Implementation Plan — v1.0*
