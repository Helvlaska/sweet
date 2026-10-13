import { useState } from "react";
import { useAuth } from "../../../../context/useAuth";
import { validateField } from "../../../../utils/validator";
import { formatData } from "../../../../utils/dataFormatter"


export function useProfileInfo() {
  const { user, updateProfile } = useAuth();

  // States
  const [firstName, setFirstName] = useState(user.first_name || "");
  const [lastName, setLastName] = useState(user.last_name || "");
  const [gender, setGender] = useState(user.gender || "");
  const [height, setHeight] = useState(user.height || "");
  const [city, setCity] = useState(user.city || "");
  const [dateOfBirth, setDateOfBirth] = useState(user.date_of_birth || "");
  const [profilePicture, setProfilePicture] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [errors, setErrors] = useState([]);


  function editing() {
    setIsEditing(true);
  }


  function cancelEditing() {
    setFirstName(user.first_name || "");
    setLastName(user.last_name || "");
    setGender(user.gender || "");
    setCity(user.city || "");
    setDateOfBirth(user.date_of_birth || "");
    setHeight(user.height || "");

    setIsEditing(false);
  }


  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    if (name ==="first_name") {
      setFirstName(value);
    }

    if (name ==="last_name") {
      setLastName(value);
    }

    if (name ==="gender") {
      setGender(value);
    }

    if (name ==="height") {
      setHeight(value);
    }

    if (name ==="city") {
      setCity(value);
    }

    if (name ==="date_of_birth") {
      setDateOfBirth(value);
    }

    setErrors([]);
  }


  function validateRequiredFields() {
    const validationErrors = [];

    if (!(firstName || user.first_name)) {
      validationErrors.push(
        "Renseigne ton prénom."
      );
    }

    if ((firstName || user.first_name) && !validateField("first_name", (firstName || user.first_name))) {
      validationErrors.push(
        "Prénom invalide."
      );
    }

    if (!(lastName || user.last_name)) {
      validationErrors.push(
        "Renseigne ton nom."
      );
    }

    if ((lastName || user.last_name) && !validateField("last_name", (lastName || user.last_name))) {
      validationErrors.push(
        "Nom invalide."
      );
    }

    if (!(gender || user.gender)) {
      validationErrors.push(
        "Renseigne ton genre."
      );
    }

    if ((gender || user.gender) && !validateField("gender", (gender || user.gender))) {
      validationErrors.push(
        "Genre invalide."
      );
    }

    if (!(height || user.height)) {
      validationErrors.push(
        "Renseigne ta taille."
      );
    }

    if ((height || user.height) && !validateField("height", (height || user.height))) {
      validationErrors.push(
        "Taille invalide."
      );
    }

    if (!(city || user.city)) {
      validationErrors.push(
        "Renseigne ta ville."
      );
    }

    if ((city || user.city) && !validateField("city", (city || user.city))) {
      validationErrors.push(
        "Ville invalide."
      );
    }

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return false;
    }

    setErrors([]);
    return true;
  }


  function handleFileChange(event) {
    const file = event.target.files[0];

    if (file) {
      setPreview(URL.createObjectURL(file));
      setProfilePicture(file);
    }
  }


  async function buildProfilePayload() {
    if (!validateRequiredFields()) {
      return false;
    }

    const data = {
      first_name: firstName || user.first_name,
      last_name: lastName || user.last_name,
      gender: gender || user.gender,
      height: height || user.height,
      city: city || user.city,
      date_of_birth: dateOfBirth || undefined,
      profile_picture: profilePicture || undefined,
    };

    const formattedData = await formatData("user", data);

    return formattedData;
  }


  async function handleSubmit() {
    const payload = await buildProfilePayload();

    if (!payload) {
      return;
    }

    setErrors([]);

    try {
      await updateProfile(payload);
      setPreview(null);
      setIsEditing(false);

    } catch (error) {
      console.error("Une erreur est survenue lors de la modification du profil user", error);
    }
  }

  return {
    firstName,
    lastName,
    gender,
    height,
    city,
    dateOfBirth,
    errors,
    preview,
    isEditing,
    editing,
    cancelEditing,
    handleChange,
    handleFileChange,
    handleSubmit,
  }
}
