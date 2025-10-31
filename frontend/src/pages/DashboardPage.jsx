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
import WeightCard from "../components/DashboardPage/dashboardWeight";
import MoodCard from "../components/DashboardPage/dashboardMood";
import MealCard from "../components/DashboardPage/dashboardMeal";

function DashboardPage() {
    return (
        <div>
            <NavBar />
            <div>
                <DashboardHeader />
                <div>
                    <GlycemiaCard />
                    <ActivityCard />
                    <MoodCard />
                    <MealCard />
                    <WeightCard />
                </div>
            </div>
        </div>
    )

}
export default DashboardPage;
