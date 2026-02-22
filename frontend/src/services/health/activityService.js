/**
 * SWEET — Activity Service
 * ================================================
 * Role: Encapsulates API calls related to activity data.
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


function createActivityEntry(data) {
  return apiClient.post("data/activity", data);
}

function getActivityEntries(params) {
  return apiClient.get("data/activity", { params });
}

function getActivityStats(params) {
  return apiClient.get("data/activity/stats", { params });
}

function updateActivityEntry(entryId, data) {
  return apiClient.put(`data/activity/${entryId}}`, data);
}

function deleteActivityEntry(entryId) {
  return apiClient.delete(`data/activity/${entryId}`);
}

export const activityService = {
  createActivityEntry,
  getActivityEntries,
  getActivityStats,
  updateActivityEntry,
  deleteActivityEntry,
};
