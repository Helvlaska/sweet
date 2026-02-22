/**
 * SWEET — useRegisterAuth Hook
 * ============================
 * Custom hook handling the business logic
 * of the authentication step in the registration process.
 *
 * Role:
 * -----
 * - Manage the form state (email, username, password).
 * - Validate required fields.
 * - Enforce password security rules.
 * - Check email and username availability.
 * - Build the authentication payload.
 * - Pass validated data to the next step.
 *
 * Managed fields:
 * ---------------
 * - email
 * - username
 * - password
 * - passwordChecklist (password security rules state)
 * - showPassword (password visibility)
 * - errors (user-facing error messages)
 * - emailStatus (neutral | valid | unavailable)
 * - usernameStatus (neutral | valid | unavailable)
 *
 * Validation:
 * -----------
 * - Validates presence and format via validateField.
 * - Applies password security rules via checkPasswordRules.
 * - Performs asynchronous availability checks
 *   via authPublicService.checkAvailability.
 *
 * Behavior:
 * ---------
 * - handleChange:
 *     Updates state and triggers necessary validations.
 *
 * - buildAuthPayload:
 *     Executes all validations (local + asynchronous),
 *     then returns a payload ready to be passed to the parent flow.
 *
 * - handleNext(onNext):
 *     Triggers full validation,
 *     then passes validated data through the onNext callback.
 *
 * Architecture:
 * -------------
 * - This hook contains no JSX.
 * - It is consumed by RegisterAuth.jsx.
 * - Validation rules are centralized in utils/validator.
 * - Network calls are isolated in authPublicService.
 * - It integrates with the global flow orchestrated by useRegisterFlow.
 *
 * Maintenance:
 * ------------
 * - Any update to validation rules must remain
 *   within the dedicated helpers.
 * - Any change to availability behavior
 *   must stay aligned with the backend API.
 * - This hook does not handle rendering or styling.
 */


import { useState } from "react";
import { validateField, checkPasswordRules } from "../../../utils/validator";
import { authPublicService } from "../../../services/auth/authPublicService";


export function useRegisterAuth() {
  // States
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordChecklist, setPasswordChecklist] = useState(null);
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState([]);
  const [emailStatus, setEmailStatus] = useState("neutral");
  const [usernameStatus, setUsernameStatus] = useState("neutral");


  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    if (name === "email") {
      setEmail(value);
      setEmailStatus("neutral");

      if (validateField("email", value)) {
        checkEmailAvailability(value);
      }
    }

    if (name === "username") {
      setUsername(value);
      setUsernameStatus("neutral");

      if (validateField("username", value)) {
        checkUsernameAvailability(value);
      }
    }

    if (name === "password") {
      setPassword(value);
      setPasswordChecklist(checkPasswordRules(value));
    }

    setErrors([]);
  }

  function togglePasswordVisibility() {
    setShowPassword(function (previousValue) {
      return !previousValue;
    });
  }

  function validateRequiredFields() {
    const validationErrors = [];

    if (!email) {
      validationErrors.push(
        "Renseigne l'email."
      );
    }

    if (email && !validateField("email", email)) {
      validationErrors.push(
        "Adresse email invalide."
      );
    }

    if (!username) {
      validationErrors.push(
        "Renseigne le nom utilisateur."
      );
    }

    if (username && !validateField("username", username)) {
      validationErrors.push(
        "Nom d'utilisateur invalide."
      );
    }

    if (!password) {
      validationErrors.push(
        "Le mot de passe est obligatoire."
      );
    }

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return false;
    }

    setErrors([]);
    return true;
  }

  async function checkEmailAvailability(value) {
    try {
      const response = await authPublicService.checkAvailability({email: value});
      const data = response.data;

      if (data.email_available) {
        setEmailStatus("valid");
        return true;
      } else {
        setEmailStatus("unavailable");
        return false;
      }
    } catch (error) {
      console.error("Erreur lors de la vérification de disponibilité :", error);
      setEmailStatus("neutral");
      setErrors([
        "Une erreur est survenue lors de la vérification. Réessaie plus tard."
      ]);

      return false;
    }
  }

  async function checkUsernameAvailability(value) {
    try {
      const response = await authPublicService.checkAvailability({username: value});
      const data = response.data;

      if (data.username_available) {
        setUsernameStatus("valid");
        return true;
      } else {
        setUsernameStatus("unavailable");
        return false;
      }
    } catch (error) {
      console.error("Erreur lors de la vérification de disponibilité :", error);
      setUsernameStatus("neutral");
      setErrors([
        "Une erreur est survenue lors de la vérification. Réessaie plus tard."
      ]);

      return false;
    }
  }

  function validatePassword() {
    const validationErrors = [];

    if (!password) {
      validationErrors.push("Renseigne ton mot de passe.")
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

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return false;
    }

    setErrors([]);
    return true;
  }

  async function buildAuthPayload() {
    setErrors([]);

    if (!validateRequiredFields()) {
      return false;
    }

    if (emailStatus !== "valid") {
      const isEmailAvailable = await checkEmailAvailability(email);
      if (!isEmailAvailable) {
        return false;
      }
    }

    if (usernameStatus !== "valid") {
      const isUsernameAvailable = await checkUsernameAvailability(username);
      if (!isUsernameAvailable) {
        return false;
      }
    }

    const ispasswordValid = validatePassword();

    if (!ispasswordValid) {
      return false;
    }

    if (errors.length > 0) {
      return false;
    }

    return {
      email: email,
      username: username,
      password: password,
    };
  }

  async function handleNext(onNext) {
    const payload = await buildAuthPayload();

    if (!payload) {
      return;
    }

    onNext(payload);
  }

  return {
    email,
    username,
    password,
    passwordChecklist,
    showPassword,
    errors,
    emailStatus,
    usernameStatus,

    handleChange,
    togglePasswordVisibility,
    handleNext,
  }
}
