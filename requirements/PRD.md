# Product Requirements Document (PRD)
## Restaurant Ordering Website

**Version:** 1.0  
**Date:** 2026-03-23  
**Author:** Engineering Team  
**Status:** Draft

---

## 1. Product Summary

### Problem Statement

Local restaurants lose potential orders because they rely solely on phone calls and walk-ins. Customers have no way to browse the menu online, and the owner has no centralized system to track and manage incoming orders — leading to missed orders, miscommunication, and revenue loss.

### Solution Overview

A mobile-first restaurant ordering website where:
- **Customers** can browse the full menu, add items to a cart, and place delivery orders with just their name and phone number.
- **Restaurant owner** receives instant WhatsApp notifications + dashboard sound alerts for every new order, and can manage order lifecycle from a simple admin panel.

### Target Users

| User | Profile |
|------|---------|
| **Customers** | Local residents, non-technical, primarily mobile users who want fast ordering without creating accounts |
| **Restaurant Owner** | Non-technical business owner who needs a simple, reliable way to receive and manage orders |

---

## 2. Goals & Objectives

### Business Goals

| # | Goal | Metric |
|---|------|--------|
| 1 | Increase order volume by offering online ordering | Orders per day |
| 2 | Zero missed orders | Missed order rate = 0% |
| 3 | Reduce phone call load for order-taking | % reduction in order calls |
| 4 | Build customer order history for repeat business | Returning customer rate |

### User Goals

**Customer Goals:**
- Browse the complete menu with prices quickly
- Place an order in under 2 minutes
- Know that the order was received (confirmation call from restaurant)
- Get delivery at their address

**Owner Goals:**
- Get instantly notified of every new order
- See all incoming orders in one place
- Track order status (Preparing → Ready → Delivered)
- View daily/weekly revenue summary
- Control store open/close status

---

## 3. User Personas

### Persona 1: Rahul (Customer)

- **Age:** 28
- **Tech comfort:** Uses WhatsApp, Swiggy, Instagram daily
- **Behavior:** Wants to order food quickly without downloading an app or creating an account
- **Pain point:** Calling the restaurant is slow, line is often busy
- **Goal:** Browse menu → pick items → place order → get delivery

### Persona 2: Sharma Ji (Restaurant Owner)

- **Age:** 50
- **Tech comfort:** Uses WhatsApp, basic smartphone usage
- **Behavior:** Runs the kitchen, checks phone between orders
- **Pain point:** Misses phone orders during rush hours, no record of orders
- **Goal:** Get notified on WhatsApp → confirm order by calling → track order status → see revenue

---

## 4. User Flows

### 4.1 Customer Journey

```
┌─────────────┐     ┌──────────────┐     ┌──────────┐     ┌───────────────┐
│  Open Site   │────→│  Browse Menu │────→│ Add to   │────→│  View Cart    │
│  (Mobile)    │     │  (4 tabs)    │     │ Cart     │     │  (Edit qty)   │
└─────────────┘     └──────────────┘     └──────────┘     └───────┬───────┘
                                                                   │
                                                                   ▼
┌─────────────┐     ┌──────────────┐     ┌──────────┐     ┌───────────────┐
│  Order      │←────│  Choose      │←────│ Enter    │←────│  Checkout     │
│  Confirmed  │     │  Payment     │     │ Details  │     │  Page         │
│  Page       │     │  (COD/Online)│     │ (Name,   │     │               │
└─────────────┘     └──────────────┘     │ Phone,   │     └───────────────┘
                                          │ Address) │
                                          └──────────┘
```

**Detailed Steps:**
1. Customer opens the website on mobile
2. Sees the menu organized in 4 tabs: **Starters | Mains | Drinks | Desserts**
3. Each item shows: name, price (Half/Full), and an "Add" button
4. Selects size (Half/Full) and quantity, adds to cart
5. Floating cart icon shows item count
6. Opens cart → can edit quantities or remove items
7. Proceeds to checkout → enters Name, Phone, Delivery Address
8. Selects payment method: **COD** or **Online Payment**
9. If online → redirected to payment gateway → payment confirmed
10. Order placed → sees confirmation page with Order ID
11. Restaurant calls to confirm the order
12. Customer receives delivery

