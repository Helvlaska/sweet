import { Link } from "react-router-dom";

import Button from "../../components/Button/buttons";
import Icon from "../../components/Icon/Icons";
import img from "../../assets/dashboard/popup-mood.webp";

function NotFound(){

  return (
    <section className="notFound">
      <div className="notFound__content">
        <div className="notFound__fail-icon">
          <Icon
            name="cross"
            className="icon-size--xl"
            strokeWidth="4"
          />
        </div>

        <h1 className="notFound__title">
          Oups ! <br/>Cette page semble introuvable.
        </h1>

        <Link to="/dashboard">
          <Button className="btn-pill-outline-brown">
            Retour au tableau de bord

            <Icon
              name="chevronRight"
              strokeWidth="2"
            />
          </Button>
        </Link>
      </div>

      <img
        src={img}
        alt="image d'illustration de la page not found"
        className="notFound__img"
      />
    </section>
  )
}

export default NotFound;
