/**
 * SWEET — Medication Service
 * ================================================
 * Role: Encapsulates API calls related to medication data.
 *
 * Client used:
 * - apiClient (routes requiring authentication)
 *
 * Responsibility:
 * - Forward CRUD and action requests to the backend
 * - Contains no business logic
 * - Does not handle errors (handled in hooks)
 */


import { apiClient } from "../core/apiClient";


function createMedicationEntry(data) {
  return apiClient.post("data/medication", data);
}

function getMedicationEntries() {
  return apiClient.get("data/medication");
}

function updateMedicationEntry(entryId, data) {
  return apiClient.put(`data/medication/${entryId}`, data);
}

function deleteMedicationEntry(entryId) {
  return apiClient.delete(`data/medication/${entryId}`);
}

function takeMedicationDose(entryId) {
  return apiClient.patch(`data/medication/${entryId}/take`);
}

export const medicationService = {
  createMedicationEntry,
  getMedicationEntries,
  updateMedicationEntry,
  deleteMedicationEntry,
  takeMedicationDose,
};
