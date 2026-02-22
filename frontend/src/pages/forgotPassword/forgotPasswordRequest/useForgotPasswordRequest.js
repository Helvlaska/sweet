/**
 * SWEET — useForgotPasswordRequest Hook
 * ====================================
 * Custom hook handling the business logic
 * for the password reset request flow.
 *
 * Role:
 * -----
 * - Manage the state of the password reset request form.
 * - Validate the email field before submission.
 * - Build the API request payload.
 * - Trigger the password reset request.
 *
 * Managed fields:
 * ---------------
 * - email
 * - errors (user-facing error messages)
 *
 * Validation:
 * -----------
 * - Ensures the email field is provided.
 * - Validates the format using the validateField helper.
 * - Prevents request submission when validation fails.
 *
 * API:
 * ----
 * - The password reset request is delegated
 *   to the forgotPasswordService.
 *
 * Architecture:
 * -------------
 * - This hook contains no JSX.
 * - It is designed to be consumed by a form component (.jsx).
 * - Validation rules are centralized in utils/validator.
 * - Network calls are isolated in service files.
 *
 * Maintenance:
 * ------------
 * - Any evolution of the reset flow should be handled
 *   within this hook or the related service.
 * - Error messages should remain user-oriented.
 * - This hook does not handle rendering or styling.
 */


import { useState } from "react";
import { validateField } from "../../../utils/validator";
import { forgotPasswordService } from "../../../services/auth/forgotPasswordService";


export function useForgotPasswordRequest() {
  const { resetRequest } = forgotPasswordService;

  // States
  const [email, setEmail] = useState("");
  const [errors, setErrors] = useState([]);
  const [success, setSuccess] = useState("");


  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    if (name === "email") {
      setEmail(value);
      setSuccess("");
    }

    setErrors([]);
  }

  function validateEmail() {
    const validationErrors = [];

    if (!email) {
      validationErrors.push("Renseigne l'email.")
    }

    if (email && !validateField("email", email)) {
      validationErrors.push("Adresse email invalide.");
    }

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return false;
    }

    setErrors([]);
    return true;
  }

  function buildEmailPayload() {
    return {
      email: email,
    };
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const isEmailValid = validateEmail();

    if (!isEmailValid) {
      return;
    }

    const payload = buildEmailPayload();
    setErrors([]);

    try {
      await resetRequest(payload);

      setSuccess("L'email de réinitialisation à bien été envoyé.")
    } catch (error) {
      console.error("[useForgotPasswordRequest] Error:", error);
      setErrors(["Vérifie ton email et réessaie."])
    }
  }

  return {
    email,
    errors,
    success,

    handleChange,
    handleSubmit,
  }
}
