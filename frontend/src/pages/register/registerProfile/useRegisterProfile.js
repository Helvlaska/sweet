/**
 * SWEET — useRegisterProfile Hook
 * ===============================
 * Custom hook handling the business logic
 * of the profile step in the registration process.
 *
 * Role:
 * -----
 * - Manage the profile form state.
 * - Validate required profile fields.
 * - Handle profile picture upload and preview.
 * - Build and format the profile payload.
 * - Pass validated data to the next step.
 *
 * Managed fields:
 * ---------------
 * - firstName
 * - lastName
 * - gender
 * - height
 * - city
 * - dateOfBirth
 * - profilePicture
 * - preview (temporary image URL)
 * - errors (user-facing error messages)
 *
 * Validation:
 * -----------
 * - Validates required fields via validateField.
 * - Ensures all mandatory fields are correctly formatted.
 * - Blocks progression if validation fails.
 *
 * Behavior:
 * ---------
 * - handleChange:
 *     Updates profile state and clears errors.
 *
 * - handleFileChange:
 *     Stores the selected file and generates
 *     a temporary preview URL for UI rendering.
 *
 * - buildProfilePayload:
 *     Executes validation and formats data
 *     using formatData("user", data).
 *
 * - handleNext(onNext):
 *     Triggers validation,
 *     then passes formatted data through the onNext callback.
 *
 * Architecture:
 * -------------
 * - This hook contains no JSX.
 * - It is consumed by RegisterProfile.jsx.
 * - Validation rules are centralized in utils/validator.
 * - Data transformation is handled by utils/dataFormatter.
 * - It integrates with the global flow orchestrated by useRegisterFlow.
 *
 * Maintenance:
 * ------------
 * - Any update to validation rules must remain
 *   within the dedicated helpers.
 * - Any change to data formatting must stay
 *   aligned with backend expectations.
 * - This hook does not handle rendering or styling.
 */


import { useState } from "react";
import { validateField } from "../../../utils/validator";
import { formatData } from "../../../utils/dataFormatter"


export function useRegisterProfile() {
  // States
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [gender, setGender] = useState("");
  const [height, setHeight] = useState("");
  const [city, setCity] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState("");
  const [profilePicture, setProfilePicture] = useState(null);
  const [errors, setErrors] = useState([]);
  const [preview, setPreview] = useState(null);



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

    if (!firstName) {
      validationErrors.push(
        "Renseigne ton prénom."
      );
    }

    if (firstName && !validateField("first_name", firstName)) {
      validationErrors.push(
        "Prénom invalide."
      );
    }

    if (!lastName) {
      validationErrors.push(
        "Renseigne ton nom."
      );
    }

    if (lastName && !validateField("last_name", lastName)) {
      validationErrors.push(
        "Nom invalide."
      );
    }

    if (!gender) {
      validationErrors.push(
        "Renseigne ton genre."
      );
    }

    if (gender && !validateField("gender", gender)) {
      validationErrors.push(
        "Genre invalide."
      );
    }

    if (!height) {
      validationErrors.push(
        "Renseigne ta taille."
      );
    }

    if (height && !validateField("height", height)) {
      validationErrors.push(
        "Taille invalide."
      );
    }

    if (!city) {
      validationErrors.push(
        "Renseigne ta ville."
      );
    }

    if (city && !validateField("city", city)) {
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
      first_name: firstName,
      last_name: lastName,
      gender: gender,
      height: height,
      city: city,
      date_of_birth: dateOfBirth || undefined,
      profile_picture: profilePicture || undefined,
    };

    const formattedData = await formatData("user", data);

    return formattedData;
  }


  async function handleNext(onNext) {
    const payload = await buildProfilePayload();

    if (!payload) {
      return;
    }

    onNext(payload);
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
    handleNext,
  }
}
