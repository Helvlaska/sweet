import React, { useState, useEffect } from "react";
import { moodService } from "../../services/health/moodService";

// imports des images et des icones
import MoodLogo from "../../assets/dashboard/page/DashboardIllustrationHumeur.png";
import PlusIcon from "../../assets/dashboard/page/DashboardIconPlus.png";
import PopUpImage from "../../assets/dashboard/page/DashboardPopUpIllustrationHumeur.png";
import PopUpCrossClose from "../../assets/dashboard/page/DashboardPopUpIconQuitter.png";

function MoodCard() {
    // Stockage des données
    const [moods, setMoods] = useState([]);
    const [selectedMood, setSelectedMood] = useState("");

    // Gestion du pop-up
    const [showPopup, setShowPopup] = useState(false);

    const moodOptions = [
        "Joyeux",
        "Calme",
        "Motivé",
        "Fatigué",
        "Anxieux",
        "Irritable",
        "Déprimé",
        "Neutre",
    ];

    // Charger les humeurs du jour
    useEffect(() => {
        async function fetchMood() {
        try {
            const response = await moodService.get_mood_entries({ range_type: "day" });
            if (response.data && response.data.length > 0) {
                setMoods(response.data);
            }
        } catch (error) {
            console.error("Erreur lors du chargement des humeurs :", error);
        }
        }
        fetchMood();
    }, []);

    // Créer une nouvelle humeur
    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!selectedMood) return;

        try {
            const response = await moodService.create_mood_entry({
                description: selectedMood,
            });
            if (response.data) {
                setMoods([...moods, response.data]);
            }
            setSelectedMood("");
            setShowPopup(false);
        } catch (error) {
            console.error("Erreur lors de l’enregistrement de l’humeur :", error);
        }
    };

    return (
        <div className="card card--mood">
            <header className="card__header">
                <div className="card__title">
                    <img src={MoodLogo} alt="Icône Humeur" className="card__icon" />
                    <h2 className="card__heading">Humeur</h2>
                </div>
                <button className="card__btn-add" onClick={() => setShowPopup(true)}>
                    <img src={PlusIcon} alt="Ajouter" />
                </button>
            </header>
            <div className="card__body">
                <p className="card__text">Ton humeur aujourd’hui :</p>
                <div className="card__list">
                    {moods.length > 0 ? (
                        moods.map((mood, index) => (
                            <span key={index} className="card__list-tag">
                                {mood.description}
                            </span>
                        ))
                    ) : (
                        <span className="mood-placeholder">Aucune humeur enregistrée</span>
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
                            <h3 className="popup__title">Comment t’es-tu senti pendant ta journée ?</h3>
                            <form className="popup__form" onSubmit={handleSubmit}>
                                <select value={selectedMood} onChange={(e) => setSelectedMood(e.target.value)} className="popup__select">
                                    <option value="">Choisir une humeur...</option>
                                    {moodOptions.map((mood, index) => (
                                        <option key={index} value={mood}>
                                            {mood}
                                        </option>
                                    ))}
                                </select>
                                <button type="submit" className="popup__btn-confirm">Confirmer</button>
                            </form>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default MoodCard;
