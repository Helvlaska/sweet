import { useState, useEffect } from "react";
import { moodService } from "../../../../../services/health/moodService";
import { validateField } from "../../../../../utils/validator";
import { formatData } from "../../../../../utils/dataFormatter";


export function useMood() {
  const [entries, setEntries] = useState([]);
  const [mood, setMood] = useState("");
  const [showPopup, setShowPopup] = useState(false);
  const [errors, setErrors] = useState([]);

  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    if (name === "mood") {
      setMood(value);
    }

    setErrors([]);
  }


  function validateRequiredFields() {
    const validationErrors = [];

    if (!mood) {
      validationErrors.push(
        "Renseigne ton humeur."
      );
    }

    if (mood && !validateField("mood", mood)) {
      validationErrors.push(
        "L'humeur est invalide."
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
    setMood("");
    setErrors([]);
    setShowPopup(true);
  }

  function closePopup() {
    setShowPopup(false);
    setErrors([]);
  }


  async function fetchMood() {
    try {
      const response = await moodService.getMoodEntries({ range_type: "day"});

      if (response.data && response.data.length > 0) {
        setEntries(response.data);
      }
      
    } catch (error) {
      console.error("Erreur chargement humeur:", error);
    }
  }


  async function handleSubmit(event) {
    event.preventDefault();

    const isFormValid = validateRequiredFields();

    if (!isFormValid) {
      return;
    }

    try {
      let data = {mood: mood};
      data = await formatData("data", data);

      await moodService.createMoodEntry({description: data.mood});
      await fetchMood();

      setMood("");
      setShowPopup(false);

    } catch (error) {
      console.error("Erreur ajout humeur:", error);
    }
  }


  useEffect(function() {
    fetchMood();
  }, []);


  return {
    entries,
    mood,
    showPopup,
    errors,
    handleChange,
    openPopup,
    closePopup,
    handleSubmit,
  }
}
