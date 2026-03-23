/**
 * SWEET — Register Auth Step (Structure)
 * ======================================
 * Component representing the credential creation step
 * in the registration process.
 *
 * Role:
 * -----
 * - Display required fields for account creation:
 *   email, username, and password.
 * - Dynamically present availability status
 *   for email and username.
 * - Display password security rules.
 * - Allow navigation between steps (Back / Continue).
 * - Delegate all business logic to the useRegisterAuth hook.
 *
 * Content:
 * --------
 * - Visual progress indicator.
 * - Credentials form.
 * - Field-level validation and error messages.
 * - Dynamic password checklist.
 * - Navigation buttons (Back / Next).
 * - Illustration linked to password visibility state.
 *
 * Interaction:
 * ------------
 * - Events (change, validation, password toggle)
 *   are handled by useRegisterAuth.
 * - Full validation is triggered via handleNext.
 * - Navigation actions are passed via props
 *   (onBack, onNext).
 *
 * Architecture:
 * -------------
 * - Business logic is centralized in useRegisterAuth.js.
 * - Global flow orchestration is handled by useRegisterFlow.
 * - Button and Icon components come from the SWEET Design System.
 * - Styles are defined in the associated SCSS file.
 *
 * Maintenance:
 * ------------
 * - Any update to validation or availability logic
 *   must be handled in useRegisterAuth.
 * - This component must remain purely structural (JSX).
 * - Visual elements must stay aligned
 *   with the SWEET Design System.
 */


import React from "react";
import { useRegisterAuth } from "./useRegisterAuth";

import imgRegisterOpen from "../../../assets/register/mascot-eyes-open.webp";
import imgRegisterClose from "../../../assets/register/mascot-eyes-closed.webp";
import Button from "../../../components/Button/buttons";
import Icon from "../../../components/Icon/Icons";


