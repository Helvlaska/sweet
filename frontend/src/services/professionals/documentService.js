/**
 * SWEET — Document Service
 * ================================================
 * Role: Encapsulates API calls related to professional documents.
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


function createDocument(professionalId, data) {
  return apiClient.post(
    `data/health_professionals/${professionalId}/documents`, data
  );
}

function getDocuments(professionalId) {
  return apiClient.get(
    `data/health_professionals/${professionalId}/documents`
  );
}

function updateDocument(professionalId, documentId, data) {
  return apiClient.put(
    `data/health_professionals/${professionalId}/documents/${documentId}`,
    data
  );
}

function deleteDocument(professionalId, documentId) {
  return apiClient.delete(
    `data/health_professionals/${professionalId}/documents/${documentId}`
  );
}

export const documentService = {
  createDocument,
  getDocuments,
  updateDocument,
  deleteDocument,
}
