import { useState, useEffect } from "react";
import { activityService } from "../../../../../services/health/activityService";
import { validateField } from "../../../../../utils/validator";
import { formatData } from "../../../../../utils/dataFormatter";


export function useActivity() {

  const [description, setDescription] = useState("");
  const [duration, setDuration] = useState("");
  const [entries, setEntries] =useState([]);
  const [average, setAverage] = useState(null);
  const [period, setPeriod] = useState("week");
  const [showPopup, setShowPopup] = useState(false);
  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState([]);

  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    if (name === "description") {
      setDescription(value);
    }

    if (name === "duration") {
      setDuration(value);
    }

    setErrors([]);
  }


  function validateRequiredFields() {
    const validationErrors = [];

    if (!description) {
      validationErrors.push(
        "Choisis ton activité."
      );
    }

    if (duration === "" || duration === null || duration === undefined) {
      validationErrors.push(
        "Renseigne une durée en minute."
      );
    }

    if (description && duration && !validateField("activity", {description: description, duration: duration})) {
      validationErrors.push(
        "Les données de l'activité sont invalides."
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
    setDescription("");
    setDuration("");
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
      const response = await activityService.getActivityEntries(params);
      const data = response.data || response;

      setEntries(data);

    } catch (error) {
      console.error("Erreur récupération activité :", error);
    }
  }


  async function fetchAverage(range) {
    try {
      setLoading(true);

      const params = { range_type: range };
      const response = await activityService.getActivityStats(params);

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
      let data = {
        description: description,
        duration: duration,
      };
      data = await formatData("data", data);

      await activityService.createActivityEntry({
        description: data.description,
        duration: data.duration,
      });

      await fetchAverage(period);
      await fetchWeeklyEntries();

      setDescription("");
      setDuration("");
      setShowPopup(false);

    } catch (error) {
      console.error("Erreur ajout activité :", error);
    }
  }


  useEffect(function () {
    fetchWeeklyEntries();
  }, []);

  useEffect(function () {
    fetchAverage(period);
  }, [period]);


  return {
    description,
    duration,
    entries,
    average,
    period,
    loading,
    showPopup,
    errors,

    handleChange,
    openPopup,
    closePopup,
    setRange,
    handleSubmit,
  }
}
