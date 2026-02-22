/**
 * SWEET — Auth Public Service
 * ================================================
 * Role: Encapsulates public authentication API calls.
 *
 * Client used:
 * - publicClient (public routes without session)
 *
 * Responsibility:
 * - Handle login, register and password reset requests
 * - Contains no business logic
 * - Does not handle errors (handled in hooks)
 */


import { publicClient } from "../core/publicClient";


function register(data) {
  return publicClient.post("auth/register", data);
}

function checkAvailability(data) {
  return publicClient.post("auth/check-availability", data);
}

function login(data) {
  return publicClient.post("auth/login", data);
}

function requestPasswordReset(data) {
  return publicClient.post("auth/reset", data);
}

export const authPublicService = {
  register,
  checkAvailability,
  login,
  requestPasswordReset,
};
