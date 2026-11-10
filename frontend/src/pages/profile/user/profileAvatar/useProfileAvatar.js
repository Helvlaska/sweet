import { useState, useRef } from "react";


export function useProfileAvatar() {
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

  return {
    profilePicture,
    preview,
    errors,
    isLoading,
    successMessage,
    inputRef,
    openFilePicker,
  }
}
