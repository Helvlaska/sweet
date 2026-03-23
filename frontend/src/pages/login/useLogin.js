/**
 * SWEET — useLogin Hook
 * ====================
 * Custom hook handling all business logic
 * related to the user login form.
 *
 * Role:
 * -----
 * - Centralize login form state management.
 * - Validate fields before submission.
 * - Build the authentication API payload.
 * - Trigger login via the AuthContext.
 * - Handle post-authentication navigation.
 *
 * Managed fields:
 * ---------------
 * - email / username (either one is required)
 * - password
 * - rememberMe ("remember me" option)
 * - showPassword (password visibility)
 * - errors (user-facing error messages)
 *
 * Validation:
 * -----------
 * - Ensures either email or username is provided.
 * - Validates formats using the validateField helper.
 * - Prevents form submission when errors are present.
 *
 * Navigation:
 * -----------
 * - Redirects to the user dashboard by default.
 * - Redirects to the admin area when the user role is "admin".
 * - Navigation logic is delegated to the useNavigation hook.
 *
 * Architecture:
 * -------------
 * - This hook contains no JSX.
 * - It is designed to be consumed by a form component (.jsx).
 * - API calls are delegated to the AuthContext.
 * - Validation rules are centralized in utils/validator.
 *
 * Maintenance:
 * ------------
 * - Any change to validation rules should be handled
 *   in the dedicated helpers.
 * - Any change to the authentication flow should remain
 *   confined to this hook.
 * - This hook does not handle rendering or styling.
 */


import { useState } from "react";
import { useAuth } from "../../context/useAuth";
import { validateField } from "../../utils/validator";
import { useNavigation } from "../../hooks/navigation/useNavigation";

export function useLogin() {
  const { login } = useAuth();
  const { goToDashboard, goToAdmin } = useNavigation();

  // States
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState([]);

  function togglePasswordVisibility() {
    setShowPassword(function (previousValue) {
      return !previousValue;
    });
  }

  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;
    const type = event.target.type;
    const checked = event.target.checked;

    if (type === "checkbox") {
      setRememberMe(checked);
      setErrors([]);
      return;
    }

    if (name === "email") {
      setEmail(value);
    }

    if (name === "username") {
      setUsername(value);
    }

    if (name === "password") {
      setPassword(value);
    }

    setErrors([]);
  }

  function validateForm() {
    const validationErrors = [];

    if (!email && !username) {
      validationErrors.push(
        "Renseigne l'email OU le nom d'utilisateur."
      );
    }

    if (email && !validateField("email", email)) {
      validationErrors.push("Adresse email invalide.");
    }

    if (username && !validateField("username", username)) {
      validationErrors.push("Nom d'utilisateur invalide.");
    }

    if (!password) {
      validationErrors.push("Le mot de passe est obligatoire.");
    }

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return false;
    }

    setErrors([]);
    return true;
  }


  function buildLoginPayload() {
    return {
      email: email || undefined,
      username: username || undefined,
      password: password,
      remember_me: rememberMe,
    };
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const isFormValid = validateForm();

    if (!isFormValid) {
      return;
    }

    const payload = buildLoginPayload();
    setErrors([]);

    try {
      const user = await login(payload);

      if (user && user.role === "admin") {
        goToAdmin();
      } else {
        goToDashboard();
      }
    } catch (error) {
      console.error("[useLogin] Login error:", error);
      setErrors(["Identifiants incorrects ou erreur serveur."]);
    }
  }


  return {
    email,
    username,
    password,
    rememberMe,
    showPassword,
    errors,

    handleChange,
    togglePasswordVisibility,
    handleSubmit,
  };
}
