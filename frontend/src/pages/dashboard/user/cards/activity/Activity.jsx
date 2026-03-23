import { useActivity } from "./useActivity";
import { useActivityChart } from "./useActivityChart";

import Button from "../../../../../components/Button/buttons";
import Icon from "../../../../../components/Icon/Icons";
import SelectedField from "../../../../../components/Form/SelectedField/SelectedField";
import imgCard from "../../../../../assets/dashboard/card-activity.webp";
import imgPopUp from "../../../../../assets/dashboard/popup-activity.webp";


function Activity() {
  const {
    description,
    duration,
    entries,
    average,
    period,
    loading,
    showPopup,
    errors,

    handleChange,
    openPopup,
    closePopup,
    setRange,
    handleSubmit,
  } = useActivity();

  const { chartRef } = useActivityChart(entries);

  return (
    <section className="activity">
      <header className="activity__header">
        <div className="activity__container">
          <img
            src={imgCard}
            alt="Icone de la carte activité physique"
            className="activity__img"
          />

          <h2 className="activity__title">Activité physique</h2>
        </div>

        <Button
          onClick={openPopup}
          className="btn-round-white"
        >
          <Icon name="plus" strokeWidth={2} size={15.5} />
        </Button>
      </header>

      <section className="activity__body">
        <p className="activity__text">
          Cette semaine, tu as fait en moyenne :

          {loading ? (
            <span className="activity__value--loading">...</span>

          ) : average !== null ? (
            <span className="activity__value">{average} min/j</span>

          ) : (
            <span className="activity__value--empty">- min/j</span>
          )}
        </p>

        <div className="activity__chart">
          <canvas ref={chartRef}></canvas>
        </div>
      </section>

      <footer className="activity__footer">
        <p className="activity__text">Ta moyenne sur :</p>

        <div className="activity__range">
          <div className="activity__actions">
            <Button
              onClick={function() {
                setRange("month");
              }}
              className={
                period === "month"
                  ? "btn-pill-activity is-active"
                  : "btn-pill-activity"
              }
            >
              30 jours
            </Button>

            <Button
              onClick={function() {
                setRange("3months");
              }}
              className={
                period === "3months"
                  ? "btn-pill-activity is-active"
                  : "btn-pill-activity"
              }
            >
              90 jours
            </Button>
          </div>

          <div className="activity__values">
            {loading ? (
              <span className="activity__value--loading">...</span>

            ) : average !== null ? (
              <span className="activity__value">{average} min/j</span>

            ) : (
              <span className="activity__value--empty">- min/j</span>
            )}
          </div>
        </div>
      </footer>

      {showPopup && (
        <div className="activity__popup">
          <img
            src={imgPopUp}
            alt="Image d'illustration du popup"
            className="popup__img"
          />

          <div className="popup__content">
            <h2 className="popup__title">
              Combien de temps t’es-tu dépensé aujourd’hui ?
            </h2>

            <form className="popup__form" onSubmit={handleSubmit}>
              <SelectedField
                name="description"
                placeholder="Choisis une activité"
                value={description}
                onChange={handleChange}
                className= "selectedField--white"
                options={[
                  { value: "marche", label: "Marche" },
                  { value: "natation", label: "Natation" },
                  { value: "vélo", label: "Vélo" },
                  { value: "yoga", label: "Yoga" },
                  { value: "pilates", label: "Pilates" },
                  { value: "renforcement", label: "Renforcement musculaire" },
                  { value: "jardinage", label: "Jardinage" },
                  { value: "bricolage", label: "Bricolage" },
                  { value: "ménage", label: "Ménage" },
                  { value: "escaliers", label: "Escaliers" }
                ]}
              />

              <input
                name="duration"
                type="number"
                step="1"
                placeholder="Durée (minutes)"
                value={duration}
                onChange={handleChange}
                className="popup__input" />

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

export default Activity;
