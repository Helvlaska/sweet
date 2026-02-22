import React, { useState, useEffect } from "react";
import { mealService } from "../../services/health/mealService";

// imports des images et des icones
import MealLogo from "../../assets/dashboard/page/DashboardIllustrationRepas.png";
import PlusIcon from "../../assets/dashboard/page/DashboardIconPlus.png";
import PopUpImage from "../../assets/dashboard/page/DashboardPopUpIllustrationRepas.png";
import PopUpCrossClose from "../../assets/dashboard/page/DashboardPopUpIconQuitter.png";

function MealCard() {
    // Stockage des données
    const [meals, setMeals] = useState([]);

    // Gestion du pop-up
    const [showPopup, setShowPopup] = useState(false);

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
            setShowPopup(false);
        } catch (error) {
            console.error("Erreur lors de l’enregistrement des repas :", error);
        }
    };

    return (
        <div className="card card--meal">
            <header className="card__header">
                <div className="card__title">
                    <img src={MealLogo} alt="Icône Humeur" className="card__icon" />
                    <h2 className="card__heading">Repas</h2>
                </div>
                <button className="card__btn-add" onClick={() => setShowPopup(true)}>
                    <img src={PlusIcon} alt="Ajouter" />
                </button>
            </header>
            <div className="card__body">
                <p className="card__text">Aujourd’hui, j’ai mangé :</p>
                <div className="card__list">
                    {meals.length > 0 ? (
                        Object.entries(
                            meals.reduce((acc, meal) => {
                                if (!acc[meal.meal_type]) acc[meal.meal_type] = [];
                                acc[meal.meal_type].push(meal.description);
                                return acc;
                            }, {})
                        ).map(([type, descriptions], index) => (
                            <div key={index} className="card__list-card">
                                <h4 className="card__list-card--header">
                                    {type === "breakfast"
                                        ? "Petit-déjeuner:"
                                        : type === "lunch"
                                        ? "Déjeuner:"
                                        : type === "dinner"
                                        ? "Dîner:"
                                        : "Collation:"}
                                </h4>
                                {descriptions.map((desc, i) => (
                                    <p key={i} className="card__list-item">{" "}{desc},</p>
                                ))}
                            </div>
                        ))
                    ) : (
                        <span className="meal-placeholder">Aucun repas enregistré</span>
                    )}
                </div>
            </div>
            {showPopup && (
                <div className="popup">
                    <img src={PopUpImage} alt="Décor popup" className="popup__img" />
                    <div className="popup__overlay">
                        <button className="popup__close" onClick={() => setShowPopup(false)}>
                            <img src={PopUpCrossClose} alt="Fermer" />
                        </button>
                        <div className="popup__content">
                            <h3 className="popup__title">Qu’as-tu mangé aujourd’hui ?</h3>
                            <form className="popup__form" onSubmit={handleSubmit}>
                                <input
                                    className="popup__input"
                                    type="text"
                                    name="breakfast"
                                    placeholder="Petit-déjeuner"
                                    value={formData.breakfast}
                                    onChange={handleChange}
                                />
                                <input
                                    className="popup__input"
                                    type="text"
                                    name="snack"
                                    placeholder="Collation"
                                    value={formData.snack}
                                    onChange={handleChange}
                                />
                                <input
                                    className="popup__input"
                                    type="text"
                                    name="lunch"
                                    placeholder="Déjeuner"
                                    value={formData.lunch}
                                    onChange={handleChange}
                                />
                                <input
                                    className="popup__input"
                                    type="text"
                                    name="dinner"
                                    placeholder="Dîner"
                                    value={formData.dinner}
                                    onChange={handleChange}
                                />
                                <button type="submit" className="popup__btn-confirm">Ajouter</button>
                            </form>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default MealCard;
