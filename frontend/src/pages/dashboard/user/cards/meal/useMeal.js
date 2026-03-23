import { useState, useEffect } from "react";
import { mealService } from "../../../../../services/health/mealService";


export function useMeal() {
  const [meals, setMeals] = useState([]);
  const [breakfast, setBreakfast] = useState("");
  const [lunch, setLunch] = useState("");
  const [dinner, setDinner] = useState("");
  const [snack, setSnack] =useState("");
  const [showPopup, setShowPopup] = useState(false);
  const [errors, setErrors] = useState([]);


  function handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    if (name === "breakfast") {
      setBreakfast(value);
    }

    if (name === "lunch") {
      setLunch(value);
    }

    if (name === "dinner") {
      setDinner(value);
    }

    if (name === "snack") {
      setSnack(value);
    }

    setErrors([]);
  }

  function validateRequiredFields() {
    const validationErrors = [];

    if (!breakfast && !lunch && !dinner && !snack) {
      validationErrors.push(
        "Renseigne au moins un repas."
      )
    }

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return false;
    }

    setErrors([]);
    return true;
  }



  function groupMealsByType(meals) {
    const groups = {};

    for (let i = 0; i < meals.length; i++) {
      const meal = meals[i];
      const type = meal.meal_type;

      if (!groups[type]) {
        groups[type] = [];
      }

      groups[type].push(meal.description);
    }

    return groups;
  }


  function openPopup() {
    setBreakfast("");
    setLunch("");
    setDinner("");
    setSnack("");
    setErrors([]);
    setShowPopup(true);
  }

  function closePopup() {
    setShowPopup(false);
    setErrors([]);
  }


  async function fetchMeals() {
    try {
      const params = { range_type: "day"};
      const response = await mealService.getMealEntries(params);
      const data = response.data || response;

      setMeals(data);

    } catch (error) {
      console.error("Erreur récupération repas:", error);
    }
  }


  function buildPayload(breakfast, lunch, dinner, snack) {
    const entries = [];

    if (breakfast) {
      entries.push({ meal_type: "breakfast", description: breakfast });
    }

    if (lunch) {
      entries.push({ meal_type: "lunch", description: lunch });
    }

    if (dinner) {
      entries.push({ meal_type: "dinner", description: dinner });
    }

    if (snack) {
      entries.push({ meal_type: "snack", description: snack });
    }

    return entries;
  }


  async function handleSubmit(event) {
    event.preventDefault();

    const isFormValid = validateRequiredFields();

    if (!isFormValid) {
      return;
    }

    try {
      const entries = buildPayload(breakfast, lunch, dinner, snack);

      for (let i = 0; i < entries.length; i++) {
        await mealService.createMealEntry({
          meal_type: entries[i].meal_type,
          description: entries[i].description,
        });
      }

      await fetchMeals();

      setBreakfast("");
      setLunch("");
      setDinner("");
      setSnack("");
      setShowPopup(false);

    } catch (error) {
      console.error("Erreur ajout repas :", error);
    }
  }

  useEffect(function() {
    fetchMeals();
  }, []);


  return {
    breakfast,
    lunch,
    dinner,
    snack,
    showPopup,
    errors,
    groupedMeals: groupMealsByType(meals),
    handleChange,
    openPopup,
    closePopup,
    handleSubmit
  }
}
