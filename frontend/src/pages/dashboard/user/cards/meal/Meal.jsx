import { useMeal } from "./useMeal";

import Button from "../../../../../components/Button/buttons";
import Icon from "../../../../../components/Icon/Icons";
import imgCard from "../../../../../assets/dashboard/card-meal.webp";
import imgPopUp from "../../../../../assets/dashboard/popup-meal.webp";


function Meal() {
  const {
    breakfast,
    lunch,
    dinner,
    snack,
    showPopup,
    errors,
    groupedMeals,
    handleChange,
    openPopup,
    closePopup,
    handleSubmit
  } = useMeal();

  return (
    <section className="meal">
      <header className="meal__header">
        <div className="meal__container">
          <img
            src={imgCard}
            alt="Icone de la carte glycémie"
            className="meal__img"
          />

          <h2 className="meal__title">Repas</h2>
        </div>

        <Button
          onClick={openPopup}
          className="btn-round-white"
        >
          <Icon name="plus" strokeWidth={2} size={15.5} />
        </Button>
      </header>

      <section className="meal__body">
        <ul className="meal__list">
          <li className="meal__item">
            <h4 className="meal__title">Petit-déjeuner :</h4>

            <ul className="meal__item--meals">
              {groupedMeals["breakfast"] && groupedMeals["breakfast"].length > 0 ? (
                groupedMeals["breakfast"].map(function (desc, i) {
                  return <p key={i} className="meal__value">{desc}</p>;
                })
              ) : (
                <span className="meal__value--empty">Aucun repas enregistré</span>
              )}
            </ul>
          </li>

          <li className="meal__item">
            <h4 className="meal__title">Déjeuner :</h4>

            <ul className="meal__item--meals">
              {groupedMeals["lunch"] && groupedMeals["lunch"].length > 0 ? (
                groupedMeals["lunch"].map(function (desc, i) {
                  return <p key={i} className="meal__value">{desc}</p>;
                })
              ) : (
                <span className="meal__value--empty">Aucun repas enregistré</span>
              )}
            </ul>
          </li>

          <li className="meal__item">
            <h4 className="meal__title">Dîner :</h4>

            <ul className="meal__item--meals">
              {groupedMeals["dinner"] && groupedMeals["dinner"].length > 0 ? (
                groupedMeals["dinner"].map(function (desc, i) {
                  return <p key={i} className="meal__value">{desc}</p>;
                })
              ) : (
                <span className="meal__value--empty">Aucun repas enregistré</span>
              )}
            </ul>
          </li>

          <li className="meal__item">
            <h4 className="meal__title">Collation :</h4>

            <ul className="meal__item--meals">
              {groupedMeals["snack"] && groupedMeals["snack"].length > 0 ? (
                groupedMeals["snack"].map(function (desc, i) {
                  return <p key={i} className="meal__value">{desc}</p>;
                })
              ) : (
                <span className="meal__value--empty">Aucun repas enregistré</span>
              )}
            </ul>
          </li>
        </ul>
      </section>

      {showPopup && (
        <div className="meal__popup">
          <img
            src={imgPopUp}
            alt="Image d'illustration du popup"
            className="popup__img"
          />

          <div className="popup__content">
            <h2 className="popup__title">
              Qu’as-tu mangé aujourd’hui ?
            </h2>

            <form className="popup__form" onSubmit={handleSubmit}>
              <input
                name="breakfast"
                type="text"
                placeholder="Petit-déjeuner"
                value={breakfast}
                onChange={handleChange}
                className="popup__input"
              />

              <input
                name="lunch"
                type="text"
                placeholder="Déjeuner"
                value={lunch}
                onChange={handleChange}
                className="popup__input"
              />

              <input
                name="dinner"
                type="text"
                placeholder="Dîner"
                value={dinner}
                onChange={handleChange}
                className="popup__input"
              />

              <input
                name="snack"
                type="text"
                placeholder="Collation"
                value={snack}
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

export default Meal;
