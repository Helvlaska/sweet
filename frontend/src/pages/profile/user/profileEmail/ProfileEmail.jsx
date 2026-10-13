import { useProfileEmail } from "./useProfileEmail";

import Button from "../../../../components/Button/buttons";
import Icon from "../../../../components/Icon/Icons";


function ProfileEmail() {
  const {
    email,
    errors,
    emailStatus,
    isEditing,
    editing,
    cancelEditing,
    handleChange,
    handleSubmit,
  } = useProfileEmail();

  return (
    <div className="profileEmail">
      {isEditing ? (
        <div className="profileEmail__edit">
          <div className="profileEmail__edit-actions">
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

          <div className="profileEmail__form">
            <input
              id="email"
              name="email"
              type="email"
              value={email}
              onChange={handleChange}
              placeholder="Email (Requis)"
              className="profile__input"
            />

            {emailStatus === "unavailable" && (
              <p className="profile__field-error">
                Email déjà utilisé.

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

          {errors.length > 0 && (
            <ul className="profileEmail__errors">
              {errors.map(function (message, index) {
                return (
                  <li key={index} className="profileEmail__error">
                    <Icon
                      name="cross"
                      className="profileEmail__error-icon"
                    />

                    {message}
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      ) : (
        <div className="profileEmail__read">
          <p className="profileEmail__read-value">
            {email}
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

export default ProfileEmail;
