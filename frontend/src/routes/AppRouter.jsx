import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

// Composant de protection d'accès
import ProtectedRoute from "./ProtectedRoute";

// Pages publiques
import LandingPage from "../pages/LandingPage";
import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";

// Page sécurisées
import AdminPage from "../pages/AdminPage";
import DashboardPage from "../pages/DashboardPage";
import HealthProPage from "../pages/HealthProPage";
// import ForumPage from "../pages/ForumPage";
// import CalendarPage from "../pages/CalendarPage";
import ArticlePage from "../pages/ArticlePage";
import ProfilePage from "../pages/ProfilePage";
import NotFoundPage from "../pages/NotFoundPage";

export default function AppRouter() {
    const { user } = useAuth();

    return (
        <BrowserRouter>
        <Routes>
            {/* Routes publiques */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* Routes sécurisées */}
            <Route path="/dashboard" element={
                <ProtectedRoute>
                    {user?.role === "user" ? (
                        <DashboardPage />
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
                    <ProfilePage />
                </ProtectedRoute>
            } />

            {/* Gestion routes inconnues */}
            <Route path="*" element={
                <ProtectedRoute>
                    <NotFoundPage />
                </ProtectedRoute>
            } />
        </Routes>
        </BrowserRouter>
    );
}
