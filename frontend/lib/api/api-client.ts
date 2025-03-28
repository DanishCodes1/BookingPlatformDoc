import axios from 'axios';

// Base URLs for each service
const API_URLS = {
    user: process.env.NEXT_PUBLIC_USER_SERVICE_URL || '/api/users',
    event: process.env.NEXT_PUBLIC_EVENT_SERVICE_URL || '/api/events',
    booking: process.env.NEXT_PUBLIC_BOOKING_SERVICE_URL || '/api/bookings',
    notification: process.env.NEXT_PUBLIC_NOTIFICATION_SERVICE_URL || '/api/notifications',
  };

// Create axios instances for each service
export const userApi = axios.create({
    baseURL: API_URLS.user,
    headers: {
        'Content-Type': 'application/json'
    }
});

export const eventApi = axios.create({
    baseURL: API_URLS.event,
    headers: {
        'Content-Type': 'application/json'
    }
});

export const bookingApi = axios.create({
    baseURL: API_URLS.booking,
    headers: {
        'Content-Type': 'application/json'
    }
});

export const notificationApi = axios.create({
    baseURL: API_URLS.notification,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Add a request interceptor to include the token in the headers
[userApi, eventApi, bookingApi, notificationApi].forEach(api => {
    api.interceptors.request.use(
        (config) => {
            const token = localStorage.getItem('token');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    );
});