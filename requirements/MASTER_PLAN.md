# Master Plan — Restaurant Ordering System
## Step-by-Step Build Plan

**Version:** 1.0  
**Date:** 2026-03-23  
**Estimated Total Duration:** 4-5 weeks (solo developer)

---

## Phase 0: Project Setup (Day 1)

### 0.1 Repository & Tooling
- [ ] Create Git repository
- [ ] Setup monorepo structure: `/frontend` + `/backend`
- [ ] Initialize Next.js app in `/frontend`
- [ ] Initialize Django project in `/backend`
- [ ] Setup `.gitignore`, `.env.example`, `README.md`
- [ ] Setup code formatting (Prettier, Black)

### 0.2 Environment Setup
- [ ] Python 3.12 virtual environment
- [ ] Node.js 20 LTS
- [ ] Install Django + DRF + required packages
- [ ] Install Next.js + SWR + Axios + required packages

---

## Phase 1: Backend Foundation (Days 2-5)

> **Goal:** Working API with database, ready for frontend integration.

### 1.1 Django Project Structure
- [ ] Create `config/` with split settings (base, dev, prod)
- [ ] Create apps: `menu`, `orders`, `store`, `authentication`, `notifications`, `payments`
- [ ] Configure CORS, middleware, static files

### 1.2 Database Models
- [ ] `Category` + `MenuItem` models (menu app)
- [ ] `Customer` model (orders app)
- [ ] `Order` + `OrderItem` models (orders app)
- [ ] `StoreSettings` model (store app)
- [ ] Run migrations
- [ ] Create seed data (sample menu items)

### 1.3 Menu API
- [ ] `GET /api/menu/` — returns categories with items
- [ ] Menu serializers
- [ ] Test with Postman/curl

### 1.4 Order API
- [ ] `POST /api/orders/` — place order (validation, customer upsert, order creation)
- [ ] `GET /api/orders/{order_id}/` — get order details
- [ ] `GET /api/customers/{phone}/` — auto-fill returning customers
- [ ] Order service layer (business logic)
- [ ] Order ID generation (ORD-YYYYMMDD-XXXX)

### 1.5 Store API
- [ ] `GET /api/store/status/` — get store open/close + min order
- [ ] Store settings serializer

### 1.6 Admin Authentication
- [ ] JWT setup with `djangorestframework-simplejwt`
- [ ] `POST /api/auth/login/` — admin login
- [ ] `POST /api/auth/refresh/` — token refresh
- [ ] Protect admin endpoints with JWT

### 1.7 Admin APIs
- [ ] `GET /api/admin/orders/` — list all orders (filterable)
- [ ] `PATCH /api/admin/orders/{id}/status/` — update order status
- [ ] `GET /api/admin/revenue/` — revenue summary
- [ ] Admin menu CRUD endpoints
- [ ] Admin store settings endpoint

---

## Phase 2: Frontend — Customer Experience (Days 6-12)

> **Goal:** Beautiful, mobile-first customer-facing pages.

### 2.1 Design System Setup
- [ ] Global CSS: colors, typography, spacing, shadows
- [ ] Import Google Fonts (Inter or similar)
- [ ] Create design tokens (CSS custom properties)
- [ ] Create reusable components: Button, Card, Badge, Modal

### 2.2 Home / Menu Page
- [ ] Restaurant hero section (name, tagline, status banner)
- [ ] Category tabs (Starters / Mains / Drinks / Desserts)
- [ ] Menu item cards (name, price, image, Half/Full toggle, Add button)
- [ ] Out-of-stock visual state
- [ ] Store closed banner (blocks ordering)
- [ ] Floating cart icon with badge
- [ ] Mobile-first responsive layout

### 2.3 Cart Page
- [ ] Cart items list with quantity controls (+/-)
- [ ] Remove item functionality
- [ ] Size display (Half / Full)
- [ ] Running subtotal
- [ ] Minimum order value check
- [ ] "Proceed to Checkout" button
- [ ] Empty cart state
- [ ] localStorage persistence

### 2.4 Checkout Page
- [ ] Customer form: Name, Phone, Delivery Address
- [ ] Phone validation (10-digit Indian mobile)
- [ ] Auto-fill for returning customers (by phone)
- [ ] Order summary section
- [ ] Payment method selection (COD / Online)
- [ ] "Place Order" button with loading state
- [ ] Error handling and validation messages

### 2.5 Order Confirmation Page
- [ ] Order ID display
- [ ] Order summary (items, total)
- [ ] Status message ("You will receive a confirmation call")
- [ ] Estimated delivery time
- [ ] "Back to Menu" button

### 2.6 Cart Context & API Integration
- [ ] Cart React Context (add, remove, update qty, clear)
- [ ] localStorage sync
- [ ] SWR hooks for menu fetching
- [ ] Order placement API call
- [ ] Error toast notifications

---

## Phase 3: Frontend — Admin Dashboard (Days 13-18)

> **Goal:** Simple, functional admin panel for the restaurant owner.

### 3.1 Admin Login
- [ ] Password login page
- [ ] JWT token handling
- [ ] Auth context / protected routes

### 3.2 Live Orders Dashboard
- [ ] Real-time order list (polling every 5s)
- [ ] New order sound alert 🔔
- [ ] Order cards: customer info, items, total, time
- [ ] Status buttons: Pending → Preparing → Ready → Delivered
- [ ] Visual status indicators (color-coded)
- [ ] Click-to-call customer phone

### 3.3 Order History
- [ ] Order list with filters (date, status)
- [ ] Search by order ID or phone
- [ ] Pagination
- [ ] Order detail expand/modal

