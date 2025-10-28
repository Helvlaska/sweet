//import React, {useState} from "react";

// Import des outils
//import {validateField} from "../utils/validator";
//import { formatData } from "../utils/dataFormatter";
//import { Link, useNavigate } from "react-router-dom";

// Import des composants
import NavBar from "../components/DashboardPage/dashboardNavbar";
import GlycemiaCard from "../components/DashboardPage/dashboardGlycemia";

function DashboardPage() {
    return (
        <div>
            <NavBar />
            <div>
                <GlycemiaCard />
            </div>
        </div>
    )

}
export default DashboardPage;
