import { api } from "./api"; // Permet de communiquer avec le backend

// Récupération des routes d'authentafication
const register = (data) => api.post("auth/register", data, {headers: {"Content-type": "application/json"}})
const check_email_username = (data) => api.post("auth/check-availability", data)
const login = (data) => api.post("auth/login", data, {headers: {"Content-Type": "application/json"}})
const logout = () => api.post("auth/logout")
const reset_request = (data) => api.post("auth/reset", data)
const reset_confirm = (token, data) => api.put(`auth/reset/${token}`, data)
const update_password = (data) => api.put("auth/password", data)
const show_profile = () => api.get("auth/profile")
const update_profile = (data) => api.put("auth/profile", data)

// Exportation des services
export const authService = {register, check_email_username, login, logout, reset_request, reset_confirm, update_password, show_profile, update_profile};
