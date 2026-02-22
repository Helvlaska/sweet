/**
 * SWEET — Meal Service
 * ================================================
 * Role: Encapsulates API calls related to meal data.
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


function createMealEntry(data) {
  return apiClient.post("data/meal", data);
}

function getMealEntries(params) {
  return apiClient.get("data/meal", { params });
}

function updateMealEntry(entryId, data) {
  return apiClient.put(`data/meal/${entryId}`, data);
}

function deleteMealEntry(entryId) {
  return apiClient.delete(`data/meal/${entryId}`);
}

export const mealService = {
  createMealEntry,
  getMealEntries,
  updateMealEntry,
  deleteMealEntry,
};
