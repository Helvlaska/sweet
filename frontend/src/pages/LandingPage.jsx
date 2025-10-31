import { useNavigate } from "react-router-dom";
import landingImage from "../assets/landing/LandingIllustrationBonjour.png"

function LandingPage() {
    const navigate = useNavigate();

    function handleLoginClick() {
        navigate("/login");
    };

    function handleRegisterClick() {
        navigate("/register");
    };

    return (
        <div className="landing">
            <div className="landing__content">
                <h1 className="landing__title">Sweet</h1>
                <div className="landing__buttons">
                    <button className="landing__btn landing__btn--outline" onClick={handleLoginClick}>Se connecter</button>
                    <button className="landing__btn landing__btn--filled" onClick={handleRegisterClick}>Inscription</button>
                </div>
            </div>
            <img src={landingImage} alt="Illustration d'accueil de l'application Sweet" className="landing__image" />
        </div>
    );
}
export default LandingPage;
