/**
 * SWEET — Health Professional Service
 * ================================================
 * Role: Encapsulates API calls related to health professionals.
 *
 * Client used:
 * - apiClient (routes requiring authentication)
 *
 * Responsibility:
 * - Forward CRUD and nested resource requests to the backend
 * - Contains no business logic
 * - Does not handle errors (handled in hooks)
 */


import { apiClient } from "../core/apiClient";


function createHealthProfessional(data) {
  return apiClient.post("data/health_professionals/", data);
}

function getHealthProfessionals(params) {
  return apiClient.get("data/health_professionals", { params });
}

function getHealthProfessionalWithDetails(id) {
  return apiClient.get(`data/health_professionals/${id}`);
}

function updateHealthProfessional(id, data) {
  return apiClient.put(`data/health_professionals/${id}`, data);
}

function deleteHealthProfessional(id) {
  return apiClient.delete(`data/health_professionals/${id}`);
}

export const healthProfessionalService = {
  createHealthProfessional,
  getHealthProfessionals,
  getHealthProfessionalWithDetails,
  updateHealthProfessional,
  deleteHealthProfessional,
};
