import { useState, useEffect } from "react";
import { weightService } from "../../../../../services/health/weightService";
import { validateField } from "../../../../../utils/validator";
import { formatData } from "../../../../../utils/dataFormatter";


export function useWeight() {

  const [intPart, setIntPart] = useState("");
  const [decPart, setDecPart] = useState("");
  const [entries, setEntries] = useState([]);
  const [period, setPeriod] = useState("week");
  const [showPopup, setShowPopup] = useState(false);
  const [errors, setErrors] = useState([]);


  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    if (name === "intPart") {
      setIntPart(value);
    }

    if (name === "decPart") {
      setDecPart(value);
    }

    setErrors([]);
  }


  function validateRequiredFields() {
    const validationErrors = [];

    if (!intPart) {
      validationErrors.push(
        "Renseigne ton poids."
      );
    }

    let fullValue = null;

    if (intPart) {
      const kilos = parseFloat(intPart);
      const grams = parseFloat(decPart || 0);
      fullValue = parseFloat(
        (kilos + grams / 100).toFixed(2)
      );
    }

    if (fullValue !== null && !validateField("weight", fullValue)) {
      validationErrors.push(
        "La valeur du poids est invalide."
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
    setIntPart("");
    setDecPart("");
    setErrors([]);
    setShowPopup(true);
  }


  function closePopup() {
    setShowPopup(false);
    setErrors([]);
  }


  function setRange(range) {
    setPeriod(range);
  }


  async function fetchWeightEntries(range) {
    try {
      const params = { range_type: range };
      const response = await weightService.getWeightEntries(params);
      const data = response.data || response;

      setEntries(data);

    } catch (error) {
      console.error("Erreur récupération poids :", error);
    }
  }


  async function handleSubmit(event) {
    event.preventDefault();

    const isFormValid = validateRequiredFields();

    if (!isFormValid) {
      return;
    }

    try {
      const kilos = parseFloat(intPart);
      const grams = parseFloat(decPart || 0);
      let fullValue = kilos + (grams / 100);
      fullValue = parseFloat(fullValue.toFixed(2));
      let data = {mass: fullValue};

      data = await formatData("data", data);
      await weightService.createWeightEntry(data);
      await fetchWeightEntries();

      setIntPart("");
      setDecPart("");
      setShowPopup(false);

    } catch (error) {

      console.error("Erreur ajout poids :", error);
    }
  }


  useEffect(function () {
    fetchWeightEntries(period);
  }, [period]);


  return {
    intPart,
    decPart,
    entries,
    period,
    showPopup,
    errors,
    handleChange,
    openPopup,
    closePopup,
    setRange,
    handleSubmit
  };
}
