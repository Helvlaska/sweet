/**
 * SWEET — Weight Service
 * ================================================
 * Role: Encapsulates API calls related to weight data.
 *
 * Client used:
 * - apiClient (routes requiring authentication)
 *
 * Responsibility:
 * - Forward CRUD requests to the backend
 * - Contains no business logic
 * - Does not handle errors (handled in hooks)
 */


import { apiClient } from "../core/apiClient";


function createWeightEntry(data) {
  return apiClient.post("data/weight/", data);
}

function getWeightEntries(params) {
  return apiClient.get("data/weight", { params });
}

function getWeightStats(params) {
  return apiClient.get("data/weight/stats", { params });
}

function updateWeightEntry(entryId, data) {
  return apiClient.put(`data/weight/${entryId}`, data);
}

function deleteWeightEntry(entryId) {
  return apiClient.delete(`data/weight/${entryId}`);
}

export const weightService = {
  createWeightEntry,
  getWeightEntries,
  getWeightStats,
  updateWeightEntry,
  deleteWeightEntry,
};
