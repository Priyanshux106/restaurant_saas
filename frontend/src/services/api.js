import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getStoreStatus = async () => {
  try {
    const response = await api.get('/store/status/');
    return response.data;
  } catch (error) {
    console.error('Error fetching store status:', error);
    throw error;
  }
};

export const getMenu = async () => {
  try {
    const response = await api.get('/menu/');
    // Backend returns { categories: [{ id, name, items: [...] }] }
    // Frontend expects a flat array of items with a 'category' field (lowercase string)
    if (response.data && response.data.categories) {
      const flatItems = [];
      response.data.categories.forEach(category => {
        const catName = category.name.toLowerCase();
        if (category.items) {
          category.items.forEach(item => {
            flatItems.push({
              id: item.id,
              name: item.name,
              description: item.description,
              price: parseFloat(item.full_price),
              half_price: item.half_price ? parseFloat(item.half_price) : null,
              image: item.image,
              category: catName,
              tag: item.is_available ? 'star' : 'local_fire_department', // Or some logic
              is_available: item.is_available
            });
          });
        }
      });
      return flatItems;
    }
    return [];
  } catch (error) {
    console.error('Error fetching menu:', error);
    throw error;
  }
};

export const getCustomer = async (phone) => {
  try {
    const response = await api.get(`/customers/${phone}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const placeOrder = async (orderData) => {
  try {
    const response = await api.post('/orders/', orderData);
    return {
      success: true,
      order_id: response.data.order_id,
      total: response.data.total,
      payment_method: response.data.payment_method
    };
  } catch (error) {
    console.error('Error placing order:', error.response?.data || error.message);
    throw error;
  }
};

export const createPayment = async (orderId) => {
  try {
    const response = await api.post('/payments/create/', { order_id: orderId });
    return response.data;
  } catch (error) {
    console.error('Error creating payment:', error);
    throw error;
  }
};

export const verifyPayment = async (paymentData) => {
  try {
    const response = await api.post('/payments/verify/', paymentData);
    return response.data;
  } catch (error) {
    console.error('Error verifying payment:', error);
    throw error;
  }
};
