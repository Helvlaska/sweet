import { useProfileMedication } from "./useProfileMedication";
import { useAuth } from "../../../context/useAuth";

import defaultPicture from "../../../assets/profile/default_profile_picture.webp";
import Button from "../../../components/Button/buttons";
import Icon from "../../../components/Icon/Icons";
import SelectedField from "../../../components/Form/SelectedField/SelectedField";


function ProfileMedication({ goToProfile }) {
  const { user } = useAuth();

  const {
    name,
    dose,
    stock,
    frequency,
    lowStock,
    medications,
    selectedMedication,
    errors,
    isOpen,
    open,
    handleChange,
    handleEdit,
    handleEditChange,
    handleEditSubmit,
    handleSubmit,
    removeMedication,
  } = useProfileMedication();


  return (
    <section className="profileMedication">
      <div className="profileMedication__profile-picture">
        <img
          src={user.profile_picture || defaultPicture}
          className="profileMedication__profile-img"
        />
      </div>

      <p className="profileMedication__username">
        {user.username}
      </p>

      <div className="profileMedication__actions">
        <Button
          onClick={goToProfile}
          className="btn-pill-solid--orange"
        >
          Informations personnelles
        </Button>

        <Button
          className="btn-pill-solid--orange"
        >
          Médications et posologies
        </Button>
      </div>

      <div className="profileMedication__wrapper">
        {medications.length === 0 && (
          <p className="profileMedication__list--empty">
            Aucun médicament enregistré.
          </p>
        )}

        {medications.length > 0 && (
          <ul className="profileMedication__list">
            {medications.map(function(medication) {
              const isEditing = selectedMedication?.id === medication.id;

              return (
                <li key={medication.id} className="profileMedication__list--item">
                  <div className="profileMedication__item--group">

                    {isEditing ? (
                      <>
                        <input
                          id="name"
                          name="name"
                          type="text"
                          value={selectedMedication.name || ""}
                          onChange={handleEditChange}
                          className="profileMedication__item--field"
                        />

                        <input
                          id="dose"
                          name="dose"
                          type="text"
                          value={selectedMedication.dose || ""}
                          onChange={handleEditChange}
                          className="profileMedication__item--field"
                        />

                        <input
                          id="stock"
                          name="stock"
                          type="text"
                          value={selectedMedication.stock || ""}
                          onChange={handleEditChange}
                          className="profileMedication__item--field"
                        />

                        <SelectedField
                          name="frequency"
                          value={selectedMedication.frequency || ""}
                          placeholder="Posologie (Requis)"
                          onChange={handleEditChange}
                          className="profileMedication__item--field-select"
                          options={[
                            { value: "once_a_day", label: "1x/jour" },
                            { value: "twice_a_day", label: "2x/jour" },
                            { value: "three_a_day", label: "3x/jour" },
                            { value: "as_needed", label: "En cas de besoin" },
                          ]}
                        />

                        <input
                          id="alert_threshold"
                          name="alert_threshold"
                          type="text"
                          value={selectedMedication.alert_threshold || ""}
                          onChange={handleEditChange}
                          placeholder="Seuil d'alerte (mg)"
                          className="profileMedication__item--field"
                        />

                        <Button
                          onClick={handleEditSubmit}
                          className=""
                        >
                          <Icon name="check" strokeWidth="1" size={20} />
                        </Button>
                      </>
                    ) : (
                      <>
                        <p className="profileMedication__item--field">
                          {medication.name}
                        </p>

                        <p className="profileMedication__item--field">
                          {medication.dose}
                        </p>

                        <p className="profileMedication__item--field">
                          {medication.stock}
                        </p>

                        <p className="profileMedication__item--field">
                          {medication.frequency}
                        </p>

                        <p className="profileMedication__item--field">
                          {medication.alert_threshold}
                        </p>

                        <div className="profileMedication__item--actions">
                          <Button
                            onClick={function() { handleEdit(medication); }}
                            className=""
                          >
                            <Icon name="pen" strokeWidth="1" size={20} />
                          </Button>

                          <Button
                            onClick={function() { removeMedication(medication); }}
                            className=""
                          >
                            <Icon name="trash" strokeWidth="1" size={20} />
                          </Button>
                        </div>
                      </>
                    )}
                  </div>

                  <div className="profileMedication__separator"></div>
                </li>
              );
            })}
          </ul>
        )}

        <Button
          onClick={open}
          className="btn-pill-outline--grey"
        >
          Ajouter un médicament

          <Icon
            name="plus"
            strokeWidth="1"
            size={20}
            className="profileMedication__action--icon"
          />
        </Button>

        {isOpen && (
          <div className="profileMedication__form">
            <div className="profileMedication__item--group">
              <input
                id="name"
                name="name"
                type="text"
                value={name}
                placeholder="Nom (Requis)"
                onChange={handleChange}
                className="profileMedication__item--field"
              />

              <input
                id="dose"
                name="dose"
                type="text"
                value={dose}
                placeholder="Dose (Requis)"
                onChange={handleChange}
                className="profileMedication__item--field"
              />

              <input
                id="stock"
                name="stock"
                type="text"
                value={stock}
                placeholder="Stock (Requis)"
                onChange={handleChange}
                className="profileMedication__item--field"
              />

              <SelectedField
                name="frequency"
                value={frequency}
                placeholder="Posologie (Requis)"
                onChange={handleChange}
                className="profileMedication__item--field-select"
                options={[
                  { value: "once_a_day", label: "1x/jour" },
                  { value: "twice_a_day", label: "2x/jour" },
                  { value: "three_a_day", label: "3x/jour" },
                  { value: "as_needed", label: "En cas de besoin" },
                ]}
              />

              <input
                id="lowStock"
                name="lowStock"
                type="text"
                value={lowStock}
                placeholder="Seuil d'alerte (mg)"
                onChange={handleChange}
                className="profileMedication__item--field"
              />

              {errors.length > 0 && (
                <ul className="profile__errors">
                  {errors.map(function(message, index) {
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

              <Button
                onClick={handleSubmit}
                className="btn-pill-outline--grey"
              >
                Ajouter

                <Icon
                  name="check"
                  strokeWidth="1"
                  size={20}
                  className="profileMedication__action--icon"
                />
              </Button>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

export default ProfileMedication;
