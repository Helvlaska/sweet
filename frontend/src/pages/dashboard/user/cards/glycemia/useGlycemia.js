import { useState, useEffect } from "react";
import { glycemiaService } from "../../../../../services/health/glycemiaService";
import { validateField } from "../../../../../utils/validator";
import { formatData } from "../../../../../utils/dataFormatter";


export function useGlycemia() {

  const [entries, setEntries] = useState([]);
  const [average, setAverage] = useState(null);
  const [glycemia, setGlycemia] = useState("");
  const [period, setPeriod] = useState("week");
  const [showPopup, setShowPopup] = useState(false);
  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState([]);


  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    if (name === "glycemia") {
      setGlycemia(value);
    }

    setErrors([]);
  }


  function validateRequiredFields() {
    const validationErrors = [];

    if (!glycemia) {
      validationErrors.push(
        "Renseigne une valeur."
      );
    }

    if (glycemia && !validateField("glycemia", glycemia)) {
      validationErrors.push(
        "La valeur de glycémie est invalide."
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
    setGlycemia("");
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


  async function fetchWeeklyEntries() {
    try {
      const params = { range_type: "week" };
      const response = await glycemiaService.getGlycemiaEntries(params);
      const data = response.data || response;

      setEntries(data);

    } catch (error) {
      console.error("Erreur récupération glycémie :", error);
    }
  }


  async function fetchAverage(range) {
    try {
      setLoading(true);

      const params = { range_type: range };
      const response = await glycemiaService.getGlycemiaStats(params);

      let avg = null;

      if (response.data && response.data.average !== undefined) {
        avg = response.data.average;
      }

      setAverage(avg);

    } catch (error) {
      console.error("Erreur récupération moyenne :", error);
      setAverage(null);

    } finally {
      setLoading(false);
    }
  }


  async function handleSubmit(event) {
    event.preventDefault();

    const isFormValid = validateRequiredFields();

    if (!isFormValid) {
      return;
    }

    try {
      let data = {glycemia: glycemia};
      data = await formatData("data", data);

      await glycemiaService.createGlycemiaEntry({
        glucose_level: data.glycemia
      });

      await fetchAverage(period);
      await fetchWeeklyEntries();

      setGlycemia("");
      setShowPopup(false);

    } catch (error) {
      console.error("Erreur ajout glycémie :", error);
    }
  }


  useEffect(function () {
    fetchWeeklyEntries();
  }, []);


  useEffect(function () {
    fetchAverage(period);
  }, [period]);


  return {
    entries,
    average,
    period,
    loading,
    showPopup,
    glycemia,
    errors,
    
    handleChange,
    handleSubmit,
    openPopup,
    closePopup,
    setRange,
  };
}
