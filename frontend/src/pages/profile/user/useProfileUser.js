import { useState } from "react";
import { useAuth } from "../../../context/useAuth";
import { validateField } from "../../../utils/validator";
import { formatData } from "../../../utils/dataFormatter"


export function useProfileUser() {
  const { user, updateProfile } = useAuth();
  const initialData = user;

  // States
  const [firstName, setFirstName] = useState(initialData.first_name || "");
  const [lastName, setLastName] = useState(initialData.last_name || "");
  const [gender, setGender] = useState(initialData.gender || "");
  const [height, setHeight] = useState(initialData.height || "");
  const [city, setCity] = useState(initialData.city || "");
  const [dateOfBirth, setDateOfBirth] = useState(initialData.date_of_birth || "");
  const [profilePicture, setProfilePicture] = useState(null);
  const [preview, setPreview] = useState(null);
  const [errors, setErrors] = useState([]);


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

    if (!(firstName || initialData.first_name)) {
      validationErrors.push(
        "Renseigne ton prénom."
      );
    }

    if ((firstName || initialData.first_name) && !validateField("first_name", (firstName || initialData.first_name))) {
      validationErrors.push(
        "Prénom invalide."
      );
    }

    if (!(lastName || initialData.last_name)) {
      validationErrors.push(
        "Renseigne ton nom."
      );
    }

    if ((lastName || initialData.last_name) && !validateField("last_name", (lastName || initialData.last_name))) {
      validationErrors.push(
        "Nom invalide."
      );
    }

    if (!(gender || initialData.gender)) {
      validationErrors.push(
        "Renseigne ton genre."
      );
    }

    if ((gender || initialData.gender) && !validateField("gender", (gender || initialData.gender))) {
      validationErrors.push(
        "Genre invalide."
      );
    }

    if (!(height || initialData.height)) {
      validationErrors.push(
        "Renseigne ta taille."
      );
    }

    if ((height || initialData.height) && !validateField("height", (height || initialData.height))) {
      validationErrors.push(
        "Taille invalide."
      );
    }

    if (!(city || initialData.city)) {
      validationErrors.push(
        "Renseigne ta ville."
      );
    }

    if ((city || initialData.city) && !validateField("city", (city || initialData.city))) {
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
      first_name: firstName || initialData.first_name,
      last_name: lastName || initialData.last_name,
      gender: gender || initialData.gender,
      height: height || initialData.height,
      city: city || initialData.city,
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
    handleChange,
    handleFileChange,
    handleSubmit,
  }
}
