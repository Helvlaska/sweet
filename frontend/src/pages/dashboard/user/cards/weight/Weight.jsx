import { useWeight } from "./useWeight";
import { useWeightChart } from "./useWeightChart";

import Button from "../../../../../components/Button/buttons";
import Icon from "../../../../../components/Icon/Icons";
import imgCard from "../../../../../assets/dashboard/card-weight.webp";
import imgPopUp from "../../../../../assets/dashboard/popup-weight.webp";


function Weight() {
  const {
    intPart,
    decPart,
    entries,
    period,
    showPopup,
    errors,
    handleChange,
    openPopup,
    closePopup,
    setRange,
    handleSubmit
  } = useWeight();

  const { chartRef } = useWeightChart(entries, period);

  return (
    <section className="weight">
      <header className="weight__header">
        <div className="weight__container">
          <img
            src={imgCard}
            alt="Icone de la carte poids"
            className="weight__img"
          />

          <h2 className="weight__title">Poids</h2>
        </div>

        <Button
          onClick={openPopup}
          className="btn-round-white"
        >
          <Icon name="plus" strokeWidth={2} size={15.5} />
        </Button>
      </header>

      <div className="weight__actions">
        <Button
          onClick={function() {
            setRange("week");
          }}
          className={
            period === "week"
            ? "btn-pill-weight is-active"
            : "btn-pill-weight"
          }
        >
          7 jours
        </Button>

        <Button
          onClick={function() {
            setRange("month");
          }}
          className={
            period === "month"
            ? "btn-pill-weight is-active"
            : "btn-pill-weight"
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
            ? "btn-pill-weight is-active"
            : "btn-pill-weight"
          }
        >
          3 mois
        </Button>

        <Button
          onClick={function() {
            setRange("6months");
          }}
          className={
            period === "6months"
            ? "btn-pill-weight is-active"
            : "btn-pill-weight"
          }
        >
          6 mois
        </Button>
      </div>

      <div className="weight__chart">
        <canvas ref={chartRef}></canvas>
      </div>

      {showPopup && (
        <div className="weight__popup">
          <img
            src={imgPopUp}
            alt="Image d'illustration du popup"
            className="popup__img"
          />

          <div className="popup__content">
            <h2 className="popup__title">
              Quel est ton poids ?
            </h2>

            <form className="popup__form" onSubmit={handleSubmit}>
              <input
                name="intPart"
                type="number"
                step="1"
                placeholder="Kilo"
                value={intPart}
                onChange={handleChange}
                className="popup__input"
              />

              <input
                name="decPart"
                type="number"
                step="1"
                placeholder="Gramme"
                value={decPart}
                onChange={handleChange}
                className="popup__input"
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

export default Weight;
