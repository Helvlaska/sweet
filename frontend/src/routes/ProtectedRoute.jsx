import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext"; // Hook global

export default function ProtectedRoute({ children }) {

  const { user, loading } = useAuth();
  // Vérifie si un user est connecté
  if (loading) {
    return <div className="loader">Vérification de la connexion...</div>;
  }
  // Vérifie si le profil du user est bien chargé
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return children;
}
