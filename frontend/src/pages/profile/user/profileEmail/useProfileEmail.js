import { useState } from "react";
import { useAuth } from "../../../../context/useAuth";
import { validateField } from "../../../../utils/validator";
import { authPublicService } from "../../../../services/auth/authPublicService";


export function useProfileEmail() {
  const { user, updateProfile } = useAuth();

  const [email, setEmail] = useState(user.email || "");
  const [emailStatus, setEmailStatus] = useState("neutral");
  const [isEditing, setIsEditing] = useState(false);
  const [errors, setErrors] = useState([]);


  function editing() {
    setIsEditing(true);
  }

  function cancelEditing() {
    setEmail(user.email || "");
    setIsEditing(false);
  }

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

    setErrors([]);
  }

  function validateRequiredFields() {
    const validationErrors = [];

    if (!(email || user.email)) {
      validationErrors.push(
        "Renseigne l'email."
      );
    }

    if ((email || user.email) && !validateField("email", (email || user.email))) {
      validationErrors.push(
        "Adresse email invalide."
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

  async function buildPayload() {
    const data = {};
    let hasChange = false;
    setErrors([]);

    if (!validateRequiredFields()) {
      return false;
    }

    if (email && email !== user.email) {
      if (emailStatus !== "valid") {
        const isEmailAvailable = await checkEmailAvailability(email);
        if (!isEmailAvailable) {
          return false;
        }
      }
      data.email = email;
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
    email,
    errors,
    emailStatus,
    isEditing,
    editing,
    cancelEditing,
    handleChange,
    handleSubmit,
  }
}
