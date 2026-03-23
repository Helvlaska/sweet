import { useMood } from "./useMood";

import Button from "../../../../../components/Button/buttons";
import Icon from "../../../../../components/Icon/Icons";
import SelectedField from "../../../../../components/Form/SelectedField/SelectedField";
import imgCard from "../../../../../assets/dashboard/card-mood.webp";
import imgPopUp from "../../../../../assets/dashboard/popup-mood.webp";


function Mood() {
  const {
    entries,
    mood,
    showPopup,
    errors,
    handleChange,
    openPopup,
    closePopup,
    handleSubmit,
  } = useMood();

  return (
    <section className="mood">
      <header className="mood__header">
        <div className="mood__container">
          <img
            src={imgCard}
            alt="Icone de la carte humeur"
            className="mood__img"
          />

          <h2 className="mood__title">Humeur</h2>
        </div>

        <Button
          onClick={openPopup}
          className="btn-round-white"
        >
          <Icon name="plus" strokeWidth={2} size={15.5} />
        </Button>
      </header>

      <div className="mood__body">
        <ul className="mood__items">
          {entries.length > 0 ? (
            entries.map(function (item, index) {
              return (
                <li key={index} className="mood__item">
                  {item.description}
                </li>
              );
            })

          ) : (
            <li className="mood__item--empty">
              Aucune humeur enregistrée.
            </li>
          )}
        </ul>
      </div>

      {showPopup && (
        <div className="mood__popup">
          <img
            src={imgPopUp}
            alt="Image d'illustration du popup"
            className="popup__img"
          />

          <div className="popup__content">
            <h2 className="popup__title">
              Comment t’es-tu senti pendant ta journée ?
            </h2>

            <form className="popup__form" onSubmit={handleSubmit}>
              <SelectedField
                name="mood"
                placeholder="Choisis une humeur"
                value={mood}
                onChange={handleChange}
                className= "selectedField--white"
                options={[
                  { value: "Joyeux", label: "Joyeux" },
                  { value: "Motivé", label: "Motivé" },
                  { value: "Calme", label: "Calme" },
                  { value: "Neutre", label: "Neutre" },
                  { value: "Fatigué", label: "Fatigué" },
                  { value: "Anxieux", label: "Anxieux" },
                  { value: "Irritable", label: "Irritable" },
                  { value: "Déprimé", label: "Déprimé" },
                ]}
              />

              {errors.length > 0 && (
                <ul className="popup__errors">
                  {errors.map(function (message, index) {
                    return (
                      <li key={index} className="popup__error">
                        <Icon
                          name="cross"
                          strokeWidth="1.5"
                          className="popup__error-icon"
                        />
                        {message}
                      </li>
                    );
                  })}
                </ul>
              )}

              <Button
                type="submit"
                className="btn-pill-outline-violet"
              >
                Confirmer

                <Icon name="chevronRight" strokeWidth="2" />
              </Button>
            </form>
          </div>

          <Button
            onClick={closePopup}
            className="btn-round-popup--close"
          >
            <Icon name="cross" strokeWidth="1" size={14} />
          </Button>
        </div>
      )}
    </section>
  )
}

export default Mood;