function RegisterAuth({ onNext, onBack }) {
  const {
    email,
    username,
    password,
    passwordChecklist,
    showPassword,
    consent,
    errors,
    emailStatus,
    usernameStatus,

    handleChange,
    togglePasswordVisibility,
    handleNext,
  } = useRegisterAuth();

  return (
    <div className="registerAuth">
      <div className="registerAuth__wrapper">
        <div className="registerAuth__progress">
          <p className="registerAuth__label">
            Création des identifiants
          </p>

          <div className="registerAuth__bar">
            <span className="registerAuth__page registerAuth__page--active" />
            <span className="registerAuth__page registerAuth__page--inactive" />
            <span className="registerAuth__page registerAuth__page--inactive" />
          </div>
        </div>

        <div className="registerAuth__container">
          <h1 className="registerAuth__title">
            Avec quels identifiants<br />
            voudras-tu te connecter ?
          </h1>

          <form className="registerAuth__form">
            <div className="registerAuth__group">
              <input
                id="email"
                name="email"
                type="email"
                value={email}
                onChange={handleChange}
                placeholder="Adresse mail (Requis)"
                required
                className="registerAuth__input"
              />

              {emailStatus === "unavailable" && (
                <p className="registerAuth__field-error">
                  Adresse email déjà utilisée.
                  <Icon
                    name="cross"
                    strokeWidth="1.5"
                    className="registerAuth__field-icon" />
                </p>
              )}

              {emailStatus === "valid" && (
                <p className="registerAuth__field-success">
                  OK
                  <Icon
                    name="check"
                    strokeWidth="1.5"
                    className="registerAuth__field-icon" />
                </p>
              )}
            </div>

            <div className="registerAuth__group">
              <input
                id="username"
                name="username"
                type="text"
                value={username}
                onChange={handleChange}
                placeholder="Nom d'utilisateur (Requis)"
                className="registerAuth__input"
              />

              {usernameStatus === "unavailable" && (
                <p className="registerAuth__field-error">
                  Nom d'utilisateur déjà utilisé.
                  <Icon
                    name="cross"
                    strokeWidth="1.5"
                    className="registerAuth__field-icon" />
                </p>
              )}

              {usernameStatus === "valid" && (
                <p className="registerAuth__field-success">
                  OK
                  <Icon
                    name="check"
                    strokeWidth="1.5"
                    className="registerAuth__field-icon" />
                </p>
              )}
            </div>

            <div className="registerAuth__group">
              <input
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={handleChange}
                placeholder="Mot de passe (Requis)"
                className="registerAuth__input"
              />

              <Button onClick={togglePasswordVisibility}>
                <Icon
                  name={showPassword ? "eyeOff" : "eye"}
                  className="registerAuth__icon"
                  strokeWidth="1"
                />
              </Button>
            </div>

            <div className="registerAuth__extras">
              <label htmlFor="consent" className="registerAuth__consent">
                <input
                  type="checkbox"
                  id="consent"
                  name="consent"
                  checked={consent}
                  onChange={handleChange}
                  className="registerAuth__checkbox"
                />

                Vous acceptez les Conditions d’utilisation et vous confirmez avoir lu la Politique de confidentialité de Sweet.
              </label>
            </div>
          </form>

          {passwordChecklist && (
            <ul className="registerAuth__checklist">
              Le mot de passe doit au moins contenir:<br/>

              <li
                className={
                  passwordChecklist.hasMinLength
                    ? "registerAuth__checklist-item is-valid"
                    : "registerAuth__checklist-item"
                }
              >
                <Icon
                  name={passwordChecklist.hasMinLength ? "check" : "cross"}
                  className="registerAuth__checklist-icon"
                  strokeWidth="1"
                />
                8 caractères minimum
              </li>

              <li
                className={
                  passwordChecklist.hasUppercase
                    ? "registerAuth__checklist-item is-valid"
                    : "registerAuth__checklist-item"
                }
              >
                <Icon
                  name={passwordChecklist.hasUppercase ? "check" : "cross"}
                  className="registerAuth__checklist-icon"
                  strokeWidth="1"
                />
                Une lettre majuscule (A–Z)
              </li>

              <li
                className={
                  passwordChecklist.hasLowercase
                    ? "registerAuth__checklist-item is-valid"
                    : "registerAuth__checklist-item"
                }
              >
                <Icon
                  name={passwordChecklist.hasLowercase ? "check" : "cross"}
                  className="registerAuth__checklist-icon"
                  strokeWidth="1"
                />
                Une lettre minuscule (a–z)
              </li>

              <li
                className={
                  passwordChecklist.hasNumber
                    ? "registerAuth__checklist-item is-valid"
                    : "registerAuth__checklist-item"
                }
              >
                <Icon
                  name={passwordChecklist.hasNumber ? "check" : "cross"}
                  className="registerAuth__checklist-icon"
                  strokeWidth="1"
                />
                Un chiffre (0–9)
              </li>

              <li
                className={
                  passwordChecklist.hasSpecialChar
                    ? "registerAuth__checklist-item is-valid"
                    : "registerAuth__checklist-item"
                }
              >
                <Icon
                  name={passwordChecklist.hasSpecialChar ? "check" : "cross"}
                  className="registerAuth__checklist-icon"
                  strokeWidth="1"
                />
                Un caractère spécial (@ $ ! % * ? &)
              </li>
            </ul>
          )}

          {errors.length > 0 && (
            <ul className="registerAuth__errors">
              {errors.map(function (message, index) {
                return (
                  <li key={index} className="registerAuth__error">
                    <Icon
                      name="cross"
                      strokeWidth="1.5"
                      className="registerAuth__error-icon"
                    />
                    {message}
                  </li>
                );
              })}
            </ul>
          )}

          <div className="registerAuth__actions">
            <Button onClick={onBack} className="btn-pill-outline-violet">
              <Icon
                name="chevronLeft"
                strokeWidth="2"
                className="icon--chevron-left"
              />
                Retour
            </Button>

            <Button onClick={handleNext.bind(null, onNext)} className="btn-pill-outline-violet">
              Continuer
              <Icon
                name="chevronRight"
                strokeWidth="2"
                className="icon--chevron-right"
              />
            </Button>
          </div>
        </div>
      </div>

      <div className="registerAuth__illustration">
        <img
          src={showPassword ? imgRegisterClose : imgRegisterOpen}
          alt="Mascotte Sweet en train de dire enchanté"
          className="registerAuth__mascot"
        />
      </div>
    </div>
  )
}

export default RegisterAuth;
