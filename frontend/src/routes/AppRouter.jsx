import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "../context/useAuth";

// Composant de protection d'accès
import ProtectedRoute from "./ProtectedRoute";

// Pages publiques
import Landing from "../pages/landing/Landing";
import Login from "../pages/login/Login";
import ForgotPassword from "../pages/forgotPassword/forgotPasswordRequest/ForgotPasswordRequest";
import RegisterFlow from "../pages/register/RegisterFlow";

// Page sécurisées
import ResetPassword from "../pages/forgotPassword/resetPassword/ResetPassword";
import HealthPro from "../pages/onboarding/healthPro/HealthPro";
import AdminPage from "../pages/AdminPage";
import Dashboard from "../pages/dashboard/user/Dashboard";
import HealthProPage from "../pages/HealthProPage";
// import ForumPage from "../pages/ForumPage";
// import CalendarPage from "../pages/CalendarPage";
import ArticlePage from "../pages/ArticlePage";
import Profile from "../pages/profile/ProfileFlow";
import NotFound from "../pages/notFound/NotFound";


export default function AppRouter() {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="loader">Chargement...</div>;
  }

  return (
    <BrowserRouter>
      <Routes>
        {/* Routes publiques */}
        <Route path="/" element={
          user
            ? <Navigate to={user.role === "admin" ? "/admin" : "/dashboard"} replace />
            : <Landing />
        } />
        <Route path="/login" element={<Login />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/forgot-password/:token" element={<ResetPassword />} />
        <Route path="/register" element={<RegisterFlow />} />

        {/* Routes sécurisées */}
        <Route path="/onboarding" element={
          <ProtectedRoute>
            <HealthPro />
          </ProtectedRoute>
        }/>

        <Route path="/dashboard" element={
          <ProtectedRoute>
            {user?.role === "user" ? (
              <Dashboard />
            ) : (
              <Navigate to="/admin" replace />
            )}
          </ProtectedRoute>
        }/>

        <Route path="/admin" element={
          <ProtectedRoute>
            {user?.role === "admin" ? (
              <AdminPage />
            ) : (
              <Navigate to="/dashboard" replace />
            )}
          </ProtectedRoute>
        }/>

        <Route path="/professionals" element={
          <ProtectedRoute>
            <HealthProPage />
          </ProtectedRoute>
        } />

        {/*<Route path="/calendar" element={
          <ProtectedRoute>
            <CalendarPage />
          </ProtectedRoute>
        } />*/}

        {/*<Route path="/forum" element={
          <ProtectedRoute>
            <ForumPage />
          </ProtectedRoute>
        } />*/}

        <Route path="/blog" element={
          <ProtectedRoute>
            <ArticlePage />
          </ProtectedRoute>
        } />

        <Route path="/profile" element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        } />

        {/* Gestion routes inconnues */}
        <Route path="*" element={
          <ProtectedRoute>
            <NotFound />
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}