### 4.2 Owner Journey

```
┌──────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│  WhatsApp    │────→│  Open Admin  │────→│  View Order   │────→│  Call        │
│  Notification│     │  Dashboard   │     │  Details      │     │  Customer    │
└──────────────┘     └──────────────┘     └───────────────┘     └──────┬───────┘
                                                                        │
                                                                        ▼
┌──────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│  Mark as     │←────│  Mark as     │←────│  Mark as      │←────│  Confirm     │
│  "Delivered" │     │  "Ready"     │     │  "Preparing"  │     │  Order       │
└──────────────┘     └──────────────┘     └───────────────┘     └──────────────┘
```

**Detailed Steps:**
1. New order placed → owner gets WhatsApp message with order summary
2. Dashboard plays a sound alert
3. Owner opens dashboard → sees new order highlighted
4. Reviews order details (items, qty, total, customer info)
5. Calls customer to confirm
6. Marks order as **"Preparing"**
7. When food is ready → marks as **"Ready"**
8. When handed to delivery → marks as **"Delivered"**

---

## 5. Features (MVP)

### 5.1 Menu Display
- 4-tab layout: Starters, Mains, Drinks, Desserts
- Each item: name, description (optional), image (optional), price
- Size variants: Half / Full with separate prices
- Items can be marked as "Out of Stock" by admin
- Store open/close banner — if closed, ordering is disabled

### 5.2 Cart System
- Floating cart icon with item count badge
- Add items with size selection (Half/Full) and quantity
- Cart page: view all items, edit quantity, remove items
- Cart total with minimum order value check for delivery
- Cart persists in browser (localStorage)

### 5.3 Checkout
- Fields: Customer Name, Phone Number, Delivery Address
- Phone number validation (10-digit Indian mobile)
- Payment method selection: COD or Online
- Order summary before final confirmation
- Minimum order value enforcement

### 5.4 Order Placement
- Order saved to database with unique Order ID
- Order status initialized to **"Pending"**
- WhatsApp notification sent to owner
- Sound alert on admin dashboard
- Confirmation page shown to customer with Order ID

### 5.5 Admin Order Management
- Protected admin dashboard (password login)
- **Live Orders:** Real-time incoming orders with sound alert
- **Order Status Update:** Pending → Preparing → Ready → Delivered
- **Order History:** Filterable by date, status
- **Revenue Summary:** Daily, weekly, monthly revenue totals
- **Store Control:** Open/Close toggle
- **Menu Management:** Add, edit, delete menu items; mark out of stock

### 5.6 Notifications
- WhatsApp message to owner on every new order (via Twilio/Interakt)
- Sound alert on dashboard for new orders
- Order details included in WhatsApp message

---

## 6. Out of Scope (V1)

| Feature | Reason | Future Version |
|---------|--------|----------------|
| Customer login/signup | Keep friction low for MVP | V2 (OTP login) |
| Customer-facing order tracking | Owner calls to confirm, manual process | V2 |
| Advanced analytics | Revenue summary is enough for MVP | V2 |
| Multiple restaurant support | Single restaurant focus | V3 |
| Coupon/discount system | Not needed for launch | V2 |
| Reviews and ratings | Not needed for launch | V3 |
| Dine-in / Pickup mode | Delivery only for MVP | V2 |
| Multi-language support | English only for MVP | V2 |

---

## 7. Functional Requirements

### FR-1: Menu Display
| ID | Requirement |
|----|-------------|
| FR-1.1 | System shall display menu items grouped by category (Starters, Mains, Drinks, Desserts) |
| FR-1.2 | Each item shall display name, price (Half & Full), and optional image |
| FR-1.3 | Items marked "out of stock" shall be visually disabled and non-orderable |
| FR-1.4 | If store is closed, a banner shall be displayed and "Add to Cart" buttons disabled |

