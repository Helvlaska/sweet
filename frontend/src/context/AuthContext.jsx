import { createContext, useState, useContext, useEffect } from "react";
import { authService } from "../services/authService";  // Appel des services pour utiliser les routes du backend


const AuthContext = createContext(null);    // Création du contexte du User
export {AuthContext};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Récupération du user connecté
    const fetchProfile = async () => {
      try {
        const res = await authService.show_profile();               // Appelle /auth/profile
        setUser(res.data);                                          // Stocke les données du user
        console.log("Utilisateur connecté :", res.data);
      } catch (err) {
        // Aucun user connecté ou cookie expiré
        console.warn("Aucun utilisateur trouvé :", err.message);
        setUser(null);
      } finally {
        // Indique que la vérification est terminée
        setLoading(false);
      }
    };

    const publicPaths = ["/", "/login", "/register"];
    const currentPath = window.location.pathname;

    if (!publicPaths.includes(currentPath)) {
        fetchProfile();
    } else {
        setLoading(false);
    }
  }, []);


  // Connection du user
  const login = async (credentials) => {
    try {
      const res = await authService.login(credentials);         // Appel /auth/login
      console.log("Connexion réussie :", res.data);

      const profileRes = await authService.show_profile();      // Récupération du profil du user
      setUser(profileRes.data);
      return profileRes.data;                                   // Renvoie des infos du user
    } catch (err) {
      console.error("Erreur de connexion :", err);
      throw err; // on relance pour que le composant puisse gérer l’erreur
    }
  };

  // Déconnexion du user
  const logout = async () => {
    try {
      await authService.logout();                       // Appel /auth/logout
      setUser(null);
      console.log("Utilisateur déconnecté");
    } catch (err) {
      console.error("Erreur lors du logout :", err);
    }
  };

  // Mise à jour du profile du user
  const updateProfile = async (updatedData) => {
    try {
      const res = await authService.update_profile(updatedData);    // Appel /auth/profile
      setUser(res.data);                                            // Mise à jour de l’état local du user
      console.log("Profil mis à jour :", res.data);
    } catch (err) {
      console.error("Erreur de mise à jour du profil :", err);
    }
  };

  // Retourne les infos du user connecté à toute l'application
  return (
    <AuthContext.Provider
      value={{ user, login, logout, updateProfile, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Hook personnalisé pour que tout les composants puissent utiliser l'authentification
// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  return useContext(AuthContext);
}
