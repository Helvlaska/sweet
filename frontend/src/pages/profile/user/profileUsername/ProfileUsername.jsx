import { useProfileUsername } from "./useProfileUsername";

import Button from "../../../../components/Button/buttons";
import Icon from "../../../../components/Icon/Icons";


function ProfileUsername() {
  const {
    username,
    errors,
    usernameStatus,
    isEditing,
    editing,
    cancelEditing,
    handleChange,
    handleSubmit,
  } = useProfileUsername();

  return (
    <div className="profileUsername">
      {isEditing ? (
        <div className="profileUsername__edit">
          <div className="profileUsername__edit-actions">
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

          <div className="profileUsername__form">
            <input
              id="username"
              name="username"
              type="text"
              value={username}
              onChange={handleChange}
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

          {errors.length > 0 && (
            <ul className="profileUsername__errors">
              {errors.map(function (message, index) {
                return (
                  <li key={index} className="profileUsername__error">
                    <Icon
                      name="cross"
                      className="profileUsername__error-icon"
                    />

                    {message}
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      ) : (
        <div className="profileUsername__read">
          <p className="profileUsername__read-value">
            {username}
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

export default ProfileUsername;