### 3.4 Revenue Summary
- [ ] Daily / Weekly / Monthly toggle
- [ ] Total revenue, total orders, average order value
- [ ] Payment method breakdown (COD vs Online)
- [ ] Simple chart (optional, can use Chart.js)

### 3.5 Menu Management
- [ ] List all menu items (with availability toggle)
- [ ] Add new item form (name, category, prices, image)
- [ ] Edit item
- [ ] Mark as out of stock / back in stock
- [ ] Delete item (soft delete)

### 3.6 Store Settings
- [ ] Open / Close toggle (big, prominent button)
- [ ] Minimum order value setting
- [ ] Estimated delivery time setting

---

## Phase 4: Notifications & Payments (Days 19-22)

> **Goal:** Critical integrations that make the system production-ready.

### 4.1 WhatsApp Notifications (Twilio)
- [ ] Create Twilio account + WhatsApp Sandbox
- [ ] Install `twilio` Python package
- [ ] Implement `send_order_whatsapp()` service
- [ ] Format order message template
- [ ] Trigger on new order creation
- [ ] Error handling (log failures, don't block order)
- [ ] Test with sandbox number

### 4.2 Payment Integration (Razorpay)
- [ ] Create Razorpay account
- [ ] Install `razorpay` Python package
- [ ] Backend: Create Razorpay order (`POST /api/payments/create/`)
- [ ] Backend: Verify payment signature (`POST /api/payments/verify/`)
- [ ] Frontend: Razorpay checkout JS integration
- [ ] Payment flow: Create order → Pay → Verify → Place order
- [ ] Handle payment failures gracefully
- [ ] Test with test mode keys

---

## Phase 5: Polish & Testing (Days 23-26)

> **Goal:** Production-quality reliability and UX.

### 5.1 Error Handling
- [ ] Frontend: Toast notifications for all error cases
- [ ] Frontend: Loading states for all async operations
- [ ] Frontend: Empty states (no orders, empty cart)
- [ ] Backend: Consistent error response format
- [ ] Backend: Input validation on all endpoints
- [ ] Backend: Rate limiting on orders and auth

### 5.2 UX Polish
- [ ] Micro-animations (add to cart, status change)
- [ ] Skeleton loading states
- [ ] Pull-to-refresh on admin dashboard
- [ ] Confirmation dialogs for destructive actions
- [ ] Responsive testing (320px, 375px, 768px, 1024px)

### 5.3 Testing
- [ ] Backend: Unit tests for order service, validation
- [ ] Backend: API tests for all endpoints
- [ ] Frontend: Smoke test all pages manually
- [ ] End-to-end: Place order → WhatsApp received → status updated
- [ ] Payment flow: COD + Online payment paths

### 5.4 Performance
- [ ] Lighthouse audit (target > 90 mobile)
- [ ] Image optimization (WebP, lazy loading)
- [ ] API response time check (< 500ms)

---

## Phase 6: Deployment (Days 27-28)

### 6.1 Backend Deployment (Render)
- [ ] Create `requirements.txt` / `Pipfile`
- [ ] Create `Procfile` or `render.yaml`
- [ ] Create Render PostgreSQL instance
- [ ] Deploy Django app to Render
- [ ] Set environment variables
- [ ] Run migrations on production
- [ ] Load initial menu data
- [ ] Verify API is accessible

### 6.2 Frontend Deployment (Vercel)
- [ ] Connect GitHub repo to Vercel
- [ ] Set `NEXT_PUBLIC_API_URL` environment variable
- [ ] Deploy
- [ ] Verify all pages work
- [ ] Test order flow end-to-end on production

### 6.3 DNS & Domain (Optional)
- [ ] Purchase domain
- [ ] Configure DNS on Vercel
- [ ] SSL certificate (auto via Vercel)

### 6.4 Go-Live Checklist
- [ ] All API endpoints tested on production
- [ ] WhatsApp notifications working
- [ ] Payment flow tested (Razorpay live mode)
- [ ] Admin dashboard fully functional
- [ ] Store settings configured (open hours, min order)
- [ ] Menu items populated with real data
- [ ] Mobile testing on real devices

---

## Phase 7: Post-Launch (Week 5+)

### 7.1 Monitoring
- [ ] Monitor Render logs for errors
- [ ] Monitor Vercel analytics for performance
- [ ] Track order completion rate
- [ ] Watch for failed WhatsApp notifications

### 7.2 V2 Planning
- [ ] Gather feedback from owner
- [ ] Prioritize: OTP login, order tracking, coupons
- [ ] Plan V2 sprint

---

## Build Priority Summary

| Priority | What | Why |
|----------|------|-----|
| 🔴 P0 | Backend API + Menu + Orders | Everything depends on this |
| 🔴 P0 | Customer menu + cart + checkout | Core user experience |
| 🟠 P1 | Admin dashboard (live orders) | Owner needs to manage orders |
| 🟠 P1 | WhatsApp notifications | Can't miss orders |
| 🟡 P2 | Razorpay payment | COD works meanwhile |
| 🟡 P2 | Revenue summary + menu mgmt | Nice to have for launch |
| 🟢 P3 | Polish + animations | Makes it premium |

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Render free tier cold starts (30s delay) | Upgrade to Starter ($7/mo) before launch |
| WhatsApp API approval takes time | Start with Twilio Sandbox, apply for production early |
| Razorpay account activation delay | Start with COD only, add payments when approved |
| Owner can't use dashboard | Design ultra-simple UI, train with a 5-min video |
| Database grows large | PostgreSQL handles this well, add indexes from day 1 |

---

*End of Master Plan — Version 1.0*
