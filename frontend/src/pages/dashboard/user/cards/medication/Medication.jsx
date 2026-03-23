import { useMedication } from "./useMedication";
import { useMedicationChart } from "./useMedicationChart";

import Button from "../../../../../components/Button/buttons";
import Icon from "../../../../../components/Icon/Icons";
import WarningIcon from "../../../../../components/Icon/Icons-custom/WarningIcon";
import SelectedField from "../../../../../components/Form/SelectedField/SelectedField";
import imgCard from "../../../../../assets/dashboard/card-medication.webp";
import imgPopUp from "../../../../../assets/dashboard/popup-medication.webp";


function Medication() {
  const {
    medications,
    medicationOptions,
    lowStock,
    selectedMed,
    showPopup,
    errors,
    handleChange,
    openPopup,
    closePopup,
    handleSubmit,
  } = useMedication();

  const { chartRef } = useMedicationChart(medications);

  return (
    <section className="medication">
      <header className="medication__header">
        <div className="medication__container">
            <img
              src={imgCard}
              alt="Icone de la carte médication"
              className="medication__img"
            />

            <h2 className="medication__title">Médication</h2>
        </div>

        <Button
          onClick={openPopup}
          className="btn-round-white"
        >
          <Icon name="plus" strokeWidth={2} size={15.5} />
        </Button>
      </header>

      <section className="medication__body">
        <canvas ref={chartRef}></canvas>
      </section>

      {lowStock && (
        <footer className="medication__footer">
          <WarningIcon size={49} />

          <div className="medication__text">
            <h2>{lowStock.name}</h2>

            <p>
              Attention, il vous reste {lowStock.stock} mg
            </p>
          </div>
        </footer>
      )}

      {showPopup && (
        <div className="medication__popup">
          <img
            src={imgPopUp}
            alt="Image d'illustration du popup"
            className="popup__img"
          />

          <div className="popup__content">
            <h2 className="popup__title">
              Quel médicament as tu pris aujourd’hui ?
            </h2>

            <form className="popup__form" onSubmit={handleSubmit}>
              <SelectedField
                name="description"
                placeholder="Choisis un médicament"
                value={selectedMed}
                onChange={handleChange}
                className="selectedField--white"
                options={medicationOptions}
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

export default Medication;
