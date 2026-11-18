import { useProfileAvatar } from "./useProfileAvatar";
import { useAuth } from "../../../../context/useAuth";

import defaultPicture from "../../../../assets/profile/default_profile_picture.webp";
import Button from "../../../../components/Button/buttons";
import Icon from "../../../../components/Icon/Icons";


function ProfileAvatar() {
  const { user } = useAuth();

  const {
    preview,
    errors,
    isLoading,
    successMessage,
    inputRef,
    openFilePicker,
    handleFileChange,
    handleFileSubmit,
    cancelPreview,
  } = useProfileAvatar();

  return (
    <section className="profileInfo__avatar">
      <input
        type="file"
        className="profileInfo__avatar-input"
        ref={inputRef}
        accept="image/jpeg,image/png"
        onChange={handleFileChange}
      />

      <div className="profileInfo__avatar-wrapper">
        <img
          src={preview || user.profile_picture || defaultPicture}
          className="profileInfo__avatar-img"
          alt="Photo de profil"
        />

        {preview ? (
          <div>
            <Button
              onClick={handleFileSubmit}
              disabled={isLoading}
              className="btn-round--kaki profileInfo__avatar-btn"
            >
              <Icon name="check" strokeWidth="1" size={20} />
            </Button>

            <Button
              onClick={cancelPreview}
              disabled={isLoading}
              className="btn-round--kaki profileInfo__avatar-btn"
            >
              <Icon name="cross" strokeWidth="1" size={20} />
            </Button>
          </div>
        ) : (
          <Button
            onClick={openFilePicker}
            className="btn-round--kaki profileInfo__avatar-btn"
          >
            <Icon name="pen" strokeWidth="1" size={20} />
          </Button>
        )}

        {errors.length > 0 && (
          <ul className="profileInfo__errors" role="alert">
            {errors.map(function (message, index) {
              return (
                <li key={index} className="profileInfo__error">
                  <Icon name="cross" className="profileInfo__error-icon" />
                  {message}
                </li>
              );
            })}
          </ul>
        )}

        {successMessage && (
          <p className="profileInfo__success" role="status">
            <Icon name="check" className="profileInfo__succes-icon" />
            {successMessage}
          </p>
        )}
      </div>
    </section>
  );
}

export default ProfileAvatar;
