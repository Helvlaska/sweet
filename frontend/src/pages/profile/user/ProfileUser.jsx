import { useProfileUser } from "./useProfileUser";
import { useProfileAuth } from "./useProfileAuth";
import { useProfilePassword } from "./useProfilePassword";
import { useAuth } from "../../../context/useAuth";

import defaultPicture from "../../../assets/profile/default_profile_picture.webp";
import Button from "../../../components/Button/buttons";
import Icon from "../../../components/Icon/Icons";
import SelectedField from "../../../components/Form/SelectedField/SelectedField";


function ProfileUser({ goToMedication }) {
  const { user } = useAuth();

  const {
    firstName,
    lastName,
    gender,
    height,
    city,
    dateOfBirth,
    errors: errorsUser,
    preview,
    handleChange: handleChangeUser,
    handleFileChange,
    handleSubmit: handleSubmitUser,
  } = useProfileUser();

  const {
    email,
    username,
    errors: errorsAuth,
    emailStatus,
    usernameStatus,
    handleChange: handleChangeAuth,
    handleSubmit: handleSubmitAuth,
  } = useProfileAuth();

  const {
    password,
    passwordChecklist,
    showPassword,
    errors: errorsPassword,
    handleChange: handleChangePassword,
    togglePasswordVisibility,
    handleSubmit: handleSubmitPassword,
  } = useProfilePassword();


  return (
    <section className="profile">
      <div className="profile__picture">
        <input
          id="profilePicture"
          name="profilePicture"
          type="file"
          className="picture__input"
          accept="image/*"
          onChange={handleFileChange}
        />

        <div className="picture__wrapper">
          <label htmlFor="profilePicture" className="picture__label">
            <img
              src={preview || user.profile_picture || defaultPicture}
              className="picture__img"
            />
          </label>

          <Button
            onClick={preview ? handleSubmitUser : function() { document.getElementById("profilePicture").click() }}
            className="btn-round--kaki picture__btn"
          >
            <Icon
              name={preview ? "check" : "pen"}
              strokeWidth="1"
              size={20}
            />
          </Button>
        </div>
      </div>

      <p className="profile__username">
        {user.username}
      </p>

      <div className="profile__actions">
        <Button
          className="btn-pill-solid--orange"
        >
          Informations personnelles
        </Button>

        <Button
          onClick={goToMedication}
          className="btn-pill-solid--orange"
        >
          Médications et posologies
        </Button>
      </div>

      <div className="profile__form--user">
        <div className="profile__group">
          <input
            id="first_name"
            name="first_name"
            type="text"
            value={firstName}
            placeholder="Prénom (Requis)"
            onChange={handleChangeUser}
          />
        </div>

        <div className="profile__group">
          <input
            id="last_name"
            name="last_name"
            type="text"
            value={lastName}
            placeholder="Nom (Requis)"
            onChange={handleChangeUser}
          />
        </div>

        <div className="profile__group">
          <input
            id="height"
            name="height"
            type="number"
            value={height}
            placeholder="Taille (cm) (Requis)"
            onChange={handleChangeUser}
            className="profile__group-number"
          />
        </div>

        <div className="profile__group">
          <input
            id="city"
            name="city"
            type="text"
            value={city}
            placeholder="Ville (Requis)"
            onChange={handleChangeUser}
          />
        </div>

        <div className="profile__group">
          <input
            id="date_of_birth"
            name="date_of_birth"
            type="date"
            value={dateOfBirth}
            placeholder="Date de Naissance"
            onChange={handleChangeUser}
          />
        </div>

        <div className="profile__group--select">
          <SelectedField
            name="gender"
            placeholder="Genre (Requis)"
            value={gender}
            onChange={handleChangeUser}
            className="selectedField--profile-page"
            options={[
              { value: "male", label: "Homme" },
              { value: "female", label: "Femme" },
              { value: "other", label: "Autre" },
              { value: "prefer_not_say", label: "Ne pas préciser" },
            ]}
          />
        </div>

        {errorsUser.length > 0 && (
          <ul className="profile__errors">
            {errorsUser.map(function (message, index) {
              return (
                <li key={index} className="profile__error">
                  <Icon
                    name="cross"
                    className="profile__error-icon"
                  />

                  {message}
                </li>
              );
            })}
          </ul>
        )}

        <div className="form__user--btn">
          <Button
            onClick={handleSubmitUser}
            className="btn-pill-outline-violet"
          >
            Modifier
          </Button>
        </div>
      </div>

      <div className="profile__form--auth">
        <div className="profile__group">
          <div className="profile__group--input">
            <input
              id="email"
              name="email"
              type="email"
              value={email}
              onChange={handleChangeAuth}
              placeholder="Adresse mail (Requis)"
              className="profile__input"
            />

            {emailStatus === "unavailable" && (
              <p className="profile__field-error">
                Adresse email déjà utilisée.

                <Icon
                  name="cross"
                  strokeWidth="1.5"
                  className="profile__field-icon"
                />
              </p>
            )}

            {emailStatus === "valid" && (
              <p className="profile__field-success">
                OK

                <Icon
                  name="check"
                  strokeWidth="1.5"
                  className="profile__field-icon"
                />
              </p>
            )}
          </div>

          <Button
            onClick={handleSubmitAuth}
            className="btn-pill-outline-violet"
          >
            Changer mon email
          </Button>
        </div>

        <div className="profile__group">
          <div className="profile__group--input">
            <input
              id="username"
              name="username"
              type="text"
              value={username}
              onChange={handleChangeAuth}
              placeholder="Nom d'utilisateur (Requis)"
              className="profile__input"
            />

            {usernameStatus === "unavailable" && (
              <p className="profile__field-error">
                Nom d'utilisateur déjà utilisé.

                <Icon
                  name="cross"
                  strokeWidth="1.5"
                  className="profile__field-icon"
                />
              </p>
            )}

            {usernameStatus === "valid" && (
              <p className="profile__field-success">
                OK

                <Icon
                  name="check"
                  strokeWidth="1.5"
                  className="profile__field-icon"
                />
              </p>
            )}
          </div>

          <Button
            onClick={handleSubmitAuth}
            className="btn-pill-outline-violet"
          >
            Changer mon pseudo
          </Button>
        </div>

        <div className="profile__group">
          <div className="profile__groupe--password">
            <div className="profile__group--input">
                <input
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={handleChangePassword}
                placeholder="Mot de passe (Requis)"
                className="profile__input"
                />

                <Button onClick={togglePasswordVisibility}>
                <Icon
                    name={showPassword ? "eyeOff" : "eye"}
                    className="profile__icon"
                    strokeWidth="1"
                />
                </Button>
            </div>

            {passwordChecklist && (
                <ul className="profile__checklist">
                Le mot de passe doit au moins contenir:<br/>

                <li
                    className={
                    passwordChecklist.hasMinLength
                        ? "profile__checklist-item is-valid"
                        : "profile__checklist-item"
                    }
                >
                    <Icon
                    name={passwordChecklist.hasMinLength ? "check" : "cross"}
                    className="profile__checklist-icon"
                    strokeWidth="1"
                    />
                    8 caractères minimum
                </li>

                <li
                    className={
                    passwordChecklist.hasUppercase
                        ? "profile__checklist-item is-valid"
                        : "profile__checklist-item"
                    }
                >
                    <Icon
                    name={passwordChecklist.hasUppercase ? "check" : "cross"}
                    className="profile__checklist-icon"
                    strokeWidth="1"
                    />
                    Une lettre majuscule (A–Z)
                </li>

                <li
                    className={
                    passwordChecklist.hasLowercase
                        ? "profile__checklist-item is-valid"
                        : "profile__checklist-item"
                    }
                >
                    <Icon
                    name={passwordChecklist.hasLowercase ? "check" : "cross"}
                    className="profile__checklist-icon"
                    strokeWidth="1"
                    />
                    Une lettre minuscule (a–z)
                </li>

                <li
                    className={
                    passwordChecklist.hasNumber
                        ? "profile__checklist-item is-valid"
                        : "profile__checklist-item"
                    }
                >
                    <Icon
                    name={passwordChecklist.hasNumber ? "check" : "cross"}
                    className="profile__checklist-icon"
                    strokeWidth="1"
                    />
                    Un chiffre (0–9)
                </li>

                <li
                    className={
                    passwordChecklist.hasSpecialChar
                        ? "profile__checklist-item is-valid"
                        : "profile__checklist-item"
                    }
                >
                    <Icon
                    name={passwordChecklist.hasSpecialChar ? "check" : "cross"}
                    className="profile__checklist-icon"
                    strokeWidth="1"
                    />
                    Un caractère spécial (@ $ ! % * ? &)
                </li>
                </ul>
            )}
          </div>

          <Button
            onClick={handleSubmitPassword}
            className="btn-pill-outline-violet--password"
          >
            Changer mon mot de passe
          </Button>

          {errorsAuth.length > 0 && (
            <ul className="profile__errors">
              {errorsAuth.map(function (message, index) {
                return (
                  <li key={index} className="profile__error">
                    <Icon
                      name="cross"
                      strokeWidth="1.5"
                      className="profile__error-icon"
                    />
                    {message}
                  </li>
                );
              })}
            </ul>
          )}

          {errorsPassword.length > 0 && (
            <ul className="profile__errors">
              {errorsPassword.map(function (message, index) {
                return (
                  <li key={index} className="profile__error">
                    <Icon
                      name="cross"
                      strokeWidth="1.5"
                      className="profile__error-icon"
                    />
                    {message}
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      </div>
    </section>
  )
}

export default ProfileUser;
