/**
 * SWEET — API Client
 * ================================================
 * Role: Encapsulates authenticated HTTP communication with the backend.
 *
 * Client used:
 * - apiClient (routes requiring authentication)
 *
 * Responsibility:
 * - Manage authenticated requests via cookies
 * - Handle automatic token refresh
 * - Does not contain business logic
 */


import axios from "axios";


export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
});

apiClient.interceptors.response.use(

  function (response) {
    return response;
  },

  async function (error) {
    if (!error.response) {
      return Promise.reject(error);
    }

    var originalRequest = error.config;

    var isAuthRoute = false;

    if (originalRequest.url.includes("/auth/login")) {
      isAuthRoute = true;
    }

    if (originalRequest.url.includes("/auth/register")) {
      isAuthRoute = true;
    }

    if (originalRequest.url.includes("/auth/reset")) {
      isAuthRoute = true;
    }

    if (originalRequest.url.includes("/auth/refresh")) {
      isAuthRoute = true;
    }

    if (
      error.response.status === 401 &&
      originalRequest._retry !== true &&
      isAuthRoute === false
    ) {
      originalRequest._retry = true;

      try {
        await apiClient.post("/auth/refresh");
        return apiClient(originalRequest);
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

