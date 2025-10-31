import React, { useState, useEffect } from "react";
import { mealService } from "../../services/mealService";

function MealCard() {
  const [meals, setMeals] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Champs du formulaire (un pour chaque type de repas)
  const [formData, setFormData] = useState({
    breakfast: "",
    lunch: "",
    dinner: "",
    snack: "",
  });

  // Charger les repas du jour
  useEffect(() => {
    async function fetchMeals() {
      try {
        const response = await mealService.get_meal_entries({ range_type: "day" });
        if (response.data && response.data.length > 0) {
          setMeals(response.data);
        }
      } catch (error) {
        console.error("Erreur lors du chargement des repas :", error);
      }
    }
    fetchMeals();
  }, []);

  // Gérer la saisie du formulaire
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  // Envoi vers l’API
  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const entries = Object.entries(formData).filter(([, desc]) => desc.trim() !== "");
      for (const [mealType, description] of entries) {
        await mealService.create_meal_entry({
          meal_type: mealType,
          description: description,
        });
      }

      // Recharge les repas après enregistrement
      const updated = await mealService.get_meal_entries({ range_type: "day" });
      setMeals(updated.data);

      // Réinitialisation
      setFormData({ breakfast: "", lunch: "", dinner: "", snack: "" });
      setIsModalOpen(false);
    } catch (error) {
      console.error("Erreur lors de l’enregistrement des repas :", error);
    }
  };

  return (
    <div className="meal-card">
      {/* --- En-tête de la carte --- */}
      <div className="meal-card-header">
        <h2>Repas</h2>
        <button onClick={() => setIsModalOpen(true)}>+</button>
      </div>

      <p>Aujourd’hui, j’ai mangé :</p>

      {/* --- Liste des repas enregistrés (groupés par type) --- */}
      <div className="meal-list">
      {meals.length > 0 ? (
        Object.entries(
          meals.reduce((acc, meal) => {
            if (!acc[meal.meal_type]) acc[meal.meal_type] = [];
            acc[meal.meal_type].push(meal.description);
            return acc;
          }, {})
        ).map(([type, descriptions], index) => (
          <div key={index} className="meal-item">
            <h4>
              {type === "breakfast"
                ? "Petit-déjeuner"
                : type === "lunch"
                ? "Déjeuner"
                : type === "dinner"
                ? "Dîner"
                : "Collation"}
            </h4>
            {descriptions.map((desc, i) => (
              <p key={i}>{desc}</p>
            ))}
          </div>
        ))
      ) : (
        <span className="meal-placeholder">Aucun repas enregistré</span>
      )}
    </div>


      {/* --- Pop-up modal --- */}
      {isModalOpen && (
        <div className="meal-modal">
          <div className="meal-modal-content">
            {/* Bouton de fermeture */}
            <button className="close-btn" onClick={() => setIsModalOpen(false)}>
              ✕
            </button>

            <div className="meal-modal-body">
              {/* Image mascotte */}
              <div className="meal-image">
                <img
                  src="/assets/meal_mascotte.png"
                  alt="Mascotte repas"
                  style={{ width: "150px" }}
                />
              </div>

              {/* Formulaire d’ajout */}
              <div className="meal-form">
                <h3>Qu’as-tu mangé aujourd’hui ?</h3>

                <form onSubmit={handleSubmit}>
                  <input
                    type="text"
                    name="breakfast"
                    placeholder="Petit-déjeuner"
                    value={formData.breakfast}
                    onChange={handleChange}
                  />
                  <input
                    type="text"
                    name="snack"
                    placeholder="Collation"
                    value={formData.snack}
                    onChange={handleChange}
                  />
                  <input
                    type="text"
                    name="lunch"
                    placeholder="Déjeuner"
                    value={formData.lunch}
                    onChange={handleChange}
                  />
                  <input
                    type="text"
                    name="dinner"
                    placeholder="Dîner"
                    value={formData.dinner}
                    onChange={handleChange}
                  />

                  <button type="submit">Confirmer</button>
                </form>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default MealCard;
