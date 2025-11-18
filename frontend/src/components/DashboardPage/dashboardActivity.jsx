import React, { useState, useEffect, useRef } from "react";
import { activityService } from "../../services/activityService"

// import gestion des graphiques
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

// imports des images et icones
import ActivityLogo from "../../assets/dashboard/page/DashboardIllustrationSport.png";
import PlusIcon from "../../assets/dashboard/page/DashboardIconPlus.png";
import PopUpImage from "../../assets/dashboard/page/DashboardPopUpIllustrationSport.png";
import PopUpCrossClose from "../../assets/dashboard/page/DashboardPopUpIconQuitter.png";

function ActivityCard() {
    // Stockage des valeurs
    const [average, setAverage] = useState(null);          // Moyenne actuelle
    const [rangeType, setRangeType] = useState("week");    // Période choisie ("week", "month", etc.)
    const [newValue, setNewValue] = useState({ description: "", duration: "" });          // Valeur saisie
    const [entries, setEntries] = useState([]);

    // Gestion du chargement des données
    const [loading, setLoading] = useState(true);          // État de chargement

    // Gestion du pop-up
    const [showPopup, setShowPopup] = useState(false);     // Contrôle du pop-up

    // Gestion du graphique
    const chartRef = useRef(null);                         // Référence du canvas Chart.js
    const chartInstance = useRef(null);                    // Instance du graphique

    // Récupération des données
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

    // Gestion agrégation journalière (nb point/jour)
    function aggregateDailyAverages(entries) {
        const grouped = {};

        // Regroupement des activités par date
        entries.forEach((entry) => {
            const dateKey = entry.entry_date;
            if (!grouped[dateKey]) grouped[dateKey] = [];
            grouped[dateKey].push(entry.duration);
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
        label: new Date(date)
            .toLocaleDateString("fr-FR", { weekday: "long" })[0]
            .toUpperCase(),
            average: averagesByDate[date] ?? null, // null si aucune donnée
        }));

        return aggregated;
    };

    // Création du graphique
    function renderChart() {
        if (!chartRef.current) return;
        const ctx = chartRef.current.getContext("2d");

        // Détruire le graphique précédent s’il existe
        if (chartInstance.current) {
            chartInstance.current.destroy();
        }

        // Gestion des agrégations, des labels, et des moyennes
        const aggregated = aggregateDailyAverages(entries);
        const labels = aggregated.map((d) => d.label);
        const dataValues = aggregated.map((d) => d.average);

        // Paramètrage du graphique
        chartInstance.current = new Chart(ctx, {
            type: "bar",
            data: {
                labels,
                datasets: [
                    {
                        label: "Durée d’activité (minutes)",
                        data: dataValues,
                        backgroundColor: "#D3BC00",
                        borderWidth: 0,
                        borderRadius: 4,
                        barPercentage: 1,          // largeur relative des barres
                        categoryPercentage: 0.9,     // espacement entre groupes
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
                            font: { size: 9 },
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


    // Gestion des moyennes
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

    // Ajout d’une activité
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

    // Paramètrage du composant
    useEffect(() => {
        fetchActivityAverage(rangeType);
        fetchActivityData(rangeType);
    }, [rangeType]);

    useEffect(() => {
        if (entries.length > 0) {
        renderChart();
        }
    }, [entries]);

    return (
        <section className="card card--activity">
            <header className="card__header">
                <div className="card__title">
                    <img src={ActivityLogo} alt="Icône Activité Physique" className="card__icon" />
                    <h2 className="card__heading">Activité  physique</h2>
                </div>
                <button className="card__btn-add" onClick={() => setShowPopup(true)}>
                    <img src={PlusIcon} alt="Ajouter" />
                </button>
            </header>
            <div className="card__body">
                <div className="card__weekly">
                    <p className="card__text">Cette semaine, tu as fait en moyenne :</p>
                    {loading ? (
                        <span className="card__value card__value--loading">...</span>
                    ) : average !== null ? (
                        <span className="card__value">{average} min/j</span>
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
                            <span className="card__value">{average} min/j</span>
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
                            <h3 className="popup__title">Combien de temps t’es-tu dépensé aujourd’hui ?</h3>
                            <form className="popup__form" onSubmit={handleAddActivity}>
                                <select value={newValue.description} onChange={(e) => setNewValue((prev) => ({ ...prev, description: e.target.value }))} required className="popup__select">
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
                                <input type="number" step="1" placeholder="Durée (minutes)" value={newValue.duration} onChange={(e) => setNewValue((prev) => ({ ...prev, duration: e.target.value }))} required className="popup__input"/>
                                <button type="submit" className="popup__btn-confirm">
                                    Ajouter
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            )}
        </section>
    );
}

export default ActivityCard;
