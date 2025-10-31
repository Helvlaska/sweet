import React, { useState, useEffect, useRef } from "react";
import { activityService } from "../../services/activityService"
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

function ActivityCard() {

  const [average, setAverage] = useState(null);          // Moyenne actuelle
  const [rangeType, setRangeType] = useState("week");    // Période choisie ("week", "month", etc.)
  const [loading, setLoading] = useState(true);          // État de chargement
  const [showPopup, setShowPopup] = useState(false);     // Contrôle du pop-up
  const [newValue, setNewValue] = useState({ description: "", duration: "" });          // Valeur saisie
  const [entries, setEntries] = useState([]);
  const chartRef = useRef(null);                         // Référence du canvas Chart.js
  const chartInstance = useRef(null);                    // Instance du graphique

  // ------------------ Récupération des données ------------------
  const fetchActivityData = async (type = "week") => {
    try {
      const params = { range_type: type };
      const response = await activityService.get_activity_entries(params);
      const data = response.data || response;
      setEntries(data);
    } catch (error) {
      console.error("[FRONT][ActivityCard] Erreur récupération des données :", error);
    }
  };

  // ------------------ Agrégation journalière ------------------
  const aggregateDailyAverages = (entries) => {
    const grouped = {};

    // Regroupement des activités par date
    entries.forEach((entry) => {
      const dateKey = entry.entry_date; // ✅ On utilise la date de la BDD
      if (!grouped[dateKey]) grouped[dateKey] = [];
      grouped[dateKey].push(entry.duration); // ✅ Champ adapté pour Activity
    });

    // Calcul des moyennes existantes
    const averagesByDate = {};
    Object.entries(grouped).forEach(([date, values]) => {
      averagesByDate[date] = values.reduce((a, b) => a + b, 0) / values.length;
    });

    // ✅ Génère la plage complète des 7 derniers jours
    const today = new Date();
    const last7days = [];
    for (let i = 6; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      const isoDate = d.toISOString().split("T")[0];
      last7days.push(isoDate);
    }

    // ✅ Construit les labels et les valeurs (même si vide)
    const aggregated = last7days.map((date) => ({
      label: new Date(date)
        .toLocaleDateString("fr-FR", { weekday: "long" })[0]
        .toUpperCase(),
      average: averagesByDate[date] ?? null, // null si aucune donnée
    }));

    return aggregated;
  };

  // ------------------ Création du graphique ------------------
  const renderChart = () => {
    if (!chartRef.current) return;
    const ctx = chartRef.current.getContext("2d");

    // 🔁 Détruire le graphique précédent s’il existe
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const aggregated = aggregateDailyAverages(entries);
    const labels = aggregated.map((d) => d.label);
    const dataValues = aggregated.map((d) => d.average);

    chartInstance.current = new Chart(ctx, {
      type: "bar", // ✅ graphique à barres
      data: {
        labels,
        datasets: [
          {
            label: "Durée d’activité (minutes)",
            data: dataValues,
            backgroundColor: "#C6B600",  // ✅ couleur jaune foncé comme ton visuel
            borderWidth: 0,              // pas de contour
            borderRadius: 4,             // coins légèrement arrondis
            barPercentage: 0.6,          // largeur relative des barres
            categoryPercentage: 0.8,     // espacement entre groupes
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: {
              display: false, // pas de lignes verticales
            },
            ticks: {
              color: "#000", // texte noir
              font: { size: 12 },
            },
          },
          y: {
            display: false,
          },
        },
        plugins: {
          legend: { display: false }, // pas de légende
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.parsed.y} min`, // affiche la durée exacte
            },
          },
        },
        layout: {
          padding: 10,
        },
      },
    });
  };


  // ------------------ Moyenne générale ------------------
  const fetchActivityAverage = async (type = "week") => {
    try {
      setLoading(true);
      const params = { range_type: type };
      const response = await activityService.get_activity_stats(params); // ✅ nom corrigé
      const avg = response.data?.average ?? null;
      setAverage(avg);
    } catch (error) {
      console.error("[FRONT][ActivityCard] Erreur récupération moyenne :", error);
      setAverage(null);
    } finally {
      setLoading(false);
    }
  };

  // ------------------ Ajout d’une activité ------------------
  const handleAddActivity = async (e) => {
    e.preventDefault();
    if (!newValue.description || !newValue.duration) return;

    try {
      const data = {
        description: newValue.description,
        duration: parseFloat(newValue.duration),
      };

      await activityService.create_activity_entry(data);

      // Rafraîchir les données et la moyenne
      fetchActivityAverage(rangeType);
      fetchActivityData(rangeType);

      // Réinitialiser le champ et fermer le pop-up
      setNewValue({ description: "", duration: "" });
      setShowPopup(false);
    } catch (error) {
      console.error("[FRONT][ActivityCard] Erreur ajout activité :", error);
    }
  };

  // ------------------ Effets React ------------------
  useEffect(() => {
    fetchActivityAverage(rangeType);
    fetchActivityData(rangeType);
  }, [rangeType]);

  useEffect(() => {
    if (entries.length > 0) {
      renderChart();
    }
  }, [entries]);

  // ------------------ Rendu JSX ------------------
  return (
    <section className="activity-card">
      <header className="card-header">
        <div className="card-icon"></div>
        <h2>Activité  physique</h2>
        <button className="add-button" onClick={() => setShowPopup(true)}>
          +
        </button>
      </header>

      <div className="weekly-average">
        <p>Cette semaine, tu as fait en moyenne :</p>
        {loading ? (
          <span className="average-value">...</span>
        ) : average !== null ? (
          <span className="average-value">{average} min/j</span>
        ) : (
          <span className="average-value">Aucune donnée</span>
        )}
      </div>

      <div className="chart-container">
        <canvas ref={chartRef}></canvas>
      </div>

      <footer className="card-footer">
        <div className="period-selector">
          <p>Ta moyenne sur :</p>
          <div className="buttons">
            <button onClick={() => setRangeType("month")}>30 jours</button>
            <button onClick={() => setRangeType("3months")}>90 jours</button>
          </div>
        </div>
        <div className="period-average">
          {loading ? (
            <span>...</span>
          ) : average !== null ? (
            <span>{average} min/j</span>
          ) : (
            <span>Aucune donnée</span>
          )}
        </div>
      </footer>

      {showPopup && (
        <div className="popup-overlay">
          <div className="popup-content">
            <button className="popup-close" onClick={() => setShowPopup(false)}>
              ✕
            </button>
            <h3>Combien de minutes d'activité aujourd’hui ?</h3>
            <form onSubmit={handleAddActivity}>
              <select value={newValue.description} onChange={(e) => setNewValue((prev) => ({ ...prev, description: e.target.value }))} required >
                <option value="">Choisis une activité</option>
                <option value="marche">Marche</option>
                <option value="natation">Natation</option>
                <option value="vélo">Vélo</option>
                <option value="yoga">Yoga</option>
                <option value="pilates">Pilates</option>
                <option value="renforcement">Renforcement musculaire</option>
                <option value="jardinage">Jardinage</option>
                <option value="bricolage">Bricolage</option>
                <option value="ménage">Ménage</option>
              </select>

              <input type="number" step="1" placeholder="Durée (minutes)" value={newValue.duration} onChange={(e) => setNewValue((prev) => ({ ...prev, duration: e.target.value }))} required />
              <button type="submit" className="confirm-button">
                Confirmer
              </button>
            </form>
          </div>
        </div>
      )}
    </section>
  );
}

export default ActivityCard;
