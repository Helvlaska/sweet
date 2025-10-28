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
  (error) => {
    if (error.response && error.response.status === 401) {
      console.warn("[API] Session expirée, redirection vers /login");
      // Redirection immédiate (rafraîchit la page pour effacer le contexte utilisateur)
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
