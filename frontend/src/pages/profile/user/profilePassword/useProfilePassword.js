import { useState } from "react";
import { useAuth } from "../../../../context/useAuth";
import { checkPasswordRules } from "../../../../utils/validator";


export function useProfilePassword() {
  const { updatePassword } = useAuth();

  //States
  const [password, setPassword] = useState("");
  const [passwordChecklist, setPasswordChecklist] = useState(checkPasswordRules(""));
  const [showPassword, setShowPassword] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [errors, setErrors] = useState([]);


  function editing() {
    setIsEditing(true);
  }

  function cancelEditing() {
    setPassword("");
    setPasswordChecklist(checkPasswordRules(""));
    setShowPassword(false);
    setErrors([]);
    setIsEditing(false);
  }


  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

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


  async function buildPasswordPayload() {
    setErrors([]);

    if (!validatePassword()) {
      return false;
    }

    if (errors.length > 0) {
      return false;
    }

    return {
      new_password: password
    };
  }


  async function handleSubmit() {
    const payload = await buildPasswordPayload();

    if (!payload) {
      return;
    }

    setErrors([]);

    try {
      await updatePassword(payload);
      setPassword("");
      setPasswordChecklist(checkPasswordRules(""));
      setShowPassword(false);
      setIsEditing(false);

    } catch (error) {
      console.error("Une erreur est survenue lors de la modification du mot de passe", error);
    }
  }


  return {
    password,
    passwordChecklist,
    showPassword,
    isEditing,
    errors,
    editing,
    cancelEditing,
    handleChange,
    togglePasswordVisibility,
    handleSubmit
  }
}
