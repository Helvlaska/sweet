/**
 * SWEET — Forgot Password Service
 * ================================================
 * Role: Encapsulates password reset confirmation API calls.
 *
 * Client used:
 * - publicClient (public routes without session)
 *
 * Responsibility:
 * - Handle password reset request and confirmation
 * - Contains no business logic
 * - Does not handle errors (handled in hooks)
 */


import { publicClient } from "../core/publicClient";

function resetRequest(data) {
  return publicClient.post("auth/reset", data);
}

function resetConfirm(token, data) {
  return publicClient.put(`auth/reset/${token}`, data);
}

export const forgotPasswordService = {
  resetRequest,
  resetConfirm,
};
