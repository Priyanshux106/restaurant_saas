import { Link } from 'react-router-dom';

export default function Hero() {
  return (
    <section className="relative min-h-[870px] flex items-center overflow-hidden bg-surface py-24">
        {/* Background Tonal Shift Layer */}
        <div className="absolute inset-0 bg-surface-container-low opacity-40 -z-10"></div>
        <div className="max-w-7xl mx-auto px-8 grid grid-cols-1 md:grid-cols-12 gap-12 items-center">
            {/* Content Column */}
            <div className="md:col-span-6 z-10">
                <div className="space-y-8">
                    <div className="inline-flex items-center gap-2 bg-tertiary-container/10 px-4 py-1.5 rounded-full">
                        <span className="w-2 h-2 rounded-full bg-tertiary"></span>
                        <span className="text-tertiary font-label text-sm font-medium uppercase tracking-wider">Now Open for Delivery</span>
                    </div>
                    <h1 className="text-5xl md:text-7xl font-bold leading-tight text-on-surface tracking-tight font-headline">
                        Delicious food, <span className="text-primary italic">delivered fast</span>
                    </h1>
                    <p className="text-on-surface-variant text-lg md:text-xl max-w-lg leading-relaxed font-body">
                        Experience the authentic heat of carefully sourced spices blended into every masterpiece. From our kitchen to your door, culinary excellence is just a tap away.
                    </p>
                    <div className="flex flex-wrap gap-4 pt-4">
                        <Link to="/#menu" className="bg-primary text-on-primary px-8 py-4 rounded-md text-lg font-semibold hover:bg-primary-container transition-all duration-300 active:scale-95 shadow-md flex items-center gap-2">
                            Order Now
                            <span className="material-symbols-outlined text-xl">arrow_forward</span>
                        </Link>
                    </div>
                    
                    {/* Trust Metrics */}
                    <div className="pt-12 grid grid-cols-2 gap-8 border-t border-outline-variant/10">
                        <div>
                            <p className="text-3xl font-bold text-secondary italic">15 min</p>
                            <p className="text-sm text-on-surface-variant font-label uppercase tracking-widest mt-1">Average Delivery</p>
                        </div>
                        <div>
                            <p className="text-3xl font-bold text-secondary italic">4.9/5</p>
                            <p className="text-sm text-on-surface-variant font-label uppercase tracking-widest mt-1">User Rating</p>
                        </div>
                    </div>
                </div>
            </div>
            
            {/* Imagery Column: Asymmetric Editorial Layout */}
            <div className="md:col-span-6 relative h-[500px] md:h-[650px] mt-12 md:mt-0">
                {/* Main Image with Bleed */}
                <div className="absolute inset-0 rounded-xl overflow-hidden shadow-2xl transform md:translate-x-12 translate-y-6">
                    <img alt="Gourmet Platter" className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDX91vd2KZHmwRDHy5IOJs0f-OclxdNr-3WfbYHg9y_flP_QrUE_v580Exc9dTcutxUi8c-ZSoiYFyL0G4K9EfswbL3ZndtfyJt4nnyg-SchTBHoC4jf8Vy4A6i0Z6t_mlZfaZ8VouT9VF-rkoJFSYIgk7RW8CzrK9WpRk96P2ZCfBQR7ZdHak0IHZOek7gHzdTEJclhIXZKXjZ4AlszHeDzwxXyPsYf5Q4dUhfelqHjGG8hL1ay0qpWNypHKztb3WY-QhDBORCZnVZ"/>
                </div>
                {/* Floating Accent Card */}
                <div className="absolute -bottom-10 -left-10 md:left-0 bg-surface-container-lowest/90 backdrop-blur-xl p-6 rounded-xl shadow-lg border border-outline-variant/10 max-w-[240px] hidden md:block">
                    <div className="flex items-center gap-4 mb-3">
                        <div className="w-12 h-12 rounded-full bg-secondary-container flex items-center justify-center">
                            <span className="material-symbols-outlined text-on-secondary-container">local_fire_department</span>
                        </div>
                        <p className="font-bold text-on-surface leading-tight font-headline">Chef's Special Recommendation</p>
                    </div>
                    <p className="text-sm text-on-surface-variant leading-snug">The Smoked Paprika Chicken with saffron-infused basmati.</p>
                </div>
                {/* Visual Accent Circle */}
                <div className="absolute -top-12 -right-12 w-64 h-64 rounded-full bg-primary-fixed-dim/20 blur-3xl -z-10"></div>
            </div>
        </div>
    </section>
  );
}
