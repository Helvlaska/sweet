import { createContext, useState, useContext, useEffect } from "react";
import { authService } from "../services/authService"; // on l'utilisera ensuite


const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await authService.profile();
        setUser(res.data);
        console.log("Profil utilisateur chargé :", res.data);
      } catch (err) {
        console.warn("Aucun utilisateur connecté :", err.message);
        setUser(null);
      }
    };

    fetchProfile();
  }, []);


  const login = (userData) => {
    setUser(userData);
  };


  const logout = async () => {
    try {
      await authService.logout();
      setUser(null);
    } catch (err) {
      console.error("Erreur de déconnexion :", err);
    }
  };


  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}


export function useAuth() {
  return useContext(AuthContext);
}
