import { useState } from "react";
import { useAuth } from "../../../../context/useAuth";
import { validateField } from "../../../../utils/validator";
import { authPublicService } from "../../../../services/auth/authPublicService";


export function useProfileUsername() {
  const { user, updateProfile } = useAuth();

  const [username, setUsername] = useState(user.username || "");
  const [usernameStatus, setUsernameStatus] = useState("neutral");
  const [isEditing, setIsEditing] = useState(false);
  const [errors, setErrors] = useState([]);


  function editing() {
    setIsEditing(true);
  }

  function cancelEditing() {
    setUsername(user.username || "");
    setIsEditing(false);
  }

  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    if (name === "username") {
      setUsername(value);
      setUsernameStatus("neutral");

      if (validateField("username", value)) {
        checkUsernameAvailability(value);
      }
    }

    setErrors([]);
  }

  function validateRequiredFields() {
    const validationErrors = [];

    if (!(username || user.username)) {
      validationErrors.push(
        "Renseigne le nom utilisateur."
      );
    }

    if ((username || user.username) && !validateField("username", (username || user.username))) {
      validationErrors.push(
        "Nom d'utilisateur invalide."
      );
    }

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return false;
    }

    setErrors([]);
    return true;
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

  async function buildPayload() {
    const data = {};
    let hasChange = false;
    setErrors([]);

    if (!validateRequiredFields()) {
      return false;
    }

    if (username && username !== user.username) {
      if (usernameStatus !== "valid") {
        const isUsernameAvailable = await checkUsernameAvailability(username);
        if (!isUsernameAvailable) {
          return false;
        }
      }
      data.username = username;
      hasChange = true;
    }

    if (!hasChange) {
      return false;
    }

    return data;
  }

  async function handleSubmit() {
    const payload = await buildPayload();

    if (!payload) {
      return;
    }

    setErrors([]);

    try {
      await updateProfile(payload);
      setIsEditing(false);

    } catch (error) {
      console.error("Une erreur est survenue lors de la modification des identifiants de connexion", error);
    }
  }

  return {
    username,
    errors,
    usernameStatus,
    isEditing,
    editing,
    cancelEditing,
    handleChange,
    handleSubmit,
  }
}