### FR-2: Cart
| ID | Requirement |
|----|-------------|
| FR-2.1 | User shall be able to add items with size (Half/Full) and quantity selection |
| FR-2.2 | Cart shall persist across page refreshes using localStorage |
| FR-2.3 | User shall be able to modify quantity or remove items from cart |
| FR-2.4 | Cart shall display running total |
| FR-2.5 | System shall enforce minimum order value before allowing checkout |

### FR-3: Checkout & Order Placement
| ID | Requirement |
|----|-------------|
| FR-3.1 | Checkout form shall require: Name, Phone (10-digit), Delivery Address |
| FR-3.2 | Phone number shall be validated as a 10-digit Indian mobile number |
| FR-3.3 | User shall select payment method: COD or Online |
| FR-3.4 | On successful order, system shall generate a unique Order ID |
| FR-3.5 | Confirmation page shall display Order ID, order summary, and estimated wait time |
| FR-3.6 | If phone number has previous orders, system shall auto-fill name and address |

### FR-4: Admin Dashboard
| ID | Requirement |
|----|-------------|
| FR-4.1 | Admin shall log in with a simple password |
| FR-4.2 | Dashboard shall display new orders in real-time with a sound alert |
| FR-4.3 | Admin shall be able to update order status: Pending → Preparing → Ready → Delivered |
| FR-4.4 | Admin shall view order history with date and status filters |
| FR-4.5 | Dashboard shall show revenue summary (daily, weekly, monthly) |
| FR-4.6 | Admin shall be able to toggle store open/close |
| FR-4.7 | Admin shall manage menu items (CRUD + out-of-stock toggle) |

### FR-5: Notifications
| ID | Requirement |
|----|-------------|
| FR-5.1 | System shall send a WhatsApp message to owner when a new order is placed |
| FR-5.2 | WhatsApp message shall include: Order ID, items, total, customer name & phone |
| FR-5.3 | Dashboard shall play an audio alert when a new order is received |

---

## 8. Non-Functional Requirements

### Performance
| ID | Requirement |
|----|-------------|
| NFR-1 | Menu page shall load in under 2 seconds on 4G mobile |
| NFR-2 | Order placement shall complete in under 3 seconds |
| NFR-3 | Admin dashboard shall reflect new orders within 5 seconds |

### Reliability
| ID | Requirement |
|----|-------------|
| NFR-4 | System shall have 99.5% uptime |
| NFR-5 | No order shall be lost — if WhatsApp fails, dashboard alert is the fallback |
| NFR-6 | Failed payment transactions shall not create orders |

### Mobile Responsiveness
| ID | Requirement |
|----|-------------|
| NFR-7 | All customer-facing pages shall be mobile-first and work on screens ≥ 320px |
| NFR-8 | Touch targets shall be minimum 44×44px |
| NFR-9 | Cart and checkout must be thumb-friendly (bottom-anchored actions) |

### Security
| ID | Requirement |
|----|-------------|
| NFR-10 | Admin dashboard shall be password-protected |
| NFR-11 | All API endpoints shall validate input data |
| NFR-12 | Rate limiting on order placement (max 5 orders per phone per hour) |

---

## 9. Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Order completion rate | > 70% of cart → order | Track cart creates vs orders placed |
| Missed orders | 0% | Check if every order triggers WhatsApp + dashboard alert |
| Page load time (mobile) | < 2 seconds | Lighthouse performance audit |
| Order placement time | < 3 seconds | API response time monitoring |
| Customer return rate | > 30% in first month | Track orders by phone number |
| Daily order volume | Baseline + 20% growth | Dashboard revenue summary |

---

## 10. Future Enhancements (Post-MVP)

### V2 (Month 2-3)
- OTP-based customer login
- Customer order tracking page
- Pickup / Dine-in ordering modes
- Coupon & discount system
- Customer SMS/WhatsApp order confirmation

### V3 (Month 4-6)
- Advanced analytics dashboard
- Multi-language support (Hindi)
- Customer reviews & ratings
- Loyalty / rewards program
- Push notifications (PWA)

### V4 (Month 6+)
- Multi-branch support
- Delivery partner integration
- Inventory management
- Kitchen display system (KDS)

---

*End of PRD — Version 1.0*
