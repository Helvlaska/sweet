/**
 * SWEET — RegisterProfile Component
 * ==================================
 * Profile creation step of the multi-step registration flow.
 *
 * Role:
 * -----
 * - Render the profile information form.
 * - Allow profile picture upload with preview.
 * - Display validation errors.
 * - Handle navigation between steps.
 *
 * Structure:
 * ----------
 * - Progress indicator (step visualization bar).
 * - Profile picture upload section with preview.
 * - Personal information fields:
 *     • first name
 *     • last name
 *     • height
 *     • city
 *     • date of birth (optional)
 *     • gender (custom SelectedField component)
 * - Error display section.
 * - Navigation buttons (Back / Continue).
 * - Illustration panel (desktop only).
 *
 * Behavior:
 * ---------
 * - All business logic is delegated to useRegisterProfile.
 * - Validation errors are displayed conditionally.
 * - Continue button triggers handleNext(onNext).
 * - Back button triggers onBack callback.
 *
 * Architecture:
 * -------------
 * - Pure presentation component.
 * - Business logic is isolated in useRegisterProfile.
 * - Uses shared design system components:
 *     • Button
 *     • Icon
 *     • SelectedField
 * - Integrates into the flow orchestrated by RegisterFlow.
 *
 * Maintenance:
 * ------------
 * - Do not move validation logic into this file.
 * - Any layout modification must remain scoped
 *   to registerProfile styles.
 * - Any new profile field must be reflected
 *   in both the hook and the payload builder.
 */


import React from "react";
import { useRegisterProfile } from "./useRegisterProfile";

import imgRegisterOpen from "../../../assets/register/mascot-eyes-open.webp";
import Button from "../../../components/Button/buttons";
import Icon from "../../../components/Icon/Icons";
import SelectedField from "../../../components/Form/SelectedField/SelectedField";


function RegisterProfile({ onNext, onBack }) {
  const {
    firstName,
    lastName,
    gender,
    height,
    city,
    dateOfBirth,
    errors,
    preview,

    handleChange,
    handleFileChange,
    handleNext,
  } = useRegisterProfile();

  return (
    <div className="registerProfile">
      <div className="registerProfile__wrapper">
        <div className="registerProfile__progress">
          <p className="registerProfile__label">
            Création du profil
          </p>

          <div className="registerProfile__bar">
            <span className="registerProfile__page registerProfile__page--inactive" />
            <span className="registerProfile__page registerProfile__page--active" />
            <span className="registerProfile__page registerProfile__page--inactive" />
          </div>
        </div>

        <form className="registerProfile__form">
          <div className="registerProfile__upload">
            <input
              id="profile_picture"
              name="profile_picture"
              type="file"
              onChange={handleFileChange}
              accept="image/"
              className="registerProfile__input"
            />

            <label
              htmlFor="profile_picture"
              className="registerProfile__label"
            >
              <div className="registerProfile__circle">
                {preview ? (
                  <img
                    src={preview}
                    alt="Aperçu de la photo de profile."
                    className="registerProfile__preview"
                  />
                ) : (
                  <span className="registerProfile__text">
                    Ajoute<br />
                    une photo<br />
                    de profil
                  </span>
                )}

                <Button className="registerProfile__btn btn-round-grey">
                  <Icon
                    name="plus"
                    strokeWidth="3"
                    className="registerProfile__icon"
                  />
                </Button>
              </div>
            </label>
          </div>

          <div className="registerProfile__fields">
            <div className="registerProfile__fields-full">
              <div className="registerProfile__group">
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  value={firstName}
                  placeholder="Prénom (Requis)"
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="registerProfile__group">
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  value={lastName}
                  placeholder="Nom (Requis)"
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="registerProfile__fields-split">
              <div className="registerProfile__group">
                <input
                  id="height"
                  name="height"
                  type="number"
                  value={height}
                  placeholder="Taille (cm) (Requis)"
                  onChange={handleChange}
                  className="registerProfile__group-number"
                  required
                />
              </div>

              <div className="registerProfile__group">
                <input
                  id="city"
                  name="city"
                  type="text"
                  value={city}
                  placeholder="Ville (Requis)"
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="registerProfile__fields-split">
              <div className="registerProfile__group">
                <input
                  id="date_of_birth"
                  name="date_of_birth"
                  type="date"
                  value={dateOfBirth}
                  placeholder="Date de Naissance"
                  onChange={handleChange}
                />
              </div>

              <div className="registerProfile__group-select">
                <SelectedField
                  name="gender"
                  placeholder="Genre (Requis)"
                  value={gender}
                  onChange={handleChange}
                  required
                  options={[
                    { value: "male", label: "Homme" },
                    { value: "female", label: "Femme" },
                    { value: "other", label: "Autre" },
                    { value: "prefer_not_say", label: "Ne pas préciser" },
                  ]}
                />
              </div>
            </div>
          </div>

          {errors.length > 0 && (
            <ul className="registerProfile__errors">
              {errors.map(function (message, index) {
                return (
                  <li key={index} className="registerProfile__error">
                    <Icon
                      name="cross"
                      className="registerProfile__error-icon"
                    />
                    {message}
                  </li>
                );
              })}
            </ul>
          )}

          <div className="registerProfile__actions">
            <Button
              onClick={onBack}
              className="btn-pill-outline-violet"
            >
              <Icon
                name="chevronLeft"
                strokeWidth="2"
                className="icon--chevron-left"
              />
              Retour
            </Button>

            <Button
              onClick={handleNext.bind(null, onNext)}
              className="btn-pill-outline-violet"
            >
              Continuer
              <Icon
                name="chevronRight"
                strokeWidth="2"
                className="icon--chevron-right"
              />
            </Button>
          </div>
        </form>
      </div>

      <div className="registerProfile__illustration">
        <img
          src={imgRegisterOpen}
          alt="Mascotte Sweet en train de dire enchanté"
          className="registerProfile__mascot"
        />
      </div>
    </div>
  )
}

export default RegisterProfile;
