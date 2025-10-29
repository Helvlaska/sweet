import React, { useState, useEffect, useRef } from "react";
import { glycemiaService } from "../../services/glycemiaService";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

function GlycemiaCard() {

  const [average, setAverage] = useState(null);          // moyenne actuelle
  const [rangeType, setRangeType] = useState("week");    // période choisie ("week", "month", etc.)
  const [loading, setLoading] = useState(true);          // état de chargement
  const [showPopup, setShowPopup] = useState(false);     // contrôle du pop-up
  const [newValue, setNewValue] = useState("");          // valeur saisie
  const [entries, setEntries] = useState([]);
  const chartRef = useRef(null);                         // Référence du canvas Chart.js
  const chartInstance = useRef(null);                    // Instance du graphique

  const fetchGlycemiaData = async (type = "week") => {
    try {
      const params = { range_type: type };
      const response = await glycemiaService.get_glycemia_entries(params);
      const data = response.data || response;

      // Crée le graphique après avoir récupéré les données
      setEntries(data);
    } catch (error) {
      console.error("[FRONT][GlycemiaCard] Erreur récupération des données :", error);
    }
  };

  const aggregateDailyAverages = (entries) => {
    const grouped = {};

    // Regroupement des mesures par date
    entries.forEach((entry) => {
      const dateKey = entry.entry_date; // ✅ on utilise la date de la BDD
      if (!grouped[dateKey]) grouped[dateKey] = [];
      grouped[dateKey].push(entry.glucose_level);
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
      label: new Date(date).toLocaleDateString("fr-FR", { weekday: "long" })[0].toUpperCase(),
      average: averagesByDate[date] ?? null, // null si aucune donnée
    }));

    return aggregated;
  };


  const renderChart = () => {
    if (!chartRef.current) return;
    const ctx = chartRef.current.getContext("2d");

    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const aggregated = aggregateDailyAverages(entries);
    const labels = aggregated.map((d) => d.label);
    const dataValues = aggregated.map((d) => d.average);


    chartInstance.current = new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Taux de glycémie (mg/dL)",
            data: dataValues,
            spanGaps: false,
            borderColor: "#CCCCCC",               // ligne gris clair
            backgroundColor: "rgba(255, 255, 255, 1)", // points blancs
            borderWidth: 1.5,
            fill: false,                          // pas de remplissage
            tension: 0,                           // lignes droites
            pointRadius: 8,                       // taille des points
            pointBackgroundColor: "#FFFFFF",      // fond des points
            pointBorderWidth: 1,
            pointBordercolor: "#BFCDFE",
            pointHoverRadius: 10,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            min: 50,
            max: 300,
            ticks: {
              stepSize: 50,
              callback: (value) => `${value}mg`,
              color: "#666",             // couleur du texte
              font: { size: 11 },
            },
            grid: {
                color: "#E0E0E0",          // grille gris clair
                lineWidth: 1,
            },
          },
          x: {
            ticks: {
              color: "#666",
              font: { size: 11 },
            },
            grid: {
              color: "#E0E0E0",
              lineWidth: 1,
            },
          },
        },
        plugins: {
          legend: { display: false },
        },
        layout: {
          padding: 10,
        },
      },
    });
  };

  const fetchGlycemiaAverage = async (type = "week") => {
    try {
      setLoading(true);
      const params = { range_type: type };
      const response = await glycemiaService.get_glycemia_stats(params);

      // le backend renvoie { average: nombre }
      const avg = response.data?.average ?? null;
      setAverage(avg);
    } catch (error) {
      console.error("[FRONT][GlycemiaCard] Erreur lors de la récupération de la moyenne :", error);
      setAverage(null);
    } finally {
      setLoading(false);
    }
  };

  const handleAddGlycemia = async (e) => {
    e.preventDefault();
    if (!newValue) return;

    try {
      const data = { glucose_level: parseFloat(newValue) };
      await glycemiaService.create_glycemia_entry(data);

      // Rafraîchir la moyenne
      fetchGlycemiaAverage(rangeType);
      fetchGlycemiaData(rangeType);

      // Réinitialiser le champ et fermer le pop-up
      setNewValue("");
      setShowPopup(false);
    } catch (error) {
      console.error("[FRONT][GlycemiaCard] Erreur ajout glycémie :", error);
    }
  };

  // ------------------ Chargement initial ------------------
  useEffect(() => {
    fetchGlycemiaAverage(rangeType);
    fetchGlycemiaData(rangeType);
  }, [rangeType]);

  useEffect(() => {
    if (entries.length > 0) {
      renderChart();
    }
  }, [entries]);

  // ------------------ Rendu JSX ------------------
  return (
    <section className="glycemia-card">
      <header className="card-header">
        <div className="card-icon"></div>
        <h2>Glycémie</h2>
        <button className="add-button" onClick={() => setShowPopup(true)}>
          +
        </button>
      </header>

      <div className="weekly-average">
        <p>Cette semaine, tu as une glycémie d’en moyenne :</p>
        {loading ? (
          <span className="average-value">...</span>
        ) : average !== null ? (
          <span className="average-value">{average} mg/dL</span>
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
            <span>{average} mg/dL</span>
          ) : (
            <span>Aucune donnée</span>
          )}
        </div>
      </footer>

      {showPopup && (
        <div className="popup-overlay">
          <div className="popup-content">
            <button className="popup-close" onClick={() => setShowPopup(false)} >
              ✕
            </button>
            <h3>Quelle est la glycémie de ta journée ?</h3>
            <form onSubmit={handleAddGlycemia}>
              <input type="number" step="0.1" placeholder="Glycémie (mg/dL)" value={newValue} onChange={(e) => setNewValue(e.target.value)} required />
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

export default GlycemiaCard;
