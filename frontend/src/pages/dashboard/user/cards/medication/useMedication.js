import { useState, useEffect } from "react";
import { medicationService } from "../../../../../services/health/medicationService";


export function useMedication() {

  const [medications, setMedications] = useState([]);
  const [medicationOptions, setMedicationOptions] = useState([]);
  const [lowStock, setLowStock] = useState(null);
  const [selectedMed, setSelectedMed] = useState("");
  const [showPopup, setShowPopup] = useState(false);
  const [errors, setErrors] = useState([]);


  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    if (name === "description") {
      setSelectedMed(value);
    }

    setErrors([]);
  }


  function validateRequiredFields() {
    const validationErrors = [];

    if (!selectedMed) {
      validationErrors.push(
        "Choisis un médicament."
      );
    }

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return false;
    }

    setErrors([]);
    return true;
  }


  function openPopup() {
    setSelectedMed("");
    setErrors([]);
    setShowPopup(true);
  }

  function closePopup() {
    setShowPopup(false);
    setErrors([]);
  }


  function checkLowStock(meds) {
    let low = null;

    for (let i = 0; i < meds.length; i++) {
      if (meds[i].stock < meds[i].alert_threshold) {
        low = meds[i];
        break;
      }
    }

    setLowStock(low);
  }


  async function fetchMedications() {
    try {
      const response = await medicationService.getMedicationEntries();
      const meds = response.data || [];

      setMedications(meds);
      setMedicationOptions(buildMedicationOptions(meds));
      checkLowStock(meds);

    } catch (error) {
      console.error("Erreur récupération médicaments :", error);
    }
  }

  function buildMedicationOptions(meds) {
    const options = [];

    for (let i = 0; i < meds.length; i++) {
      options.push({
        value: meds[i].id,
        label: meds[i].name,
      });
    }

    return options;
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const isFormValid = validateRequiredFields();

    if (!isFormValid) {
      return;
    }

    try {
      await medicationService.takeMedicationDose(selectedMed);

      const response = await medicationService.getMedicationEntries();
      const meds = response.data || [];

      setMedications(meds);
      setMedicationOptions(buildMedicationOptions(meds));
      checkLowStock(meds);

      setSelectedMed("");
      setShowPopup(false);

    } catch (error) {
      console.error("Erreur prise de dose :", error);
    }
  }


  useEffect(function () {
    fetchMedications();
  }, []);


  return {
    medications,
    medicationOptions,
    lowStock,
    selectedMed,
    showPopup,
    errors,
    handleChange,
    openPopup,
    closePopup,
    handleSubmit,
  };
}
