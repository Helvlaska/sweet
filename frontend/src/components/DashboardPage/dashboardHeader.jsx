// Import des outils
import { useAuth } from "../../context/AuthContext";

// Import image
import imageIllus from "../../assets/images/05-illustration-board.png"

function DashboardHeader() {
    const {user} = useAuth();
    console.log("Le current user est:", user)

    const currentDate = new Date().toLocaleDateString("fr-FR", {
        weekday: "long",
        day: "numeric",
        month: "long",
    });

    return (
        <header className="header-dashboard">
            <div className="bubble-container">
                <img src={imageIllus}></img>
                <div className="bubble">
                    <p className="bubble-greeting">Bonjour {user?.first_name}</p>
                    <p>Comment vas-tu aujourd’hui ?</p>
                    <p>N’oublie pas d’enregistrer tes données !</p>
                </div>
                <p className="bubble-date">Nous sommes le {currentDate}</p>
            </div>
        </header>
    )

}

export default DashboardHeader

