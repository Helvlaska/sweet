import { useNavigate } from "react-router-dom";

// import des images et des icones
import IllusPage from "../assets/dashboard/page/DashboardPopUpIllustrationHumeur.png";

function NotFoundPage(){
    const navigate = useNavigate();

    return (
        <div className="NotFound-page">
            <section className="error-page">
                <h1 className="error-code">404 :(</h1>
                <p className="error-message">Oups ! Cette page semble introuvable.</p>
                <button className="error-button" onClick={() => navigate("/dashboard")}>
                    Retour au dashboard
                </button>
            </section>
            <img src={IllusPage} />
        </div>
    )
}
export default NotFoundPage
