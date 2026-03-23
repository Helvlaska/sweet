/**
 * SWEET — Landing Page (Structure)
 * ================================
 * Page component representing the public landing screen of the SWEET application.
 *
 * Role:
 * -----
 * - Present the application identity (name, visual).
 * - Provide visual entry points to authentication:
 *   - Login
 *   - Register
 *
 * Content:
 * --------
 * - JSX structure only (no business logic).
 * - Action buttons wrapped in React Router <Link /> components.
 * - Static welcome illustration.
 *
 * Navigation:
 * -----------
 * - Routes (/login, /register) are referenced here only
 *   for user navigation purposes.
 * - Redirection rules and route protection
 *   are centralized in AppRouter.jsx.
 *
 * Architecture:
 * -------------
 * - This component contains no redirection logic.
 * - It has no associated business .js file.
 * - Styles are defined exclusively in the folder’s SCSS file.
 *
 * Maintenance:
 * ------------
 * - Any navigation or redirection logic changes
 *   must be handled in AppRouter.jsx.
 * - Changes in this file must remain strictly structural (JSX).
 * - Button components must stay aligned with the SWEET Design System.
 */


import landingImg from "../../assets/landing/mascot-welcome.webp";
import Button from "../../components/Button/buttons";

import { Link } from "react-router-dom";

export default function Landing() {

  return (
    <div className="landing">
      <div className="landing__content">
        <h1 className="landing__title">Sweet</h1>
        <div className="landing__buttons">
          <Link to="/login">
            <Button className="btn-pill-outline-kaki">
              Se connecter
            </Button>
          </Link>
          <Link to="/register">
            <Button className="btn-pill-solid-kaki">
              Inscription
            </Button>
          </Link>
        </div>
      </div>
      <div className="landing__image-wrapper">
        <img
          src={landingImg}
          alt="Illustration d'accueil de l'application Sweet" className="landing__image"
        />
      </div>
    </div>
  );
}
