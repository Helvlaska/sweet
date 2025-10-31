import React, { useState, useEffect, useRef } from "react";
import { weightService } from "../../services/weightService";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

function WeightCard() {
  const [entries, setEntries] = useState([]);
  const [rangeType, setRangeType] = useState("week");
  const [loading, setLoading] = useState(true);
  const [showPopup, setShowPopup] = useState(false);
  const [newValue, setNewValue] = useState({ intPart: "", decPart: "" });
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  // ------------------ Récupération des données ------------------
  const fetchWeightData = async (type = "week") => {
    try {
      setLoading(true);
      const params = { range_type: type };
      const response = await weightService.get_weight_entries(params);
      const data = response.data || response;
      setEntries(data);
    } catch (error) {
      console.error("[FRONT][WeightCard] Erreur récupération des données :", error);
    } finally {
      setLoading(false);
    }
  };

  // ------------------ Agrégation journalière ------------------
  const aggregateWeightData = (entries, rangeType) => {
    const grouped = {};

    entries.forEach((entry) => {
      const dateKey = entry.entry_date;
      if (!grouped[dateKey]) grouped[dateKey] = [];
      grouped[dateKey].push(entry.mass);
    });

    // Moyenne par jour
    const dailyAverages = Object.entries(grouped).map(([date, values]) => ({
      date,
      average: values.reduce((a, b) => a + b, 0) / values.length,
    }));

    // 🧠 Selon la période, on agrège différemment
    if (rangeType === "week" || rangeType === "month") {
      // 7j ou 30j → moyenne par jour
      return dailyAverages.map((d) => ({
        label: new Date(d.date).toLocaleDateString("fr-FR", { weekday: "short" })[0].toUpperCase(),
        average: d.average,
      }));
    }

    if (rangeType === "3months" || rangeType === "6months") {
      // 90j ou 6 mois → moyenne par semaine
      const weekly = {};
      dailyAverages.forEach((d) => {
        const dateObj = new Date(d.date);
        const weekNumber = Math.ceil(dateObj.getDate() / 7) + dateObj.getMonth() * 4; // repère grossier
        if (!weekly[weekNumber]) weekly[weekNumber] = [];
        weekly[weekNumber].push(d.average);
      });

      return Object.entries(weekly).map(([week, values]) => ({
        label: `S${week}`,
        average: values.reduce((a, b) => a + b, 0) / values.length,
      }));
    }

    return dailyAverages;
  };


  // ------------------ Création du graphique ------------------
  const renderChart = () => {
    if (!chartRef.current) return;
    const ctx = chartRef.current.getContext("2d");

    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    // ------------------ Gestion dynamique de l’axe X ------------------
    let labels = [];
    if (rangeType === "week") {
      labels = ["L", "M", "M", "J", "V", "S", "D"];
    }
    else if (rangeType === "month") {
      const today = new Date();
      for (let i = 29; i >= 0; i -= 3) {
        const d = new Date(today);
        d.setDate(today.getDate() - i);
        labels.push(d.getDate().toString());
      }
    }
    else if (rangeType === "3months") {
      labels = Array.from({ length: 13 }, (_, i) => `S${i + 1}`);
    }
    else if (rangeType === "6months") {
      labels = Array.from({ length: 6 }, (_, i) => `M${i + 1}`);
    }

    // ------------------ Données du graphique ------------------
    const aggregated = aggregateWeightData(entries, rangeType);
    const dataValues = aggregated.map((d) => d.average);

    // ------------------ Gestion dynamique de l’axe Y ------------------
    const validValues = entries.map(e => e.mass).filter(v => typeof v === "number");
    const avg = validValues.length > 0
      ? validValues.reduce((a, b) => a + b, 0) / validValues.length
      : 70; // fallback si vide

    const yMin = Math.floor(avg - 10);
    const yMax = Math.ceil(avg + 10);

    // ------------------ Création du graphique ------------------
    chartInstance.current = new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Poids (kg)",
            data: dataValues,
            spanGaps: false,
            borderColor: "#CCCCCC",
            backgroundColor: "rgba(255, 255, 255, 1)",
            borderWidth: 1.5,
            fill: false,
            tension: 0, // lignes droites
            pointRadius: 8,
            pointBackgroundColor: "#FFFFFF",
            pointBorderWidth: 1,
            pointBordercolor: "#BFCDFE",
            pointHoverRadius: 10,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 600, // transition douce
        },
        scales: {
          y: {
            min: yMin,
            max: yMax,
            ticks: {
              stepSize: 5,
              callback: (value) => `${value}kg`,
              color: "#666",
              font: { size: 11 },
            },
            grid: {
              color: "#E0E0E0",
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


  // ------------------ Ajout d'une nouvelle donnée ------------------
  const handleAddWeight = async (e) => {
    e.preventDefault();
    if (!newValue.intPart) return;

    // On additionne proprement les parties
    let fullValue = parseFloat(newValue.intPart) + parseFloat(newValue.decPart || 0);
    console.log("première partie de la valeur:", newValue.intPart);
    console.log("deuxième partie de la valeur:", newValue.decPart);
    // ✅ Force la conversion explicite en float avec une décimale
    fullValue = parseFloat(fullValue.toFixed(1));
    console.log("fullvalue:", fullValue);

    const data = { mass: Number(fullValue.toFixed(1)) };
    console.log("Valeur envoyée au backend :", data, typeof data.mass);

    try {
      await weightService.create_weight_entry(data);
      fetchWeightData(rangeType);

      setNewValue({ intPart: "", decPart: "" });
      setShowPopup(false);
    } catch (error) {
      console.error("[FRONT][WeightCard] Erreur ajout poids :", error);
    }
  };


  // ------------------ Effets React ------------------
  useEffect(() => {
    fetchWeightData(rangeType);
  }, [rangeType]);

  useEffect(() => {
    if (entries.length > 0) {
      renderChart();
    }
  }, [entries, rangeType]);

  // ------------------ Rendu JSX ------------------
  return (
    <section className="weight-card">
      <header className="card-header">
        <div className="card-icon"></div>
        <h2>Poids</h2>
        <button className="add-button" onClick={() => setShowPopup(true)}>
          +
        </button>
      </header>

      <div className="period-buttons">
        <button className={rangeType === "week" ? "active" : ""} onClick={() => setRangeType("week")}>
          7 jours
        </button>
        <button className={rangeType === "month" ? "active" : ""} onClick={() => setRangeType("month")}>
          30 jours
        </button>
        <button className={rangeType === "3months" ? "active" : ""} onClick={() => setRangeType("3months")}>
          90 jours
        </button>
        <button className={rangeType === "6months" ? "active" : ""} onClick={() => setRangeType("6months")}>
          6 mois
        </button>
      </div>

      <div className="chart-container">
        {loading ? <p>Chargement...</p> : <canvas ref={chartRef}></canvas>}
      </div>

      {showPopup && (
        <div className="popup-overlay">
          <div className="popup-content">
            <button className="popup-close" onClick={() => setShowPopup(false)}>
              ✕
            </button>
            <h3>Quel est ton poids aujourd’hui ?</h3>
            <form onSubmit={handleAddWeight} className="weight-form">
              <div className="weight-select-group">
                <select value={newValue.intPart} onChange={(e) => setNewValue((prev) => ({ ...prev, intPart: e.target.value }))} required >
                    <option value="">--</option>
                    {Array.from({ length: 400 }, (_, i) => (
                        <option key={i + 1} value={i + 1}>
                            {i + 1}
                        </option>
                    ))}
                </select>
                <span className="comma">,</span>
                <select value={newValue.decPart} onChange={(e) => setNewValue((prev) => ({ ...prev, decPart: e.target.value }))} required>
                    <option value="">--</option>
                    {Array.from({ length: 10 }, (_, i) => (
                        <option key={i} value={i / 10}>
                            {i}
                        </option>
                    ))}
                </select>
                <span className="unit">kg</span>
            </div>
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

export default WeightCard;
