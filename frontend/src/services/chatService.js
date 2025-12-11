import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const chatAPI = {
  sendMessage: async (payload) => {
    try {
      const response = await axiosInstance.post("/api/chat/", payload);
      return response.data;
    } catch (error) {
      if (error.response) {
        // Server responded with error status
        throw new Error(
          error.response.data?.detail ||
            `Server error: ${error.response.status}`
        );
      } else if (error.request) {
        // Request made but no response
        throw new Error(
          "No response from server. Make sure backend is running on port 8000."
        );
      } else {
        throw error;
      }
    }
  },

  addToCart: async (customerId, productData) => {
    try {
      const response = await axiosInstance.post("/api/cart/add", {
        customer_id: customerId,
        ...productData,
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || "Failed to add to cart");
    }
  },

  getCart: async (customerId) => {
    try {
      const response = await axiosInstance.get(`/api/cart/${customerId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || "Failed to fetch cart");
    }
  },

  createOrder: async (customerData) => {
    try {
      const response = await axiosInstance.post("/api/checkout/create-order", customerData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || "Failed to create order");
    }
  },
};

export default chatAPI;
