import { useNavigate } from "react-router-dom";


export default function LandingPage() {
  // Hook de navigation React Router
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate("/login");
  };

  const handleRegisterClick = () => {
    navigate("/register");
  };

  return (
    <div className="landing">
      <h1 className="landing__title">Sweet</h1>
      <div className="landing__buttons">
        <button className="landing__btn landing__btn--outline" onClick={handleLoginClick}>
          Se connecter
        </button>
        <button className="landing__btn landing__btn--filled" onClick={handleRegisterClick}>
          Inscription
        </button>
      </div>
    </div>
  );
}
