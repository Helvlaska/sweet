/**
 * SWEET — useResetPassword Hook
 * ============================
 * Custom hook handling the business logic
 * of the user password reset process.
 *
 * Role:
 * -----
 * - Manage the state of the password reset form.
 * - Validate the security rules of the new password.
 * - Verify password confirmation.
 * - Build the API request payload.
 * - Trigger the password reset confirmation using a secure token.
 *
 * Managed fields:
 * ---------------
 * - password (new password)
 * - confirmPassword (confirmation)
 * - passwordChecklist (password security rules state)
 * - showPassword (password visibility)
 * - errors (user-facing error messages)
 * - success (confirmation message)
 *
 * Validation:
 * -----------
 * - Ensures both password fields are provided.
 * - Applies security rules via checkPasswordRules.
 * - Prevents submission when passwords do not match.
 *
 * API:
 * ----
 * - Password reset confirmation is delegated
 *   to the forgotPasswordService using a secure token.
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
 * - Any change to password security rules
 *   should be handled in the dedicated helpers.
 * - Any modification to the reset password flow
 *   should remain confined to this hook.
 * - This hook does not handle rendering or styling.
 */


import { useState } from "react";
import { checkPasswordRules } from "../../../utils/validator";
import { forgotPasswordService } from "../../../services/auth/forgotPasswordService";


export function useResetPassword(token) {
  const { resetConfirm } = forgotPasswordService;

  // States
  const [password, setPassword] = useState("");
  const [passwordChecklist, setPasswordChecklist] = useState(null);
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState([]);
  const [success, setSuccess] = useState("");


  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    if (name === "password") {
      setPassword(value);
      setPasswordChecklist(checkPasswordRules(value));
      setSuccess("");
    }

    if (name === "confirmPassword") {
      setConfirmPassword(value);
      setSuccess("");
    }

    setErrors([]);
  }

  function togglePasswordVisibility() {
    setShowPassword(function (previousValue) {
      return !previousValue;
    });
  }

  function validatePassword() {
    const validationErrors = [];

    if (!password) {
      validationErrors.push("Renseigne le nouveau mot de passe.")
    }

    if (!confirmPassword) {
      validationErrors.push("Confirme ton nouveau mot de passe.");
    }

    if (password) {
      const rules = checkPasswordRules(password);

      const isPasswordStrong =
        rules.hasMinLength &&
        rules.hasUppercase &&
        rules.hasLowercase &&
        rules.hasNumber &&
        rules.hasSpecialChar;

      if (!isPasswordStrong) {
        validationErrors.push(
          "Le mot de passe ne respecte pas les critères de sécurité."
        );
      }
    }

    if (password && confirmPassword && password !== confirmPassword) {
      validationErrors.push("Les mots de passe ne correspondent pas.")
    }

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return false;
    }

    setErrors([]);
    return true;
  }

  function buildPasswordPayload() {
    return {
      new_password: password,
    };
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const ispasswordValid = validatePassword();

    if (!ispasswordValid) {
      return;
    }

    const payload = buildPasswordPayload();
    setErrors([]);

    try {
      await resetConfirm(token, payload);

      setSuccess("Le mot de passe à bien été mit à jour.")
    } catch (error) {
      console.error("[useResetPassword] Error:", error);
      setErrors(["Une erreur est survenue."]);
    }
  }

  return {
    password,
    passwordChecklist,
    confirmPassword,
    showPassword,
    errors,
    success,

    togglePasswordVisibility,
    handleChange,
    handleSubmit,
  }
}
