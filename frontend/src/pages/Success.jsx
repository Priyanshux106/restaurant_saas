import { Link, useLocation } from 'react-router-dom';

export default function Success() {
  const location = useLocation();
  const { orderId, total, items } = location.state || { orderId: 'SH-829104', total: 44.50, items: [] };

  return (
    <main className="flex-grow flex items-center justify-center px-4 py-28 min-h-screen">
      <div className="max-w-2xl w-full text-center">
        {/* Success Status Section */}
        <section className="mb-12">
          <div className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-tertiary-container mb-8 shadow-sm">
            <span className="material-symbols-outlined text-white text-5xl" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-on-surface mb-4 leading-tight font-headline">
            Your order has been placed successfully!
          </h1>
          <p className="text-on-surface-variant font-light text-lg italic mb-2 font-headline">Order #{orderId}</p>
          <div className="bg-surface-container-low py-3 px-6 rounded-lg inline-block text-secondary font-medium font-body">
            The restaurant will call you to confirm your order.
          </div>
        </section>

        {/* Order Summary Bento Grid */}
        <section className="bg-surface-container-low rounded-xl p-8 mb-10 text-left border-l-4 border-primary">
          <h2 className="text-2xl font-bold mb-8 text-on-surface font-headline">Order Summary</h2>
          <div className="space-y-6">
            {items && items.length > 0 ? items.map((item, index) => (
              <div key={index} className="flex justify-between items-start">
                <div>
                  <p className="font-semibold text-on-surface font-headline">{item.name} x {item.quantity}</p>
                </div>
                <span className="text-on-surface font-medium font-body">₹{(item.price * item.quantity).toFixed(2)}</span>
              </div>
            )) : (
              <div className="flex justify-between items-start">
                  <div>
                    <p className="font-semibold text-on-surface font-headline">Your Items</p>
                  </div>
              </div>
            )}
          </div>

          <div className="mt-10 pt-8 border-t border-outline-variant/30">
            <div className="flex justify-between items-center">
              <span className="text-xl font-bold text-on-surface font-headline">Total</span>
              <span className="text-2xl font-bold text-primary font-serif">₹{typeof total === 'number' ? total.toFixed(2) : '0.00'}</span>
            </div>
          </div>
        </section>

        {/* Action Section */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link to="/" className="bg-primary hover:bg-primary-container text-white px-10 py-4 rounded-md font-medium transition-all duration-300 shadow-md hover:shadow-lg active:scale-95 w-full sm:w-auto font-label text-center">
            Back to Home
          </Link>
        </div>

        {/* Visual Decoration */}
        <div className="mt-16 relative h-40 overflow-hidden rounded-xl opacity-80 md:opacity-100">
          <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-transparent z-10"></div>
          <img alt="Spices" className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBoAsiKaf5qXoE1uNt1DlBGtAqol5REFobtExPDuDhvZjyoVPrhDVv8Mw_cRbGZm-9-zeGVZ1WBSb8Qu8qcPLMkfrE7mz8Ce49OF_Ops5NT0gt6cEMcMd4x7IQSlVPUEbb21kR2JvtPHH88uHT9pFx6RnWCcLKNBGYs6CZTaRgqLQnDZGa3CPqPw1dzwE-TFNdb8jBIr_Ss4d37kXjRnPw2ukz2_ufIWIsitsWXnuAB0VrXjNcJwLV_p4xxyAWiRstL4iy40-Gtmd7J" />
          <div className="absolute bottom-4 left-6 z-20">
            <p className="text-white font-serif italic text-xl drop-shadow-md">Handcrafted with passion.</p>
          </div>
        </div>
      </div>
    </main>
  );
}
