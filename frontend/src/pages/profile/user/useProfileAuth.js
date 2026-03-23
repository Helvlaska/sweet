import { useState } from "react";
import { useAuth } from "../../../context/useAuth";
import { validateField } from "../../../utils/validator";
import { authPublicService } from "../../../services/auth/authPublicService";


export function useProfileAuth() {
  const { user, updateProfile } = useAuth();
  const initialData = user;

  // States
  const [email, setEmail] = useState(initialData.email || "");
  const [username, setUsername] = useState(initialData.username || "");
  const [emailStatus, setEmailStatus] = useState("neutral");
  const [usernameStatus, setUsernameStatus] = useState("neutral");
  const [errors, setErrors] = useState([]);


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

    setErrors([]);
  }


  function validateRequiredFields() {
    const validationErrors = [];

    if (!(email || initialData.email)) {
      validationErrors.push(
        "Renseigne l'email."
      );
    }

    if ((email || initialData.email) && !validateField("email", (email || initialData.email))) {
      validationErrors.push(
        "Adresse email invalide."
      );
    }

    if (!(username || initialData.username)) {
      validationErrors.push(
        "Renseigne le nom utilisateur."
      );
    }

    if ((username || initialData.username) && !validateField("username", (username || initialData.username))) {
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


  async function buildAuthPayload() {
    const data = {};
    let hasChange = false;
    setErrors([]);

    if (!validateRequiredFields()) {
      return false;
    }

    if (email && email !== initialData.email) {
      if (emailStatus !== "valid") {
        const isEmailAvailable = await checkEmailAvailability(email);
        if (!isEmailAvailable) {
          return false;
        }
      }
      data.email = email;
      hasChange = true;
    }

    if (username && username !== initialData.username) {
      if (usernameStatus !== "valid") {
        const isUsernameAvailable = await checkUsernameAvailability(username);
        if (!isUsernameAvailable) {
          return false;
        }
      }
      data.username = username;
      hasChange = true;
    }

    if (errors.length > 0) {
      return false;
    }

    if (!hasChange) {
      return false;
    }

    return data;
  }


  async function handleSubmit() {
    const payload = await buildAuthPayload();

    if (!payload) {
      return;
    }

    setErrors([]);

    try {
      await updateProfile(payload);

    } catch (error) {
      console.error("Une erreur est survenue lors de la modification des identifiants de connexion", error);
    }
  }

  return {
    email,
    username,
    errors,
    emailStatus,
    usernameStatus,
    handleChange,
    handleSubmit,
  }
}
