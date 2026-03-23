/**
 * SWEET — Glycemia Service
 * ================================================
 * Role: Encapsulates API calls related to glycemia data.
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


function createGlycemiaEntry(data) {
  return apiClient.post("data/glycemia/", data);
}

function getGlycemiaEntries(params) {
  return apiClient.get("data/glycemia", { params });
}

function getGlycemiaStats(params) {
  return apiClient.get("data/glycemia/stats", { params });
}

function updateGlycemiaEntry(entryId, data) {
  return apiClient.put(`data/glycemia/${entryId}`, data);
}

function deleteGlycemiaEntry(entryId) {
  return apiClient.delete(`data/glycemia/${entryId}`);
}

export const glycemiaService = {
  createGlycemiaEntry,
  getGlycemiaEntries,
  getGlycemiaStats,
  updateGlycemiaEntry,
  deleteGlycemiaEntry,
};
