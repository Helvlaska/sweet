/**
 * SWEET — Note Service
 * ================================================
 * Role: Encapsulates API calls related to professional notes.
 *
 * Client used:
 * - apiClient (routes requiring authentication)
 *
 * Responsibility:
 * - Forward nested CRUD requests to the backend
 * - Contains no business logic
 * - Does not handle errors (handled in hooks)
 */


import { apiClient } from "../core/apiClient";


function createNote(professionalId, data) {
  return apiClient.post(
    `data/health_professionals/${professionalId}/notes`,
    data
  );
}

function getNotes(professionalId) {
  return apiClient.get(
    `data/health_professionals/${professionalId}/notes`
  );
}

function updateNote(professionalId, noteId, data) {
  return apiClient.put(
    `data/health_professionals/${professionalId}/notes/${noteId}`,
    data
  );
}

function deleteNote(professionalId, noteId) {
  return apiClient.delete(
    `data/health_professionals/${professionalId}/notes/${noteId}`
  );
}

export const noteService = {
  createNote,
  getNotes,
  updateNote,
  deleteNote,
};
