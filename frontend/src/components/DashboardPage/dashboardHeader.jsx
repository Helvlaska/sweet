// Import des outils
import { useAuth } from "../../context/AuthContext";

// import des images et des icones
import imageIllus from "../../assets/dashboard/page/DashboardIllustrationLogo.png"
import imageBubble from "../../assets/dashboard/page/DashboardBulle.svg";

function DashboardHeader() {
    const {user} = useAuth();
    console.log("Le current user est:", user)

    const currentDate = new Date().toLocaleDateString("fr-FR", {
        day: "numeric",
        month: "long",
        year: "numeric",
    });

    return (
        <header className="header-dashboard">
            <div className="header-dashboard__left">
                <img src={imageIllus} alt="Mascotte Sweet" className="header-dashboard__illustration" />
                <div className="header-dashboard__bubble">
                    <img src= {imageBubble} alt="Bulle décorative" className="header-dashboard__bubble-img"  />
                    <div className="header-dashboard__bubble-content">
                        <h2 className="header-dashboard__greeting">Bonjour {user?.first_name} !</h2>
                        <p className="header-dashboard__text">
                            Comment vas-tu aujourd’hui ?<br />
                            N’oublie pas d’enregistrer tes données !
                        </p>
                    </div>
                </div>
            </div>
            <div className="header-dashboard__right">
                <p className="header-dashboard__date-title">Aujourd’hui nous sommes le :</p>
                <p className="header-dashboard__date">{currentDate}</p>
            </div>
        </header>
    );
}

export default DashboardHeader

