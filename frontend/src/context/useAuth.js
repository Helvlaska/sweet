/**
 * SWEET — useAuth Hook
 * =================================================
 * Role: Provides access to the authentication context.
 *
 * Responsibilities:
 * - Allow components to access authentication state
 * - Expose user, login, logout and updateProfile
 *
 * Important:
 * - Must be used within <AuthProvider>.
 * - Contains no business logic.
 */


import { useContext } from "react";
import { AuthContext } from "./AuthContext";


export function useAuth() {
  return useContext(AuthContext);
}
