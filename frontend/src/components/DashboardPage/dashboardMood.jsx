import React, { useState, useEffect } from "react";
import { moodService } from "../../services/moodService";

function MoodCard() {
  const [moods, setMoods] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedMood, setSelectedMood] = useState("");

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
      setIsModalOpen(false);
    } catch (error) {
      console.error("Erreur lors de l’enregistrement de l’humeur :", error);
    }
  };

  return (
    <div className="mood-card">
      <div className="mood-card-header">
        <h2>Humeur</h2>
        <button onClick={() => setIsModalOpen(true)}>+</button>
      </div>

      <p>Ton humeur aujourd’hui :</p>
      <div className="mood-list">
        {moods.length > 0 ? (
          moods.map((mood, index) => (
            <span key={index} className="mood-tag">
              {mood.description}
            </span>
          ))
        ) : (
          <span className="mood-placeholder">Aucune humeur enregistrée</span>
        )}
      </div>
      {isModalOpen && (
        <div className="mood-modal">
          <div className="mood-modal-content">
            <button className="close-btn" onClick={() => setIsModalOpen(false)}>
              ✕
            </button>

            <div className="mood-modal-body">
              {/* Image / Mascotte */}
              {/*<div className="mood-image">
                <img
                  src="/assets/mood_mascotte.png"
                  alt="Mascotte humeur"
                  style={{ width: "150px" }}
                />
              </div>*/}

              {/* Formulaire */}
              <div className="mood-form">
                <h3>Comment t’es-tu senti pendant ta journée ?</h3>

                <form onSubmit={handleSubmit}>
                  <select
                    value={selectedMood}
                    onChange={(e) => setSelectedMood(e.target.value)}
                  >
                    <option value="">Choisir une humeur...</option>
                    {moodOptions.map((mood, index) => (
                      <option key={index} value={mood}>
                        {mood}
                      </option>
                    ))}
                  </select>

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

export default MoodCard;
