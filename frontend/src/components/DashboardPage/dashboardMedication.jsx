import React, { useState, useEffect, useRef } from "react";
import { medicationService } from "../../services/health/medicationService";

// import gestion des graphiques
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

// imports des images et des icones
import MedicationLogo from "../../assets/dashboard/page/DashboardIllustrationMedication.png";
import PlusIcon from "../../assets/dashboard/page/DashboardIconPlus.png";
import WarningIcon from "../../assets/dashboard/page/DashboardMedicationAttention.png";
import PopUpImage from "../../assets/dashboard/page/DashboardPopUpIllustrationMedication.png";
import PopUpCrossClose from "../../assets/dashboard/page/DashboardPopUpIconQuitter.png";

function MedicationCard() {
    // Gestion du pop-up
    const [showPopup, setShowPopup] = useState(false);

    const chartRef = useRef(null);
    const chartInstance = useRef(null);
    const [medications, setMedications] = useState([]);
    const [lowStockMed, setLowStockMed] = useState(null);
    const [selectedMed, setSelectedMed] = useState("");

    // Récupérer les données depuis la BDD */
    useEffect(() => {
        async function fetchData() {
        try {
            const response = await medicationService.get_medication_entries();
            const meds = response.data || [];
            setMedications(meds);

            // Vérifie si un médicament est sous le seuil
            const low = meds.find((m) => m.stock < m.alert_threshold);
            setLowStockMed(low);

            // Crée ou met à jour le graphique
            renderChart(meds);
        } catch (error) {
            console.error("Erreur lors de la récupération des médicaments :", error);
        }
        }
        fetchData();
    }, []);

    // Paramètrage du graphique
    function renderChart(data) {
        const ctx = chartRef.current.getContext("2d");

        const labels = data.map((m) => m.name);
        const stocks = data.map((m) => m.stock);

        if (chartInstance.current) chartInstance.current.destroy();

        chartInstance.current = new Chart(ctx, {
            type: "bar",
            data: {
                labels,
                datasets: [
                    {
                        label: "Stock (mg)",
                        data: stocks,
                        backgroundColor: "#F34FBF",
                        borderWidth: 0,
                        borderRadius: 4,
                        barPercentage: 0.8,          // largeur relative des barres
                        categoryPercentage: 0.9,     // espacement entre groupes
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: "#FFF",
                            font: { size: 9 },
                        },
                        grid: {
                            color: "#FFFFFF",
                            drawBorder: true,
                            borderColor: "#000",
                            lineWidth: 0.5,
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
                            lineWidth: 0.5,
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
    }

    async function handleTakeDose(event) {
        event.preventDefault();
        if (!selectedMed) return;

        try {
            await medicationService.take_medication_dose(selectedMed);
            const refreshed = await medicationService.get_medication_entries();
            setMedications(refreshed.data);
            renderChart(refreshed.data);

            const low = refreshed.data.find((m) => m.stock < m.alert_threshold);
            setLowStockMed(low || null);

            setShowPopup(false);
            setSelectedMed("");
        } catch (error) {
            console.error("Erreur lors de la prise de dose :", error);
        }
    }

    return (
        <section className="card card--medication">
            <header className="card__header">
                <div className="card__title">
                    <img src={MedicationLogo} alt="Icône Glycémie" className="card__icon" />
                    <h2 className="card__heading">Médication</h2>
                </div>
                <button className="card__btn-add" onClick={() => setShowPopup(true)}>
                    <img src={PlusIcon} alt="Ajouter" />
                </button>
            </header>
            <div className="card__chart">
                <canvas ref={chartRef}></canvas>
            </div>
            {lowStockMed && (
                <footer className="medication-card__warning">
                    <img src={WarningIcon} className="medication-card__icon"/>
                    <div className="medication-card__text">
                        <h2>{lowStockMed.name}</h2>
                        <p>Attention, il vous reste {lowStockMed.stock} mg</p>
                    </div>
                </footer>
            )}
            {showPopup && (
                <div className="popup">
                    <img src={PopUpImage} alt="Décor popup" className="popup__img" />
                    <div className="popup__overlay">
                        <button className="popup__close" onClick={() => setShowPopup(false)}>
                            <img src={PopUpCrossClose} alt="Fermer" />
                        </button>
                        <div className="popup__content">
                            <h3 className="popup__title">As-tu pris tes médicaments aujourd'hui ?</h3>
                            <form className="popup__form">
                                <select
                                    value={selectedMed}
                                    onChange={(e) => setSelectedMed(e.target.value)}
                                    >
                                    <option value="">Choisir un médicament</option>
                                    {medications.map((m) => (
                                        <option key={m.id} value={m.id}>
                                            {m.name}: 1x dose
                                        </option>
                                    ))}
                                </select>
                                <button type="submit" className="popup__btn-confirm" onClick={handleTakeDose}>Ajouter</button>
                            </form>
                        </div>
                    </div>
                </div>
            )}
        </section>
    )
}
export default MedicationCard
