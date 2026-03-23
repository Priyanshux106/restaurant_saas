import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';

export default function Cart() {
  const { cartItems, removeFromCart, updateQuantity, getCartTotal } = useCart();
  const navigate = useNavigate();

  const subtotal = getCartTotal();
  const serviceFee = subtotal > 0 ? 4.50 : 0;
  const taxes = subtotal > 0 ? subtotal * 0.08 : 0; // 8% tax
  const total = subtotal + serviceFee + taxes;

  return (
    <main className="pt-28 pb-20 px-4 md:px-8 max-w-screen-2xl mx-auto min-h-screen">
      <header className="mb-16">
        <h1 className="text-5xl font-bold text-on-surface leading-tight font-headline">Your Selection</h1>
        <p className="text-on-surface-variant font-body mt-4 tracking-wide">A curated collection of your gastronomic desires.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-16 items-start">
        {/* Cart Items List */}
        <div className="lg:col-span-8 space-y-12">
          {cartItems.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-24 text-center">
              <div className="w-64 h-64 mb-8 bg-surface-container-low rounded-full flex items-center justify-center">
                <span className="material-symbols-outlined text-7xl text-stone-300">shopping_basket</span>
              </div>
              <h2 className="text-3xl font-bold mb-4 font-headline">Your cart is empty</h2>
              <p className="text-on-surface-variant mb-8 max-w-xs font-body">It seems you haven't discovered our delicacies yet.</p>
              <Link to="/#menu" className="bg-primary text-on-primary px-10 py-4 rounded-md font-bold uppercase tracking-widest hover:opacity-90 transition-all text-sm font-label">
                Browse Menu
              </Link>
            </div>
          ) : (
            cartItems.map((item) => (
              <div key={item.id} className="flex flex-col md:flex-row gap-8 items-center md:items-start group transition-all duration-500">
                <div className="w-full md:w-48 h-48 flex-shrink-0 overflow-hidden rounded-xl shadow-lg shadow-on-surface/5">
                  <img
                    alt={item.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                    src={item.image}
                  />
                </div>
                <div className="flex-grow flex flex-col justify-between py-2 w-full">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-2xl font-bold mb-1 font-headline">{item.name}</h3>
                      <p className="text-on-surface-variant text-sm font-body max-w-md">{item.description}</p>
                    </div>
                    <span className="text-xl font-bold font-serif">₹{item.price.toFixed(2)}</span>
                  </div>

                  <div className="flex items-center justify-between mt-8">
                    <div className="flex items-center gap-6 bg-surface-container-low px-4 py-2 rounded-full">
                      <button onClick={() => updateQuantity(item.id, item.quantity - 1)} className="hover:text-primary transition-colors flex items-center justify-center">
                        <span className="material-symbols-outlined text-lg">remove</span>
                      </button>
                      <span className="font-bold text-lg font-body w-4 text-center">{item.quantity}</span>
                      <button onClick={() => updateQuantity(item.id, item.quantity + 1)} className="hover:text-primary transition-colors flex items-center justify-center">
                        <span className="material-symbols-outlined text-lg">add</span>
                      </button>
                    </div>
                    <button onClick={() => removeFromCart(item.id)} className="text-on-surface-variant hover:text-error flex items-center gap-2 transition-colors uppercase tracking-widest text-xs font-semibold font-label">
                      <span className="material-symbols-outlined text-sm">delete</span>
                      Remove
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Sticky Summary */}
        <aside className="lg:col-span-4 sticky top-32">
          <div className="bg-surface-container-low p-8 rounded-xl">
            <h2 className="text-2xl font-bold mb-8 border-b border-outline-variant/20 pb-4 font-headline">Order Summary</h2>
            <div className="space-y-4 mb-8">
              <div className="flex justify-between font-body">
                <span className="text-on-surface-variant">Subtotal</span>
                <span className="font-medium">₹{subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between font-body">
                <span className="text-on-surface-variant">Service Fee</span>
                <span className="font-medium">₹{serviceFee.toFixed(2)}</span>
              </div>
              <div className="flex justify-between font-body">
                <span className="text-on-surface-variant">Estimated Taxes</span>
                <span className="font-medium">₹{taxes.toFixed(2)}</span>
              </div>
              <div className="flex justify-between font-body text-tertiary">
                <span className="flex items-center gap-2 text-sm">
                  <span className="material-symbols-outlined text-sm">local_shipping</span>
                  Delivery Fee
                </span>
                <span className="font-medium inline-block">Free</span>
              </div>
            </div>

            <div className="border-t border-outline-variant/30 pt-6 mb-8">
              <div className="flex justify-between items-baseline">
                <span className="text-xl font-bold font-headline">Total</span>
                <div className="text-right">
                  <span className="text-3xl font-bold font-serif text-primary">₹{total.toFixed(2)}</span>
                  <p className="text-[10px] uppercase tracking-tighter text-on-surface-variant mt-1">Inclusive of all duties</p>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <button
                onClick={() => navigate('/checkout')}
                disabled={cartItems.length === 0}
                className="w-full bg-primary disabled:opacity-50 disabled:cursor-not-allowed text-on-primary py-5 rounded-md font-bold text-lg uppercase tracking-widest shadow-xl shadow-primary/20 hover:bg-primary-container transition-all flex items-center justify-center gap-3 group font-label"
              >
                Proceed to Checkout
                <span className="material-symbols-outlined group-hover:translate-x-1 transition-transform">arrow_forward</span>
              </button>
              <p className="text-center text-xs text-on-surface-variant font-body px-4">
                By proceeding, you agree to our <a className="underline text-primary" href="#">Terms of Service</a> and <a className="underline text-primary" href="#">Privacy Policy</a>.
              </p>
            </div>
          </div>
          
          <div className="mt-8 bg-secondary-container/10 p-6 rounded-xl border border-secondary-container/20 flex gap-4 items-center">
            <span className="material-symbols-outlined text-secondary text-3xl">auto_awesome</span>
            <div>
              <p className="text-sm font-bold text-on-secondary-container font-headline">Unlock 15% Savings</p>
              <p className="text-xs text-on-secondary-container/80 font-body">Add ₹20 more to your order for a secret spice reward.</p>
            </div>
          </div>
        </aside>
      </div>
    </main>
  );
}
