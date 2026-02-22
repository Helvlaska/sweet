/**
 * SWEET — Mood Service
 * ================================================
 * Role: Encapsulates API calls related to mood data.
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


function createMoodEntry(data) {
  return apiClient.post("data/mood", data);
}

function getMoodEntries(params) {
  return apiClient.get("data/mood", { params });
}

function updateMoodEntry(entryId, data) {
  return apiClient.put(`data/mood/${entryId}`, data);
}

function deleteMoodEntry(entryId) {
  return apiClient.delete(`data/mood/${entryId}`);
}

export const moodService = {
  createMoodEntry,
  getMoodEntries,
  updateMoodEntry,
  deleteMoodEntry,
};
