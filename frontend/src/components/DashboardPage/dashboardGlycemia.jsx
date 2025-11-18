import React, { useState, useEffect, useRef } from "react";
import { glycemiaService } from "../../services/glycemiaService";

// import gestion des graphiques
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

// imports des images et des icones
import GlycemiaLogo from "../../assets/dashboard/page/DashboardIllustrationGlycemie.png";
import PlusIcon from "../../assets/dashboard/page/DashboardIconPlus.png";
import PopUpImage from "../../assets/dashboard/page/DashboardPopUpIllustrationGlycemie.png";
import PopUpCrossClose from "../../assets/dashboard/page/DashboardPopUpIconQuitter.png";

function GlycemiaCard() {
    // Stockage des valeurs
    const [average, setAverage] = useState(null);          // moyenne actuelle
    const [rangeType, setRangeType] = useState("week");    // période choisie ("week", "month", etc.)
    const [newValue, setNewValue] = useState("");          // valeur saisie
    const [entries, setEntries] = useState([]);

    // Gestion du chargement des données
    const [loading, setLoading] = useState(true);          // état de chargement

    // Gestion du pop-up
    const [showPopup, setShowPopup] = useState(false);     // contrôle du pop-up

    // Gestion du graphique
    const chartRef = useRef(null);                         // Référence du canvas Chart.js
    const chartInstance = useRef(null);                    // Instance du graphique

    // Récupération des données
    const fetchGlycemiaData = async (type = "week") => {
        try {
            // Récupération des données
            const params = { range_type: type };
            const response = await glycemiaService.get_glycemia_entries(params);
            const data = response.data || response;

            // Crée le graphique après avoir récupéré les données
            setEntries(data);
        } catch (error) {
            console.error("[FRONT][GlycemiaCard] Erreur récupération des données :", error);
        }
    };

    // Gestion agrégation journalière (nb point/jour)
    function aggregateDailyAverages(entries) {
        const grouped = {};

        // Regroupement des mesures par date
        entries.forEach((entry) => {
            const dateKey = entry.entry_date;
            if (!grouped[dateKey]) grouped[dateKey] = [];
            grouped[dateKey].push(entry.glucose_level);
        });

        // Calcul des moyennes existantes
        const averagesByDate = {};
        Object.entries(grouped).forEach(([date, values]) => {
            averagesByDate[date] = values.reduce((a, b) => a + b, 0) / values.length;
        });

        // Génère la plage complète des 7 derniers jours
        const today = new Date();
        const last7days = [];
        for (let i = 6; i >= 0; i--) {
            const d = new Date(today);
            d.setDate(today.getDate() - i);
            const isoDate = d.toISOString().split("T")[0];
            last7days.push(isoDate);
        }

        // Construit les labels et les valeurs (même si vide)
        const aggregated = last7days.map((date) => ({
            label: new Date(date).toLocaleDateString("fr-FR", { weekday: "long" })[0].toUpperCase(),
            average: averagesByDate[date] ?? null, // null si aucune donnée
        }));
        return aggregated;
    };

    // Création du graphique
    function renderChart() {
        if (!chartRef.current) return;
        const ctx = chartRef.current.getContext("2d");

        // Détruire le graphique précédent s'il existe
        if (chartInstance.current) {
            chartInstance.current.destroy();
        }

        // Gestion des agrégations, des labels, et des moyennes
        const aggregated = aggregateDailyAverages(entries);
        const labels = aggregated.map((d) => d.label);
        const dataValues = aggregated.map((d) => d.average);

        // Paramètrages du graphique
        chartInstance.current = new Chart(ctx, {
            type: "line",
            data: {
                labels,
                datasets: [
                    {
                        label: "Taux de glycémie (mg/l)",
                        data: dataValues,
                        spanGaps: false,
                        borderColor: "#72655A",               // ligne gris clair
                        backgroundColor: "rgba(255, 255, 255, 1)", // points blancs
                        borderWidth: 1,
                        fill: false,                          // pas de remplissage
                        tension: 0,                           // lignes droites
                        pointRadius: 6,                       // taille des points
                        pointBackgroundColor: "#FFFFFF",      // fond des points
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
                        min: 50,
                        max: 300,
                        ticks: {
                            stepSize: 50,
                            callback: (value) => `${value}mg`,
                            color: "#000",             // couleur du texte
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
                            color: "#000",
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

    // Gestion des moyennes
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

    // Ajout d'une mesure de glycémie
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

    // Paramètrage du composant
    useEffect(() => {
        fetchGlycemiaAverage(rangeType);
        fetchGlycemiaData(rangeType);
    }, [rangeType]);

    useEffect(() => {
        if (entries.length > 0) {
            renderChart();
        }
    }, [entries]);

    return (
        <section className="card card--glycemia">
            <header className="card__header">
                <div className="card__title">
                    <img src={GlycemiaLogo} alt="Icône Glycémie" className="card__icon" />
                    <h2 className="card__heading">Glycémie</h2>
                </div>
                <button className="card__btn-add" onClick={() => setShowPopup(true)}>
                    <img src={PlusIcon} alt="Ajouter" />
                </button>
            </header>
            <div className="card__body">
                <div className="card__weekly">
                    <p className="card__text">
                        Cette semaine, tu as une glycémie d’en moyenne :
                    </p>
                    {loading ? (
                        <span className="card__value card__value--loading">...</span>
                    ) : average !== null ? (
                        <span className="card__value">{average} mg/l</span>
                    ) : (
                        <span className="card__value card__value--empty">Aucune donnée</span>
                    )}
                </div>
                <div className="card__chart">
                    <canvas ref={chartRef}></canvas>
                </div>
            </div>
            <footer className="card__footer">
                <p className="card__text">Ta moyenne sur :</p>
                <div className="card__period">
                    <div className="card__period-buttons">
                        <button className={`card__period-btn ${rangeType === "month" ? "card__period-btn--active" : ""}`} onClick={() => setRangeType("month")}>30 jours</button>
                        <button className={`card__period-btn ${rangeType === "3months" ? "card__period-btn--active" : ""}`} onClick={() => setRangeType("3months")}>90 jours</button>
                    </div>
                    <div className="card__period-value">
                        {loading ? (
                            <span className="card__value card__value--loading">...</span>
                        ) : average !== null ? (
                            <span className="card__value">{average} mg/l</span>
                        ) : (
                            <span className="card__value card__value--empty">Aucune donnée</span>
                        )}
                    </div>
                </div>
            </footer>
            {showPopup && (
                <div className="popup">
                    <img src={PopUpImage} alt="Décor popup" className="popup__img" />
                    <div className="popup__overlay">
                        <button className="popup__close" onClick={() => setShowPopup(false)}>
                            <img src={PopUpCrossClose} alt="Fermer" />
                        </button>
                        <div className="popup__content">
                            <h3 className="popup__title">Quelle est la glycémie de ta journée ?</h3>
                            <form className="popup__form" onSubmit={handleAddGlycemia}>
                                <input type="number" step="0.1" placeholder="Glycémie (mg/l)" value={newValue} onChange={(e) => setNewValue(e.target.value)} required className="popup__input" />
                                <button type="submit" className="popup__btn-confirm">Confirmer</button>
                            </form>
                        </div>
                    </div>
                </div>
            )}
        </section>
    );
}

export default GlycemiaCard;
