/**
 * SWEET — Register Welcome Step (Structure)
 * ========================================
 * Component representing the transitional step
 * of the registration process.
 *
 * Role:
 * -----
 * - Introduce the user profile creation phase.
 * - Prepare the user to enter the active registration steps.
 * - Allow the user to start the flow via the "Start" action.
 *
 * Content:
 * --------
 * - User-oriented introductory message.
 * - Primary button triggering the next step.
 * - Secondary call-to-action linking to the login page.
 * - Illustration aligned with the SWEET visual identity.
 *
 * Interaction:
 * ------------
 * - The primary action is passed via the onNext prop.
 * - Navigation to login uses React Router (<Link />).
 * - This component contains no business logic.
 *
 * Architecture:
 * -------------
 * - Flow progression is managed by useRegisterFlow.
 * - Button and Icon components come from the SWEET Design System.
 * - Styles are defined in the associated SCSS file.
 *
 * Maintenance:
 * ------------
 * - This step should remain simple and user-experience oriented.
 * - Any additional logic (analytics, tracking, etc.)
 *   must remain decoupled.
 * - Changes in this file must remain strictly structural (JSX).
 */


import React from "react";
import { Link } from "react-router-dom";

import imgRegisterOpen from "../../../assets/register/mascot-eyes-open.webp";
import Button from "../../../components/Button/buttons";
import Icon from "../../../components/Icon/Icons";


function RegisterWelcome({ onNext }) {
  return (
    <div className="registerWelcome">
      <div className="registerWelcome__wrapper">
        <div className="registerWelcome__content">
          <p className="registerWelcome__text">
            Tout d’abord, <br />
            commençons <br />
            par créer ton profil.
          </p>

          <Button onClick={onNext} className="btn-pill-outline-violet">
            Commencer
            <Icon
              name="chevronRight"
              className="icon--chevron-right"
              strokeWidth="2"
            />
          </Button>

          <div className="registerWelcome__cta">
            Déjà un compte ?

            <Link to="/login" className="registerWelcome__link">
              Connexion ici.
            </Link>
          </div>
        </div>
      </div>

      <div className="registerWelcome__illustration">
        <img
          src={imgRegisterOpen}
          alt="Mascotte Sweet en train de dire enchanté"
          className="registerWelcome__mascot"
        />
      </div>
    </div>
  )
}

export default RegisterWelcome;
