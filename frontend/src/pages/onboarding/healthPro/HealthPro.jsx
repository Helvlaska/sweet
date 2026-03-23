import React from "react";
import { useHealthPro } from "./useHealthPro";
import { useHealthProList } from "./healthProList/useHealthProList";

import HealthProAdd from "./healthProAdd/HealthProAdd";
import HealthProList from "./healthProList/HealthProList";

import imgWelcome from "../../../assets/onboarding/healthPro/mascot-welcome.webp";
import Button from "../../../components/Button/buttons";
import Icon from "../../../components/Icon/Icons";


function HealthPro() {

  const { goToDashboard } = useHealthPro();
  const { fetchPros, ...propsList } = useHealthProList();


  return (
    <div className="healthPro">
      <div className="healthPro__wrapper">
        <div className="healthPro__progress">
          <p className="healthPro__label">
            Ajout de professionnels de santé
          </p>

          <div className="healthPro__bar">
            <span className="healthPro__page healthPro__page--inactive" />
            <span className="healthPro__page healthPro__page--inactive" />
            <span className="healthPro__page healthPro__page--active" />
          </div>
        </div>

        <div className="healthPro__container">
          <h1 className="healthPro__title">
            Qui sont <br />
            tes professionnels <br />
            de santé ?
          </h1>

          <div className="healthPro__skip">
            <Button className="btn-underline-grey" onClick={goToDashboard}>
              Compléter plus tard
              <Icon
                name="chevronRight"
                strokeWidth="2"
                className="icon--chevron-right"
              />
            </Button>

            <span className="healthPro__separator" />
          </div>



          <div className="healthPro__healthPros">
            <HealthProList fetchPros={fetchPros} {...propsList} />
          </div>

          <div className="healthPro__formAdd">
            <HealthProAdd fetchPros={fetchPros} />
          </div>

          <div className="healthPro__actions">
            <Button onClick={goToDashboard} className="btn-pill-outline-violet">
              Continuer
              <Icon
                name="chevronRight"
                strokeWidth="2"
                className="icon--chevron-right"
              />
            </Button>
          </div>
        </div>
      </div>

      <div className="healthPro__illustration">
        <img
          src={imgWelcome}
          alt="Mascotte Sweet en train de dire enchanté"
          className="healthPro__mascot"
        />
      </div>
    </div>
  )
}

export default HealthPro;
