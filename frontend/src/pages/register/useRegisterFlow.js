/**
 * SWEET — useRegisterFlow Hook
 * ===========================
 * Custom hook orchestrating the entire multi-step
 * registration process.
 *
 * Role:
 * -----
 * - Manage progression between register flow steps.
 * - Centralize data collected at each step.
 * - Merge authentication and profile payloads.
 * - Trigger final registration via the API.
 * - Automatically log the user in after registration.
 * - Redirect to onboarding at the end of the process.
 *
 * Managed steps:
 * --------------
 * - Step 0: Introduction
 * - Step 1: Welcome
 * - Step 2: Authentication (email / password)
 * - Step 3: User profile
 *
 * Internal state:
 * ---------------
 * - currentPage (active step index)
 * - authPayload (data collected during the Auth step)
 * - errors (global flow error messages)
 * - isLoading (final submission state)
 *
 * Flow logic:
 * -----------
 * - onAuthReady(payload):
 *     Stores authentication data and moves to the next step.
 *
 * - onProfileReady(profilePayload):
 *     Ensures authentication data exists,
 *     then triggers final submission.
 *
 * - submitRegistration(authData, profileData):
 *     Merges data,
 *     calls the registration service,
 *     logs the user in,
 *     redirects to "/onboarding".
 *
 * Navigation:
 * -----------
 * - Internal progression is handled via currentPage.
 * - Final redirection uses useNavigate.
 *
 * Architecture:
 * -------------
 * - This hook contains no JSX.
 * - API calls are delegated to authPublicService.
 * - Post-registration authentication uses AuthContext.
 * - It is designed to be consumed by RegisterFlow.jsx.
 *
 * Maintenance:
 * ------------
 * - Any change to the number or order of steps
 *   must be synchronized with RegisterFlow.
 * - Business rules of the flow must remain centralized here.
 * - This hook does not handle rendering or styling.
 */


import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authPublicService } from "../../services/auth/authPublicService";
import { useAuth } from "../../context/useAuth";


export function useRegisterFlow() {
  // States
  const [currentPage, setCurrentPage] = useState(0);
  const [authPayload, setAuthPayload] = useState(null);
  const [errors, setErrors] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();
  const { login } = useAuth();

  function goNext() {
    setCurrentPage(function (previousPage) {
      return previousPage + 1;
    });
  }

  function goBack() {
    setCurrentPage(function (previousPage) {
      return previousPage - 1;
    });
  }

  function skipPage() {
    goNext();
  }


  function onAuthReady(payload) {
    setAuthPayload(payload);
    goNext();
  }

  function onProfileReady(profilePayload) {
    if (!authPayload) {
      setErrors(["Erreur interne : données d'authentification manquantes.",]);
      return;
    }

    submitRegistration(authPayload, profilePayload);
  }

  async function submitRegistration(authData, profileData) {
    if (!authData || !profileData) {
      setErrors([
        "Les informations d'inscription sont incomplètes.",
      ]);
      return;
    }

    const finalPayload = {
      ...authData,
      ...profileData,
    };

    setIsLoading(true);
    setErrors([]);

    try {
      await authPublicService.register(finalPayload);
      await login({
        email: authData.email,
        password: authData.password,
      });

      navigate("/onboarding");
    } catch (error) {
      console.error(error);
      setErrors([
        "Une erreur est survenue lors de l'inscription. Réessaie plus tard.",
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  return {
    currentPage,
    errors,
    isLoading,

    goNext,
    goBack,
    skipPage,

    onAuthReady,
    onProfileReady,
  };
}
