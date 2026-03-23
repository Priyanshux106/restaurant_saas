import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';

export default function Navbar() {
  const { getCartCount } = useCart();
  const cartCount = getCartCount();

  return (
    <nav className="fixed top-0 w-full z-50 bg-[#f3fcf0]/80 dark:bg-stone-900/80 backdrop-blur-xl shadow-sm dark:shadow-none">
      <div className="flex justify-between items-center w-full px-6 py-4 max-w-screen-2xl mx-auto">
        <Link to="/" className="text-2xl font-serif font-bold text-[#b7102a] dark:text-[#db313f] tracking-tighter">
          Spice House
        </Link>
        <div className="flex items-center gap-4">
          <Link to="/cart" className="relative p-2 hover:bg-[#edf6ea]/50 dark:hover:bg-stone-800/50 transition-all rounded-full flex items-center justify-center">
            <span className="material-symbols-outlined text-[#161d16] dark:text-stone-100">shopping_bag</span>
            {cartCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-primary text-white text-[10px] font-bold w-5 h-5 flex items-center justify-center rounded-full shadow-lg border-2 border-background">
                {cartCount}
              </span>
            )}
          </Link>
          <button className="md:hidden p-2 text-[#161d16] dark:text-stone-100">
            <span className="material-symbols-outlined">menu</span>
          </button>
        </div>
      </div>
    </nav>
  );
}
