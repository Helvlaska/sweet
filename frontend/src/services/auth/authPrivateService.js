/**
 * SWEET — Auth Private Service
 * ================================================
 * Role: Encapsulates authenticated user account API calls.
 *
 * Client used:
 * - apiClient (routes requiring authentication)
 *
 * Responsibility:
 * - Handle profile, logout and password update
 * - Contains no business logic
 * - Does not handle errors (handled in hooks)
 */


import { apiClient } from "../core/apiClient";


function logout() {
  return apiClient.post("auth/logout");
}

function getProfile() {
  return apiClient.get("auth/profile");
}

function updateProfile(data) {
  return apiClient.put("auth/profile", data);
}

function updatePassword(data) {
  return apiClient.put("auth/password", data);
}

export const authPrivateService = {
  logout,
  getProfile,
  updateProfile,
  updatePassword,
};
