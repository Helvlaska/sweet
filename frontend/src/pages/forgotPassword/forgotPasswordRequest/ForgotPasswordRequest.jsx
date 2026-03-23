/**
 * SWEET — Forgot Password Request Page (Structure)
 * ================================================
 * Page component representing the password reset request screen.
 *
 * Role:
 * -----
 * - Display the form allowing users
 *   to request a password reset link.
 * - Structure visual elements and related actions.
 * - Delegate all business logic to the useForgotPasswordRequest hook.
 *
 * Content:
 * --------
 * - Email input field.
 * - Conditional display of user-facing error messages.
 * - Submit button to send the request.
 * - Link back to the login page.
 * - Visual illustration related to the "forgot password" context.
 *
 * Interaction:
 * ------------
 * - Events (change, submit) are handled
 *   by the useForgotPasswordRequest hook.
 * - This component contains no validation logic
 *   and no API calls.
 *
 * Architecture:
 * -------------
 * - Business logic is centralized in useForgotPasswordRequest.js.
 * - Navigation is handled via React Router (<Link />).
 * - Button and Icon components come from the SWEET Design System.
 * - Styles are defined in the associated SCSS file.
 *
 * Maintenance:
 * ------------
 * - Any change to the password reset flow must be handled
 *   in the hook or the related service.
 * - Changes in this file must remain strictly structural (JSX).
 * - Visual elements must remain consistent
 *   with the SWEET Design System.
 */


import React from "react";
import { Link } from "react-router-dom";
import { useForgotPasswordRequest } from "./useForgotPasswordRequest";

import imgEyesOpen from "../../../assets/forgotPassword/mascot-eyes-open.webp";
import Button from "../../../components/Button/buttons";
import Icon from "../../../components/Icon/Icons";


function ForgotPasswordRequest() {
  const {
    email,
    errors,
    success,

    handleChange,
    handleSubmit,
  } = useForgotPasswordRequest();

  return (
    <div className="forgotPassword">
      <div className="forgotPassword__container">

        {success ? (
          <div className="forgotPassword__success">
            <div className="forgotPassword__success-icon">
              <Icon
                name="check"
                className="icon-size--xl"
                strokeWidth="4"
              />
            </div>

            <h2 className="forgotPassword__success-title">
              Email envoyé !<br />
              <p className="forgotPassword__success-text">
                Si un compte est associé à cette adresse,<br />
                vous recevrez un email pour réinitialiser votre mot de passe.
              </p>
            </h2>

            <p className="forgotPassword__success-warning">
              Pensez à vérifier vos spams.
            </p>
          </div>

        ) : (
          <form onSubmit={handleSubmit} className="forgotPassword__form">
            <div className="forgotPassword__group">
              <input
                id="email"
                name="email"
                type="email"
                value={email}
                onChange={handleChange}
                placeholder="Adresse mail"
                className="forgotPassword__input"
              />
            </div>

            {errors.length > 0 && (
              <ul className="forgotPassword__errors">
                {errors.map(function (message, index) {
                  return (
                    <li key={index} className="forgotPassword__error">
                      <Icon name="cross" className="forgotPassword__error-icon" />
                      {message}
                    </li>
                  );
                })}
              </ul>
            )}

            <div className="forgotPassword__actions">
              <Button type="submit" className="btn-pill-outline-blue">
                Envoyer
              </Button>
            </div>

            <div className="forgotPassword__cta">
              <p>
                Changé d'avis ?{" "}
                <Link to="/login" className="forgotPassword__link">
                  Connectez-vous
                </Link>
              </p>
            </div>
          </form>
        )}
      </div>

      <div className="forgotPassword__illustration">
        <img
          src={imgEyesOpen}
          alt="Mascotte Sweet en train de demander si vous avez un trou de mémoire"
          className="forgotPassword__mascot"
        />
      </div>
    </div>

  )
}

export default ForgotPasswordRequest
