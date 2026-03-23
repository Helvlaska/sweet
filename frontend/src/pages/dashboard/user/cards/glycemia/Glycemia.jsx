import { useGlycemia } from "./useGlycemia";
import { useGlycemiaChart } from "./useGlycemiaChart";

import Button from "../../../../../components/Button/buttons";
import Icon from "../../../../../components/Icon/Icons";
import imgCard from "../../../../../assets/dashboard/card-glycemia.webp";
import imgPopUp from "../../../../../assets/dashboard/popup-glycemia.webp";


function Glycemia() {
  const {
    entries,
    average,
    period,
    loading,
    showPopup,
    value,
    errors,
    handleChange,
    handleSubmit,
    openPopup,
    closePopup,
    setRange,
  } = useGlycemia();

  const { chartRef } = useGlycemiaChart(entries);

  return (
    <section className="glycemia">
      <header className="glycemia__header">
        <div className="glycemia__container">
          <img
            src={imgCard}
            alt="Icone de la carte glycémie"
            className="glycemia__img"
          />

          <h2 className="glycemia__title">Glycémie</h2>
        </div>

        <Button
          onClick={openPopup}
          className="btn-round-white"
        >
          <Icon name="plus" strokeWidth={2} size={15.5} />
        </Button>
      </header>

      <section className="glycemia__body">
        <p className="glycemia__text">
          Cette semaine, tu as une glycémie moyenne de :

          {loading ? (
            <span className="glycemia__value--loading">...</span>

          ) : average !== null ? (
            <span className="glycemia__value">{average} mg/l</span>

          ) : (
            <span className="glycemia__value--empty">- mg/l</span>
          )}
        </p>

        <div className="glycemia__chart">
          <canvas ref={chartRef}></canvas>
        </div>
      </section>

      <footer className="glycemia__footer">
        <p className="glycemia__text">Ta moyenne sur :</p>

        <div className="glycemia__range">
          <div className="glycemia__actions">
            <Button
              onClick={function() {
                setRange("month");
              }}
              className={
                period === "month"
                  ? "btn-pill-glycemia is-active"
                  : "btn-pill-glycemia"
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
                  ? "btn-pill-glycemia is-active"
                  : "btn-pill-glycemia"
              }
            >
              90 jours
            </Button>
          </div>

          <div className="glycemia__values">
            {loading ? (
              <span className="glycemia__value--loading">...</span>

            ) : average !== null ? (
              <span className="glycemia__value">{average} mg/l</span>

            ) : (
              <span className="glycemia__value--empty">0 mg/l</span>
            )}
          </div>
        </div>
      </footer>

      {showPopup && (
        <div className="glycemia__popup">
          <img
            src={imgPopUp}
            alt="Image d'illustration du popup"
            className="popup__img"
          />

          <div className="popup__content">
            <h2 className="popup__title">
              Quelle est la glycémie de ta journée ?
            </h2>

            <form className="popup__form" onSubmit={handleSubmit}>
              <input
                name="glycemia"
                type="number"
                step="0.1"
                placeholder="Glycémie (mg/l)"
                value={value}
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

export default Glycemia;
