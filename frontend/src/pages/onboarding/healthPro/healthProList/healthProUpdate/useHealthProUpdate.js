import { useState, useEffect } from "react";
import { validateField } from "../../../../../utils/validator";
import { formatData } from "../../../../../utils/dataFormatter";
import { healthProfessionalService } from "../../../../../services/professionals/healthProService";
import { documentService } from "../../../../../services/professionals/documentService";

export function useHealthProUpdate(fetchPros, selectedPro, setSelectedPro) {
  // States
  const [speciality, setSpeciality] = useState("");
  const [fullname, setFullname] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");
  const [postalCode, setPostalCode] = useState("");
  const [city, setCity] = useState("");
  const [files, setFiles] = useState([]);
  const [errors, setErrors] = useState([]);
  const [isOpenDocs, setIsOpenDocs] = useState(null);


  function initForm(selectedPro) {
    setErrors([]);

    setFullname(selectedPro.fullname);
    setSpeciality(selectedPro.speciality);
    setPhone(selectedPro.phone || "");
    setAddress(selectedPro.address || "");
    setPostalCode(selectedPro.postal_code || "");
    setCity(selectedPro.city || "");
    setEmail(selectedPro.email || "");
    setFiles([]);
   }

  function close() {
    setErrors([]);
    setSelectedPro(null);
    setFiles([]);
  }


  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    if (name === "speciality") {
      setSpeciality(value);
    }

    if (name === "fullname") {
      setFullname(value);
    }

    if (name === "phone") {
      setPhone(value);
    }

    if (name === "email") {
      setEmail(value);
    }

    if (name === "address") {
      setAddress(value);
    }

    if (name === "postalCode") {
      setPostalCode(value);
    }

    if (name === "city") {
      setCity(value);
    }

    setErrors([]);
  }

  function handleFileChange(event) {
    const selectedFiles = Array.from(event.target.files);
    setFiles(selectedFiles);
  }

  function validateRequiredFields() {
    const validationErrors = [];

    if (!speciality) {
      validationErrors.push(
        "Renseigne la spécialité de ton professionnel de santé."
      );
    }

    if (speciality && !validateField("speciality", speciality)) {
      validationErrors.push(
        "Spécialité invalide."
      );
    }

    if (!fullname) {
      validationErrors.push(
        "Renseigne le prénom et le nom de ton professionnel de santé."
      );
    }

    if (fullname && !validateField("fullname", fullname)) {
      validationErrors.push(
        "Prénom et Nom invalides."
      );
    }

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return false;
    }

    setErrors([]);
    return true;
  }


  function toggleDocs(proId) {
    if (isOpenDocs === proId) {
      setIsOpenDocs(null);
    } else {
      setIsOpenDocs(proId);
    }
  }

  function removeFiles(index) {
    const updatedFiles = [];

    for (let i = 0; i < files.length; i++) {
      if (i !== index) {
        updatedFiles.push(files[i]);
      }
    }

    setFiles(updatedFiles);
  }

  async function removeDoc(proId, documentId) {
    setErrors([]);

    try {
      await documentService.deleteDocument(proId, documentId);
      await fetchPros();
    } catch (error) {
      console.error(error);
      setErrors(["Erreur lors de la suppression du document."]);
    }
  }


  function buildPayload() {
    setErrors([]);

    if (!validateRequiredFields()) {
      return false;
    }

    return {
      fullname: fullname,
      speciality: speciality,
      phone: phone || undefined,
      email: email || undefined,
      address: address || undefined,
      postal_code: postalCode || undefined,
      city: city || undefined,
      documents: files,
    };
  }

  async function submit(event) {
    event.preventDefault();

    setErrors([]);

    if (!selectedPro) {
      return;
    }

    const payload = buildPayload();
    if (!payload) {
      return;
    }

    try {
      const formattedPayload = await formatData("professional", payload);
      await healthProfessionalService.updateHealthProfessional(selectedPro.id, formattedPayload);
      await fetchPros();

      setIsOpenDocs(null);
      close();
    } catch (error) {
      console.error(error);
      setErrors([
        "Erreur lors de la modification du professionnel de santé."
      ]);
    }
  }


  useEffect(function() {
    if (selectedPro) {
      initForm(selectedPro);
    }
  }, [selectedPro]);


  return {
    speciality,
    fullname,
    phone,
    email,
    address,
    postalCode,
    city,
    files,
    errors,
    isOpenDocs,

    close,
    handleChange,
    handleFileChange,
    toggleDocs,
    removeFiles,
    removeDoc,
    submit,
  }
}
