import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

// Composant de protection (auth obligatoire)
import ProtectedRoute from "./ProtectedRoute";

// Tes pages React (tu pourras les créer plus tard)
import LandingPage from "../pages/LandingPage";
import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";
import DashboardPage from "../pages/DashboardPage";

// (optionnel) une page NotFound pour les mauvaises routes
// import NotFoundPage from "../pages/NotFoundPage";

export default function AppRouter() {
  return (
    /**
     * BrowserRouter :
     *  - supervise tout le système de navigation (URLs)
     *  - rend possible les <Link>, <Navigate>, <Route>...
     */
    <BrowserRouter>
      <Routes>
        {/* Routes publiques */}
        <Route path="/" element={<LandingPage />} />
        {/* Page de connexion */}
        <Route path="/login" element={<LoginPage />} />

        {/* Page d'inscription */}
        <Route path="/register" element={<RegisterPage />} />

        {/* ------------------------------
            🔒 Routes protégées (auth requise)
           ------------------------------ */}

        {/* Page principale du Dashboard */}
        <Route path="/dashboard" element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          } />

        {/* Exemple : une autre page protégée plus tard
        <Route
          path="/notes"
          element={
            <ProtectedRoute>
              <NotesPage />
            </ProtectedRoute>
          }
        /> */}

        {/* ------------------------------
            🚦 Gestion des routes inconnues
           ------------------------------ */}
        {/* Redirige toute URL inconnue vers /login */}
        {/*<Route path="*" element={<Navigate to="/login" />} />*/}
      </Routes>
    </BrowserRouter>
  );
}
