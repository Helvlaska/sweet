import React, { useState, useEffect, useRef } from "react";
import { weightService } from "../../services/health/weightService";

// import gestion graphique
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

// import des images et icones
import WeightLogo from "../../assets/dashboard/page/DashboardIllustrationPoids.png";
import PlusIcon from "../../assets/dashboard/page/DashboardIconPlus.png";
import PopUpImage from "../../assets/dashboard/page/DashboardPopUpIllustrationPoids.png";
import PopUpCrossClose from "../../assets/dashboard/page/DashboardPopUpIconQuitter.png";

function WeightCard() {
    // Stockage des valeurs
    const [entries, setEntries] = useState([]);
    const [rangeType, setRangeType] = useState("week");
    const [newValue, setNewValue] = useState({ intPart: "", decPart: "" });

    // Gestion du chargement des données
    const [loading, setLoading] = useState(true);

    // Gestion du pop-up
    const [showPopup, setShowPopup] = useState(false);

    // Gestion du graphique
    const chartRef = useRef(null);
    const chartInstance = useRef(null);

    // Récupération des données
    async function fetchWeightData(type) {
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

    // Gestion agrégation journalière (nb point/jour)
    function aggregateWeightData(entries, rangeType) {
        const grouped = {};

        // Regroupe les masses par date
        entries.forEach(entry => {
            const dateKey = entry.entry_date;
            if (!grouped[dateKey]) grouped[dateKey] = [];
            grouped[dateKey].push(entry.mass);
        });

        // Calcule les moyennes par jour
        const dailyAverages = Object.entries(grouped).map(([date, values]) => ({
            date: new Date(date),
            average: values.reduce((a, b) => a + b, 0) / values.length
        }));

        // On génère la plage complète de dates selon le range
        const today = new Date();
        let startDate;
        if (rangeType === "week") startDate = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 6);
        else if (rangeType === "month") startDate = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 29);
        else if (rangeType === "3months") startDate = new Date(today.getFullYear(), today.getMonth() - 2, today.getDate());
        else if (rangeType === "6months") startDate = new Date(today.getFullYear(), today.getMonth() - 5, today.getDate());

        // Crée une date par jour sur la période choisie
        const completeRange = [];
        const currentDate = new Date(startDate);
        while (currentDate <= today) {
            const formatted = new Date(currentDate);
            const existing = dailyAverages.find(d => d.date.toDateString() === formatted.toDateString());
            if (existing) {
                completeRange.push({ date: formatted, average: existing.average });
            } else {
                completeRange.push({ date: formatted, average: null }); // "trou" explicite
            }
            currentDate.setDate(currentDate.getDate() + 1);
        }

        return completeRange;
    }



    // Création du graphique
    function renderChart() {
        if (!chartRef.current) return;
        const ctx = chartRef.current.getContext("2d");
        if (chartInstance.current) chartInstance.current.destroy();

        const aggregated = aggregateWeightData(entries, rangeType);

        const labels = aggregated.map(d =>
            d.date.toLocaleDateString("fr-FR", { day: "2-digit", month: "short" })
        );

        const dataValues = aggregated.map(d => d.average);

        // Calcul du centrage sur la moyenne
        const validValues = dataValues.filter(v => typeof v === "number");
        const avg = validValues.length > 0
            ? validValues.reduce((a, b) => a + b, 0) / validValues.length
            : 70;
        const yMin = Math.floor((avg - 10) / 5) * 5;
        const yMax = Math.ceil((avg + 10) / 5) * 5;

        // Paramètrage du graphique
        chartInstance.current = new Chart(ctx, {
            type: "line",
            data: {
                labels,
                datasets: [
                    {
                        label: "Poids (kg)",
                        data: dataValues,
                        spanGaps: false,
                        borderColor: "#72655A",
                        backgroundColor: "rgba(255, 255, 255, 1)",
                        borderWidth: 1,
                        fill: false,
                        tension: 0,
                        pointRadius: 6,
                        pointBackgroundColor: "#FFFFFF",
                        pointBorderWidth: 0,
                        pointHoverRadius: 10,
                        pointHoverBackgroundColor: "#FFFFFF",
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: yMin,
                        max: yMax,
                        ticks: {
                            stepSize: 5,
                            callback: (value) => `${value}kg`,
                            color: "#FFF",
                            font: { size: 9 },
                        },
                        grid: {
                            color: "#FFFFFF",
                            drawBorder: true,
                            borderColor: "#000",
                            lineWidth: 1,
                        },
                    },
                    x: {
                        ticks: {
                            color: "#FFF",
                            font: { size: 9 },
                        },
                        grid: {
                            color: "#FFFFFF",
                            drawBorder: true,
                            borderColor: "#000",
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

    // Ajout d'une nouvelle donnée
    const handleAddWeight = async (e) => {
        e.preventDefault();
        if (!newValue.intPart) return;

        // Additionne les parties
        let fullValue = parseFloat(newValue.intPart) + parseFloat(newValue.decPart || 0);
        console.log("première partie de la valeur:", newValue.intPart);
        console.log("deuxième partie de la valeur:", newValue.decPart);

        // Force la conversion explicite en float avec une décimale
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

    // Paramètrage du composant
    useEffect(() => {
        fetchWeightData(rangeType);
    }, [rangeType]);

    useEffect(() => {
        if (entries.length > 0) {
            renderChart();
        }
    }, [entries, rangeType]);

    return (
        <section className="card card--weight">
            <header className="card__header">
                <div className="card__title">
                    <img src={WeightLogo} alt="Icône Poids" className="card__icon" />
                    <h2 className="card__heading">Poids</h2>
                </div>
                <button className="card__btn-add" onClick={() => setShowPopup(true)}>
                    <img src={PlusIcon} alt="Ajouter" />
                </button>
            </header>
            <div className="card__body">
                <div className="card__period-buttons">
                    <button className={`card__period-btn ${rangeType === "week" ? "card__period-btn--active" : ""}`} onClick={() => setRangeType("week")}>7 jours</button>
                    <button className={`card__period-btn ${rangeType === "month" ? "card__period-btn--active" : ""}`} onClick={() => setRangeType("month")}>30 jours</button>
                    <button className={`card__period-btn ${rangeType === "3months" ? "card__period-btn--active" : ""}`} onClick={() => setRangeType("3months")}>90 jours</button>
                    <button className={`card__period-btn ${rangeType === "6months" ? "card__period-btn--active" : ""}`} onClick={() => setRangeType("6months")}>6 mois</button>
                </div>
            </div>
            <div className="card__chart">
                {loading ? <p>Chargement...</p> : <canvas ref={chartRef}></canvas>}
            </div>
            {showPopup && (
                <div className="popup">
                    <img src={PopUpImage} alt="Décor popup" className="popup__img" />
                    <div className="popup__overlay">
                       <button className="popup__close" onClick={() => setShowPopup(false)}>
                            <img src={PopUpCrossClose} alt="Fermer" />
                        </button>
                        <div className="popup__content">
                            <h3 className="popup__title">Quel est ton poids ?</h3>
                            <form onSubmit={handleAddWeight} className="popup__form">
                                <div className="popup__select">
                                    <select value={newValue.intPart} onChange={(e) => setNewValue((prev) => ({ ...prev, intPart: e.target.value }))} required className="popup__select-1">
                                        <option value="">kilo</option>
                                        {Array.from({ length: 400 }, (_, i) => (
                                            <option key={i + 1} value={i + 1}>
                                                {i + 1}
                                            </option>
                                        ))}
                                    </select>
                                    <span className="popup__select-comma">.</span>
                                    <select value={newValue.decPart} onChange={(e) => setNewValue((prev) => ({ ...prev, decPart: e.target.value }))} required className="popup__select-2">
                                        <option value="">gramme</option>
                                        {Array.from({ length: 10 }, (_, i) => (
                                            <option key={i} value={i / 10}>
                                                {i}
                                            </option>
                                        ))}
                                    </select>
                                    <span className="popup__select-unit">kg</span>
                                </div>
                                <button type="submit" className="popup__btn-confirm">
                                    Confirmer
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            )}
        </section>
    );
}

export default WeightCard;
