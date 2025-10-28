import React, {useState} from "react";

// import des outils
//import { validateField } from "../utils/validator";
//import { formatData } from "../utils/dataFormatter";


function GlycemiaCard() {
    return (
        <section className="glycemia-card">
            {/* --- En-tête de la card --- */}
            <header className="card-header">
                <div className="card-icon"></div>
                <h2>Glycémie</h2>
                <button className="add-button">+</button>
            </header>

            {/* --- Moyenne hebdomadaire --- */}
            <div className="weekly-average">
                <p>Cette semaine, tu as une glycémie d’en moyenne :</p>
                <span className="average-value">150mg/l</span>
            </div>

            {/* --- Graphique --- */}
            <div className="chart-container">
                {/* Ici viendra ton composant Chart.js plus tard */}
                <canvas id="glycemiaChart"></canvas>
            </div>

            {/* --- Moyenne sur période --- */}
            <footer className="card-footer">
                <div className="period-selector">
                <p>Ta moyenne sur :</p>
                <div className="buttons">
                    <button>30 jours</button>
                    <button>90 jours</button>
                </div>
                </div>
                <div className="period-average">
                <span>150mg/l</span>
                </div>
            </footer>
        </section>
    )
}
export default GlycemiaCard
