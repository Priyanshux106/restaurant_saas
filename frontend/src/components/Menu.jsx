import { useState, useEffect } from 'react';
import { getMenu, getStoreStatus } from '../services/api';
import { useCart } from '../context/CartContext';

export default function Menu() {
  const [items, setItems] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { addToCart } = useCart();
  const [toastMessage, setToastMessage] = useState('');

  const [isStoreOpen, setIsStoreOpen] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [menuData, statusData] = await Promise.all([
          getMenu(),
          getStoreStatus()
        ]);
        setItems(menuData);
        setIsStoreOpen(statusData.is_open);
      } catch (err) {
        setError('Failed to load menu. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleAddToCart = (item) => {
    addToCart(item);
    setToastMessage(`Added ${item.name} to cart`);
    setTimeout(() => setToastMessage(''), 3000);
  };

  const uniqueCategories = Array.from(new Set(items.map(item => item.category)));
  const categories = ['all', ...uniqueCategories];

  const filteredItems = filter === 'all' ? items : items.filter(item => item.category === filter);

  if (error) {
    return (
      <div className="py-24 text-center text-error block w-full px-6">
        <h2 className="text-2xl font-bold font-headline mb-4">Oops!</h2>
        <p>{error}</p>
        <button onClick={() => window.location.reload()} className="mt-6 px-6 py-2 bg-primary text-on-primary rounded font-bold hover:bg-primary-container transition-colors">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div id="menu" className="relative pb-24">
      {!isStoreOpen && (
        <div className="bg-error/10 border-b border-error/20 text-error px-6 py-3 text-center sticky top-16 z-50">
          <p className="font-headline font-bold text-sm">Our store is currently closed. You can view the menu, but ordering is temporarily disabled.</p>
        </div>
      )}

      {/* Category Filter */}
      <section className="px-6 py-8 max-w-screen-2xl mx-auto sticky top-28 z-40 bg-background/95 backdrop-blur-sm mt-12">
        <div className="flex flex-wrap items-center justify-center gap-3 md:gap-6">
          {categories.map(cat => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-8 py-2 rounded-full font-label text-sm font-bold label-tracking transition-all duration-300 ${
                filter === cat
                  ? 'glaze-gradient text-on-primary shadow-lg shadow-primary/20 active:scale-95'
                  : 'bg-surface-container-high text-on-surface-variant hover:bg-surface-container-highest'
              }`}
            >
              {cat === 'all' ? 'All' : cat === 'veg' ? 'Veg' : cat === 'non-veg' ? 'Non-Veg' : 'Drinks'}
            </button>
          ))}
        </div>
      </section>

      {/* Menu Grid / Loading State */}
      <section className="px-6 py-4 max-w-screen-2xl mx-auto min-h-[500px]">
        {loading ? (
          <div className="flex justify-center flex-col items-center h-64 gap-4 text-primary">
            <span className="material-symbols-outlined animate-spin text-4xl">autorenew</span>
            <p className="font-label font-bold label-tracking text-sm text-on-surface-variant">Gathering fresh spices...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-16">
            {filteredItems.map(item => (
              <article key={item.id} className="group relative flex flex-col">
                <div className="relative aspect-[4/5] overflow-hidden bg-surface-container-low rounded-lg transition-transform duration-500 group-hover:-translate-y-2">
                  <img
                    alt={item.name}
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                    src={item.image}
                  />
                  <div className="absolute top-4 right-4 bg-surface-container-lowest/90 px-3 py-1 rounded-full shadow-sm">
                    <span className="font-label text-xs font-bold text-primary">₹{item.price.toFixed(2)}</span>
                  </div>
                </div>
                
                <div className="mt-6 flex flex-col flex-grow">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-headline text-xl font-bold text-on-surface group-hover:text-primary transition-colors">
                      {item.name}
                    </h3>
                    <span className="material-symbols-outlined text-secondary text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>
                      {item.tag}
                    </span>
                  </div>
                  
                  <p className="text-on-surface-variant text-sm leading-relaxed mb-6 line-clamp-2">
                    {item.description}
                  </p>
                  
                  <button
                    onClick={() => handleAddToCart(item)}
                    disabled={!isStoreOpen || !item.is_available}
                    className="mt-auto w-full py-3 font-label text-xs font-bold label-tracking border border-outline-variant/30 hover:bg-primary hover:text-white hover:border-primary transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-on-surface disabled:hover:border-outline-variant/30"
                  >
                    {!isStoreOpen ? 'Store Closed' : (!item.is_available ? 'Out of Stock' : 'Add to Cart')}
                    {isStoreOpen && item.is_available && <span className="material-symbols-outlined text-sm">add</span>}
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>

      {/* Toast Mockup (Indicator Only) */}
      <div className={`fixed bottom-8 left-1/2 -translate-x-1/2 bg-inverse-surface text-inverse-on-surface px-6 py-3 rounded-full shadow-2xl flex items-center gap-3 transition-opacity duration-300 z-50 ${toastMessage ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>
        <span className="material-symbols-outlined text-primary-fixed" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
        <span className="font-label text-xs font-bold label-tracking">{toastMessage}</span>
      </div>
    </div>
  );
}
