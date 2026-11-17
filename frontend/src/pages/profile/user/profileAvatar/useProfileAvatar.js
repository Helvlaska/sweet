import { useState, useRef } from "react";
import { useAuth } from "../../../../context/useAuth";
import { validateField } from "../../../../utils/validator";
import { formatData } from "../../../../utils/dataFormatter";


export function useProfileAvatar() {
  const { updateProfile } = useAuth();

  // States
  const [profilePicture, setProfilePicture] = useState(null);
  const [preview, setPreview] = useState(null);
  const [errors, setErrors] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  //Ref
  const inputRef = useRef(null);


  function openFilePicker() {
    inputRef.current.click();
  }

  function handleFileChange(event) {
    const file = event.target.files[0];
    const validationErrors = [];

    if (!file) {
      return;
    }

    if (!validateField("profile_picture", file)) {
      validationErrors.push(
        "Format accepté : JPEG ou PNG, 2 Mo maximum."
      );
      setErrors(validationErrors);
      return;

    } else {
      setErrors([]);
      URL.revokeObjectURL(preview);
      setPreview(URL.createObjectURL(file));
      setProfilePicture(file);
    }
  }

  async function handleFileSubmit() {
    if (!profilePicture) {
      return;
    }
    setIsLoading(true);

    const data = {profile_picture: profilePicture};

    setErrors([]);

    try {
      const formattedData = await formatData("user", data);

      if (!formattedData) { return; }
      await updateProfile(formattedData);
      URL.revokeObjectURL(preview);
      setPreview(null);
      setProfilePicture(null);
      setSuccessMessage("La nouvelle photo de profil a bien été ajoutée.");
    } catch (error) {
      // TODO : bloc 3 / tâche 2.8
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  function cancelPreview() {
    URL.revokeObjectURL(preview);
    setPreview(null);
    setProfilePicture(null);
    setErrors([]);
  }

  return {
    profilePicture,
    preview,
    errors,
    isLoading,
    successMessage,
    inputRef,
    openFilePicker,
    handleFileChange,
    handleFileSubmit,
    cancelPreview,
  }
}
