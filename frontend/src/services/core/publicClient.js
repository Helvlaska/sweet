/**
 * SWEET — Public Client
 * ================================================
 * Role: Encapsulates public HTTP communication with the backend.
 *
 * Client used:
 * - publicClient (public routes without session)
 *
 * Responsibility:
 * - Send unauthenticated requests
 * - Does not handle token refresh
 * - Does not contain business logic
 */


import axios from "axios";

export const publicClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
});
