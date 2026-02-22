/**
 * SWEET — Article Service
 * ================================================
 * Role: Encapsulates API calls related to articles.
 *
 * Client used:
 * - apiClient (routes requiring authentication)
 *
 * Responsibility:
 * - Forward CRUD and interaction requests to the backend
 * - Contains no business logic
 * - Does not handle errors (handled in hooks)
 */


import { apiClient } from "../core/apiClient";


function createArticle(data) {
  return apiClient.post("article", data);
}

function getArticles() {
  return apiClient.get("article");
}

function getArticle(id) {
  return apiClient.get(`article/${id}`);
}

function updateArticle(id, data) {
  return apiClient.put(`article/${id}`, data);
}

function deleteArticle(id) {
  return apiClient.delete(`article/${id}`);
}

function toggleLike(articleId) {
  return apiClient.post(`article/${articleId}/like`);
}

export const articleService = {
  createArticle,
  getArticles,
  getArticle,
  updateArticle,
  deleteArticle,
  toggleLike,
};
