import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { placeOrder } from '../services/api';

export default function Checkout() {
  const { cartItems, getCartTotal, clearCart } = useCart();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    address: ''
  });

  const subtotal = getCartTotal();
  const serviceFee = subtotal > 0 ? 4.00 : 0;
  const taxes = subtotal > 0 ? subtotal * 0.08 : 0;
  const total = subtotal + serviceFee + taxes;

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (cartItems.length === 0) return;
    
    setLoading(true);
    try {
      const orderData = {
        ...formData,
        items: cartItems,
        total,
        payment_method: 'online'
      };
      const response = await placeOrder(orderData);
      
      if (response.success) {
        clearCart();
        navigate('/success', { state: { orderId: response.order_id, total, items: cartItems } });
      }
    } catch (error) {
      console.error(error);
      alert('Failed to place order.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="pt-28 pb-20 max-w-[1440px] mx-auto w-full px-8 md:px-16 md:py-20 min-h-screen">
      <header className="mb-16">
        <h1 className="text-5xl md:text-6xl font-headline font-bold italic tracking-tight text-on-surface mb-4">Complete your journey.</h1>
        <p className="text-on-surface-variant font-body text-lg max-w-2xl leading-relaxed">Please provide your details below to finalize your order. Our chefs are standing by to prepare your sensory experience.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-16 items-start">
        {/* Checkout Form */}
        <div className="lg:col-span-7">
          <section className="space-y-12">
            <div className="bg-surface-container-low p-8 md:p-12 rounded-xl">
              <h2 className="text-2xl font-headline font-bold text-secondary mb-8">Guest Information</h2>
              <form onSubmit={handleSubmit} className="space-y-8">
                
                <div className="space-y-2">
                  <label className="block font-label text-sm uppercase tracking-widest text-on-surface-variant" htmlFor="name">Full Name</label>
                  <input required value={formData.name} onChange={handleChange} className="w-full bg-surface-container-highest border-none focus:ring-0 focus:border-b-2 focus:border-primary px-4 py-4 rounded-md transition-all font-body text-on-surface" id="name" placeholder="E.g., Julian Thorne" type="text" />
                </div>
                
                <div className="space-y-2">
                  <label className="block font-label text-sm uppercase tracking-widest text-on-surface-variant flex justify-between" htmlFor="phone">
                    Phone Number
                    <span className="text-primary text-[10px] font-bold tracking-normal italic uppercase">Required</span>
                  </label>
                  <input required value={formData.phone} onChange={handleChange} className="w-full bg-surface-container-highest border-none focus:ring-0 focus:border-b-2 focus:border-primary px-4 py-4 rounded-md transition-all font-body text-on-surface ring-1 ring-primary/10" id="phone" placeholder="+1 (555) 000-0000" type="tel" />
                  <p className="text-[11px] text-primary/80 font-medium italic">We'll text you when your order is ready.</p>
                </div>
                
                <div className="space-y-2 pt-4">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-2xl font-headline font-bold text-secondary">Delivery Details</h2>
                    <span className="font-label text-xs text-on-surface-variant italic">Optional for pickup</span>
                  </div>
                  <label className="block font-label text-sm uppercase tracking-widest text-on-surface-variant" htmlFor="address">Delivery Address</label>
                  <textarea value={formData.address} onChange={handleChange} className="w-full bg-surface-container-highest border-none focus:ring-0 focus:border-b-2 focus:border-primary px-4 py-4 rounded-md transition-all font-body text-on-surface resize-none" id="address" placeholder="Enter your street address, apartment, or suite..." rows="3"></textarea>
                </div>

                <div className="pt-8">
                  <button disabled={loading || cartItems.length === 0} type="submit" className="w-full bg-primary text-on-primary font-headline font-bold text-xl py-5 rounded-md hover:bg-primary-container transition-all duration-300 shadow-xl shadow-primary/10 scale-100 active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed">
                    {loading ? 'Processing...' : 'Place Order'}
                  </button>
                  <p className="text-center mt-6 text-on-surface-variant text-sm font-body italic">
                    By placing your order, you agree to our <a className="underline decoration-outline-variant hover:text-primary transition-colors" href="#">Terms of Service</a>.
                  </p>
                </div>
              </form>
            </div>
          </section>
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-5 sticky top-32">
          <div className="bg-surface-container-low rounded-xl overflow-hidden">
            <div className="h-48 w-full overflow-hidden relative">
              <img alt="Gourmet saffron dish" className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDp3R4DtrFcw1IumH8-QYaeRRA_XADao5j6p1B6rr9mGtW6MRfA8SnG88Pa4FWkeQoTzkjY64QuhZkruN-R9JbXtX5j-ezNT1IExbPh5Qj-8-J2640BSnUpkVpwJjX6pDCjVJFw3SHNpi0y2QWv6ESO63j6dRxi0YkkC3vMy7jibi_JNg4tYujWn88h7zus09TFfwqwyTls7BSSqm5byOUoI7k1XWRJRhR76Bnmgtt_S2we1Qeu627EoaKYWWpiH6i4VWm33sMEzvOp" />
              <div className="absolute inset-0 bg-gradient-to-t from-surface-container-low to-transparent"></div>
              <div className="absolute bottom-4 left-8">
                <span className="bg-tertiary-container text-on-tertiary-container text-[10px] font-label uppercase tracking-[0.2em] px-3 py-1 rounded-full">Your Selection</span>
              </div>
            </div>

            <div className="p-8 md:p-10 space-y-10">
              <h3 className="text-3xl font-headline font-bold text-on-surface italic">The Spice Basket</h3>
              <div className="space-y-8">
                {cartItems.map((item) => (
                  <div key={item.id} className="flex justify-between items-start">
                    <div className="space-y-1">
                      <p className="font-headline text-lg text-on-surface font-bold">{item.name} x {item.quantity}</p>
                    </div>
                    <span className="font-body font-semibold text-secondary">₹{(item.price * item.quantity).toFixed(2)}</span>
                  </div>
                ))}
              </div>

              {/* Pricing Breakdown */}
              <div className="pt-10 space-y-4">
                <div className="flex justify-between items-center text-sm font-label uppercase tracking-widest text-on-surface-variant">
                  <span>Subtotal</span>
                  <span>₹{subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-sm font-label uppercase tracking-widest text-on-surface-variant">
                  <span>Service Fee</span>
                  <span>₹{serviceFee.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-sm font-label uppercase tracking-widest text-on-surface-variant pb-6">
                  <span>Tax (8%)</span>
                  <span>₹{taxes.toFixed(2)}</span>
                </div>

                {/* Total */}
                <div className="border-t border-outline-variant/30 pt-8 flex justify-between items-end">
                  <div>
                    <p className="font-label text-xs uppercase tracking-[0.3em] text-on-surface-variant mb-1">Total Amount</p>
                    <p className="font-headline text-4xl font-bold text-primary">₹{total.toFixed(2)}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
