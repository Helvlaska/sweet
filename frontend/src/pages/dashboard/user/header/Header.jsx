import { useAuth } from "../../../../context/useAuth";

import imgIllus from "../../../../assets/dashboard/header-logo.webp";
import imgBubble from "../../../../assets/dashboard/header-bubble.svg";

function DashboardHeader() {
  const {user} = useAuth();

  const currentDate = new Date().toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <header className="header">
      <div className="header__welcome">
        <img src={imgIllus} alt="Mascotte Sweet" className="welcome__mascot" />

        <div className="welcome__bubble">
          <img src= {imgBubble} alt="Bulle décorative" className="bubble__container"  />

          <div className="bubble__content">
            <h2 className="bubble__greeting">Bonjour {user?.first_name} !</h2>

            <p className="bubble__text">
              Comment vas-tu aujourd’hui ?<br />
              N’oublie pas d’enregistrer tes données !
            </p>
          </div>
        </div>
      </div>

      <div className="header__date">
        <p className="date__text">Aujourd’hui nous sommes le :</p>

        <p className="date__date">{currentDate}</p>
      </div>
    </header>
  );
}

export default DashboardHeader;

