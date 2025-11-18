//import React, {useState} from "react";

// Import des outils
//import {validateField} from "../utils/validator";
//import { formatData } from "../utils/dataFormatter";
//import { Link, useNavigate } from "react-router-dom";

// Import des composants
import DashboardHeader from "../components/DashboardPage/dashboardHeader";
import NavBar from "../components/DashboardPage/dashboardNavbar";
import GlycemiaCard from "../components/DashboardPage/dashboardGlycemia";
import ActivityCard from "../components/DashboardPage/dashboardActivity";
import MedicationCard from "../components/DashboardPage/dashboardMedication";
import WeightCard from "../components/DashboardPage/dashboardWeight";
import MoodCard from "../components/DashboardPage/dashboardMood";
import MealCard from "../components/DashboardPage/dashboardMeal";
import ArticleCard from "../components/DashboardPage/dashboardArticle";

function DashboardPage() {
    return (
        <div className="dashboardPage">
            <NavBar />
            <div className="dashboardPage__body">
                <DashboardHeader />
                <div className="dashboardPage__content">
                    <div className="dashboardPage__master">
                        <GlycemiaCard />
                        <ActivityCard />
                        <MedicationCard />
                        <WeightCard />
                    </div>
                    <div className="dashboardPage__option">
                        <MoodCard />
                        <MealCard />
                    </div>
                </div>
                <ArticleCard />
            </div>
        </div>
    )
}
export default DashboardPage;
