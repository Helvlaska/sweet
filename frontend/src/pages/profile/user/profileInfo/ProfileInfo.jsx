import { useProfileInfo } from "./useProfileInfo";
import { useAuth } from "../../../../context/useAuth";
import { translateGender } from "../../../../utils/translateEnum/translateGender";

import defaultPicture from "../../../../assets/profile/default_profile_picture.webp";
import Button from "../../../../components/Button/buttons";
import Icon from "../../../../components/Icon/Icons";
import SelectedField from "../../../../components/Form/SelectedField/SelectedField";


function ProfileInfo() {
  const { user } = useAuth();

  const {
    firstName,
    lastName,
    gender,
    height,
    city,
    dateOfBirth,
    errors,
    preview,
    isEditing,
    editing,
    cancelEditing,
    handleChange,
    handleFileChange,
    handleSubmit,
  } = useProfileInfo();

  return (
    <section className="profileInfo">
      <div className="profileInfo__avatar">
        <input
          id="profilePicture"
          name="profilePicture"
          type="file"
          className="profileInfo__avatar-input"
          accept="image/*"
          onChange={handleFileChange}
        />

        <div className="profileInfo__avatar-wrapper">
          <label htmlFor="profilePicture" className="profileInfo__avatar-label">
            <img
              src={preview || user.profile_picture || defaultPicture}
              className="profileInfo__avatar-img"
            />
          </label>

          <Button
            onClick={preview ? handleSubmit : function() { document.getElementById("profilePicture").click() }}
            className="btn-round--kaki profileInfo__avatar-btn"
          >
            <Icon
              name={preview ? "check" : "pen"}
              strokeWidth="1"
              size={20}
            />
          </Button>
        </div>
      </div>

      {isEditing ? (
        <div className="profileInfo__edit">
          <div className="profileInfo__edit-header">
            <div className="profileInfo__edit-required">
              <p className="profileInfo__edit-star">*</p>
              <p className="profileInfo__edit-text"> Champs requis</p>
            </div>

            <div className="profileInfo__edit-actions">
              <Button
                onClick={cancelEditing}
                className="btn-round--kaki profileInfo__avatar-btn"
              >
                <Icon
                  name="cross"
                  strokeWidth="1"
                  size={20}
                />
              </Button>

              <Button
                onClick={handleSubmit}
                className="btn-round--kaki profileInfo__avatar-btn"
              >
                <Icon
                  name="check"
                  strokeWidth="1"
                  size={20}
                />
              </Button>
            </div>
          </div>

          <div className="profileInfo__form">
            <div className="profileInfo__form-row">
              <div className="profileInfo__form-group">
                <label htmlFor="first_name" className="profileInfo__label">
                  Prénom
                  <span className="profileInfo__label-required">*</span>
                </label>

                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  value={firstName}
                  placeholder="Prénom"
                  className="profileInfo__form-label"
                  onChange={handleChange}
                />
              </div>

              <div className="profileInfo__form-group">
                <label htmlFor="last_name" className="profileInfo__label">
                  Nom
                  <span className="profileInfo__label-required">*</span>
                </label>

                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  value={lastName}
                  placeholder="Nom"
                  className="profileInfo__form-label"
                  onChange={handleChange}
                />
              </div>

              <div className="profileInfo__form-group">
                <label htmlFor="height" className="profileInfo__label">
                  Taille (cm)
                  <span className="profileInfo__label-required">*</span>
                </label>

                <input
                  id="height"
                  name="height"
                  type="number"
                  value={height}
                  placeholder="Taille (cm)"
                  className="profileInfo__form-label"
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="profileInfo__form-row">
              <div className="profileInfo__form-group">
                <label htmlFor="city" className="profileInfo__label">
                  Ville
                  <span className="profileInfo__label-required">*</span>
                </label>

                <input
                  id="city"
                  name="city"
                  type="text"
                  value={city}
                  placeholder="Ville"
                  className="profileInfo__form-label"
                  onChange={handleChange}
                />
              </div>

              <div className="profileInfo__form-group">
                <label htmlFor="date_of_birth" className="profileInfo__label">
                  Date de naissance
                </label>

                <input
                  id="date_of_birth"
                  name="date_of_birth"
                  type="date"
                  value={dateOfBirth}
                  placeholder="Date de Naissance"
                  className="profileInfo__form-label"
                  onChange={handleChange}
                />
              </div>

              <div className="profileInfo__form-group">
                <label htmlFor="gender" className="profileInfo__label">
                  Genre
                  <span className="profileInfo__label-required">*</span>
                </label>

                <SelectedField
                  name="gender"
                  placeholder="Genre"
                  value={gender}
                  onChange={handleChange}
                  className="selectedField--profile-page"
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
            <ul className="profileInfo__errors">
              {errors.map(function (message, index) {
                return (
                  <li key={index} className="profileInfo__error">
                    <Icon
                      name="cross"
                      className="profileInfo__error-icon"
                    />

                    {message}
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      ) : (
        <div className="profileInfo__read">
          <div className="profileInfo__read-header">
            <Button
              onClick={editing}
              className="btn-round--kaki profileInfo__read-edit-btn"
            >
              <Icon
                name="pen"
                strokeWidth="1"
                size={20}
              />
            </Button>
          </div>

          <div className="profileInfo__read-content">
            <div className="profileInfo__read-row">
              <p className="profileInfo__read-value">{firstName}</p>
              <p className="profileInfo__read-value">{lastName}</p>
              <p className="profileInfo__read-value">{height} cm</p>
            </div>

            <div className="profileInfo__read-row">
              <p className="profileInfo__read-value">{city}</p>
              <p className="profileInfo__read-value">{dateOfBirth}</p>
              <p className="profileInfo__read-value">{translateGender(gender)}</p>
            </div>
          </div>
        </div>
      )}
    </section>
  )
}

export default ProfileInfo;
