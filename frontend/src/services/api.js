import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,   // URL de base du backend
  withCredentials: true,                        // Envoyer et recevoir les cookies JWT
});
