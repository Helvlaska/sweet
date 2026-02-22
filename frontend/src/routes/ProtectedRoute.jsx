/**
 * SWEET — Protected Route Component
 * =================================================
 * Role: Restricts access to authenticated users only.
 *
 * Responsibilities:
 * - Check authentication state
 * - Display a loading state while authentication is being verified
 * - Redirect unauthenticated users to the login page
 * - Render protected content for authenticated users
 *
 * Important:
 * - Relies on AuthContext for user and loading state.
 * - Does not contain business logic.
 */


import { Navigate } from "react-router-dom";
import { useAuth } from "../context/useAuth";


export default function ProtectedRoute({ children }) {

  const { user, loading } = useAuth();

  if (loading) {
    return <div className="loader">Vérification de la connexion...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
