import axios from "axios";

// Création d'une instance Axios commune à toute l'application
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,   // URL du backend Flask
  withCredentials: true,                        // ✅ Envoie et reçoit les cookies JWT
});


// Si une requête renvoie un 401 → cela signifie que le token est expiré ou invalide
// On redirige automatiquement vers la page de login
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Si token expiré (401) et qu'on n'a pas déjà essayé de refresh
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        console.warn("[API] Access token expiré, tentative de refresh...");
        await api.post("/auth/refresh");               // 🔄 Appel au backend pour régénérer le cookie
        console.info("[API] Nouveau token généré, relance de la requête initiale");
        return api(originalRequest);                   // Relance la requête initiale
      } catch (refreshError) {
        console.warn("[API] Refresh token invalide, redirection vers /login");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

