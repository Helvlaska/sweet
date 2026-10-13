import { useProfilePassword } from "./useProfilePassword";

import Button from "../../../../components/Button/buttons";
import Icon from "../../../../components/Icon/Icons";


function ProfilePassword() {
  const {
    password,
    passwordChecklist,
    showPassword,
    isEditing,
    errors,
    editing,
    cancelEditing,
    handleChange,
    togglePasswordVisibility,
    handleSubmit,
  } = useProfilePassword();

  return (
    <div className="profilePassword">
      {isEditing ? (
        <div className="profilePassword__edit">
          <div className="profilePassword__edit-actions">
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

          <div className="profilePassword__form">
            <div className="profilePassword__input-wrapper">
              <input
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={handleChange}
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

            <ul className="profilePassword__checklist">
              Le mot de passe doit au moins contenir :<br />

              <li
                className={
                  passwordChecklist.hasMinLength
                    ? "profilePassword__checklist-item is-valid"
                    : "profilePassword__checklist-item"
                }
              >
                <Icon
                  name={passwordChecklist.hasMinLength ? "check" : "cross"}
                  className="profilePassword__checklist-icon"
                  strokeWidth="1"
                />
                8 caractères minimum
              </li>

              <li
                className={
                  passwordChecklist.hasUppercase
                    ? "profilePassword__checklist-item is-valid"
                    : "profilePassword__checklist-item"
                }
              >
                <Icon
                  name={passwordChecklist.hasUppercase ? "check" : "cross"}
                  className="profilePassword__checklist-icon"
                  strokeWidth="1"
                />
                Une lettre majuscule (A–Z)
              </li>

              <li
                className={
                  passwordChecklist.hasLowercase
                    ? "profilePassword__checklist-item is-valid"
                    : "profilePassword__checklist-item"
                }
              >
                <Icon
                  name={passwordChecklist.hasLowercase ? "check" : "cross"}
                  className="profilePassword__checklist-icon"
                  strokeWidth="1"
                />
                Une lettre minuscule (a–z)
              </li>

              <li
                className={
                  passwordChecklist.hasNumber
                    ? "profilePassword__checklist-item is-valid"
                    : "profilePassword__checklist-item"
                }
              >
                <Icon
                  name={passwordChecklist.hasNumber ? "check" : "cross"}
                  className="profilePassword__checklist-icon"
                  strokeWidth="1"
                />
                Un chiffre (0–9)
              </li>

              <li
                className={
                  passwordChecklist.hasSpecialChar
                    ? "profilePassword__checklist-item is-valid"
                    : "profilePassword__checklist-item"
                }
              >
                <Icon
                  name={passwordChecklist.hasSpecialChar ? "check" : "cross"}
                  className="profilePassword__checklist-icon"
                  strokeWidth="1"
                />
                Un caractère spécial (@ $ ! % * ? &)
              </li>
            </ul>
          </div>

          {errors.length > 0 && (
            <ul className="profilePassword__errors">
              {errors.map(function (message, index) {
                return (
                  <li key={index} className="profilePassword__error">
                    <Icon
                      name="cross"
                      strokeWidth="1.5"
                      className="profilePassword__error-icon"
                    />

                    {message}
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      ) : (
        <div className="profilePassword__read">
          <p className="profilePassword__read-value">
            ••••••••
          </p>

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
      )}
    </div>
  )
}

export default ProfilePassword;
