/**
 * SWEET — Reset Password Page (Structure)
 * ======================================
 * Page component representing the user password reset screen.
 *
 * Role:
 * -----
 * - Display the form to define a new password.
 * - Dynamically present password security rules.
 * - Display a confirmation screen upon success.
 * - Delegate all business logic to the useResetPassword hook.
 *
 * Content:
 * --------
 * - New password input field with conditional visibility.
 * - Dynamic checklist of password security rules.
 * - Password confirmation input field.
 * - Conditional display of user-facing error messages.
 * - Success screen with a call-to-action leading to login.
 * - Visual illustration related to the "reset password" flow.
 *
 * Interaction:
 * ------------
 * - The reset token is retrieved from the URL via useParams.
 * - Events (change, submit, password toggle)
 *   are handled by the useResetPassword hook.
 * - This component contains no validation logic
 *   and no API calls.
 *
 * Architecture:
 * -------------
 * - Business logic is centralized in useResetPassword.js.
 * - Navigation is handled via React Router (<Link />).
 * - Button and Icon components come from the SWEET Design System.
 * - Styles are defined in the associated SCSS file.
 *
 * Maintenance:
 * ------------
 * - Any change to password rules or the reset flow
 *   must be handled in the useResetPassword hook.
 * - Changes in this file must remain strictly structural (JSX).
 * - Visual elements must remain consistent
 *   with the SWEET Design System.
 */


import React from "react";
import { Link } from "react-router-dom";
import { useParams } from "react-router-dom";
import { useResetPassword } from "./useResetPassword";

import imgForgotPassword from "../../../assets/login/mascot-password-forgotten.webp";
import Button from "../../../components/Button/buttons";
import Icon from "../../../components/Icon/Icons";

function ResetPassword() {
  const { token } = useParams();

  const {
    password,
    passwordChecklist,
    confirmPassword,
    showPassword,
    errors,
    success,

    togglePasswordVisibility,
    handleChange,
    handleSubmit,
  } = useResetPassword(token);

  return (
    <div className="resetPassword">
      <div className="resetPassword__container">

        {success ? (
          <div className="resetPassword__success">
            <div className="resetPassword__success-icon">
              <Icon
                name="check"
                className="icon-size--xl"
                strokeWidth="4"
              />
            </div>

            <h2 className="resetPassword__success-title">
              Mot de passe mis à jour
              <p className="resetPassword__success-text">
                Votre mot de passe a été modifié avec succès.<br />
                Vous pouvez maintenant vous connecter avec vos nouveaux identifiants.
              </p>
            </h2>

            <Button className="btn-pill-outline-blue">
              <Link to="/login" className="resetPassword__success-link">
                Se connecter
              </Link>
            </Button>
          </div>

        ) : (

          <form onSubmit={handleSubmit} className="resetPassword__form">
            <div className="resetPassword__group">
              <input
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={handleChange}
                placeholder="Nouveau mot de passe"
                className="resetPassword__input"
              />
              <Button>
                <Icon
                  name={showPassword ? "eyeOff" : "eye"}
                  className="resetPassword__icon"
                  strokeWidth="1"
                  onClick={togglePasswordVisibility}
                />
              </Button>
            </div>

            {passwordChecklist && (
              <ul className="resetPassword__checklist">
                Le mot de passe doit au moins contenir:<br/>
                <li
                  className={
                    passwordChecklist.hasMinLength
                      ? "resetPassword__checklist-item is-valid"
                      : "resetPassword__checklist-item"
                  }
                >
                  <Icon
                    name={passwordChecklist.hasMinLength ? "check" : "cross"}
                    className="resetPassword__checklist-icon"
                    strokeWidth="1"
                  />
                  8 caractères minimum
                </li>

                <li
                  className={
                    passwordChecklist.hasUppercase
                      ? "resetPassword__checklist-item is-valid"
                      : "resetPassword__checklist-item"
                  }
                >
                  <Icon
                    name={passwordChecklist.hasUppercase ? "check" : "cross"}
                    className="resetPassword__checklist-icon"
                    strokeWidth="1"
                  />
                  Une lettre majuscule (A–Z)
                </li>

                <li
                  className={
                    passwordChecklist.hasLowercase
                      ? "resetPassword__checklist-item is-valid"
                      : "resetPassword__checklist-item"
                  }
                >
                  <Icon
                    name={passwordChecklist.hasLowercase ? "check" : "cross"}
                    className="resetPassword__checklist-icon"
                    strokeWidth="1"
                  />
                  Une lettre minuscule (a–z)
                </li>

                <li
                  className={
                    passwordChecklist.hasNumber
                      ? "resetPassword__checklist-item is-valid"
                      : "resetPassword__checklist-item"
                  }
                >
                  <Icon
                    name={passwordChecklist.hasNumber ? "check" : "cross"}
                    className="resetPassword__checklist-icon"
                    strokeWidth="1"
                  />
                  Un chiffre (0–9)
                </li>

                <li
                  className={
                    passwordChecklist.hasSpecialChar
                      ? "resetPassword__checklist-item is-valid"
                      : "resetPassword__checklist-item"
                  }
                >
                  <Icon
                    name={passwordChecklist.hasSpecialChar ? "check" : "cross"}
                    className="resetPassword__checklist-icon"
                    strokeWidth="1"
                  />
                  Un caractère spécial (@ $ ! % * ? &)
                </li>
              </ul>
            )}

            <div className="resetPassword__group">
              <input
                id="confirmPassword"
                name="confirmPassword"
                type={showPassword ? "text" : "password"}
                value={confirmPassword}
                onChange={handleChange}
                placeholder="Confirmer le nouveau mot de passe"
                className="resetPassword__input"
              />
            </div>

            {errors.length > 0 && (
              <ul className="resetPassword__errors">
                {errors.map(function (message, index) {
                  return (
                    <li key={index} className="resetPassword__error">
                      <Icon name="cross" className="resetPassword__error-icon" />
                      {message}
                    </li>
                  );
                })}
              </ul>
            )}

            <div className="resetPassword__actions">
              <Button type="submit" className="btn-pill-outline-blue">
                Réinitialiser le mot de passe
              </Button>
            </div>
          </form>
        )}
      </div>

      <div className="resetPassword__illustration">
        <img
          src={imgForgotPassword}
          alt="Mascotte Sweet en train de demander si vous avez un trou de mémoire"
          className="resetPassword__mascot"
        />
      </div>
    </div>
  )
}

export default ResetPassword;
