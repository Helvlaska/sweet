import React from "react";
import { translateSpeciality } from "../../../../utils/translateEnum/translateSpecialities";

import HealthProUpdate from "./healthProUpdate/HealthProUpdate";

import Button from "../../../../components/Button/buttons";
import Icon from "../../../../components/Icon/Icons";
import PhoneIcon from "../../../../components/Icon/Icons-custom/PhoneIcon";
import HomeIcon from "../../../../components/Icon/Icons-custom/HomeIcon";
import MailIcon from "../../../../components/Icon/Icons-custom/MailIcon";


function HealthProList({ fetchPros, healthPros, selectedPro, isLoading, isOpenPro, isOpenDocs, selectForUpdate, togglePro, toggleDocs, removePro }) {

  return (
    <div className="healthProList">
      {isLoading && (
        <p className="healthProList__loading">Chargement...</p>
      )}

      {!isLoading && healthPros.length === 0 && (
        <p className="healthProList__empty">
          Aucun professionnel enregistré.
        </p>
      )}

      {!isLoading && healthPros.length > 0 && (
        <ul className="healthProList__list">
          {healthPros.map(function(pro) {
            return (
              <li key={pro.id} className="healthProList__item">
                {selectedPro && selectedPro.id === pro.id ? (
                  <HealthProUpdate
                    fetchPros={fetchPros}
                    selectedPro={selectedPro}
                    setSelectedPro={selectForUpdate}
                  />

                ) : isOpenPro === pro.id ? (
                  <div className="healthProList__item--open">
                    <Button
                      onClick={function() {
                        togglePro(pro.id);
                      }}
                      className="btn-list"
                    >
                      <p className="healthProList__group">
                        {translateSpeciality(pro.speciality)}
                      </p>

                      <p className="healthProList__group">
                        {pro.fullname}
                      </p>

                      <Icon
                        name="arrowDown"
                        strokeWidth="1.3"
                        size={14}
                        className={isOpenPro === pro.id ? "btn-list__arrow--open" : "btn-list__arrow--close"}
                      />
                    </Button>

                    <div className="healthProList__row">
                      <p className="healthProList__group">
                        {translateSpeciality(pro.speciality)}
                      </p>

                      <p className="healthProList__group">
                        {pro.fullname}
                      </p>

                      <div className="healthProList__group">
                        <PhoneIcon size={11} />

                        <p className={pro.phone ? "healthProList__phone" : "healthProList__placeholder"}>
                          {pro.phone || "N° de téléphone"}
                        </p>
                      </div>
                    </div>

                    <div className="healthProList__row--split">
                      <div className="healthProList__group--full">
                        <MailIcon size={11} />

                        <p className={pro.email ? "healthProList__email" : "healthProList__placeholder"}>
                          {pro.email || "Adresse mail"}
                        </p>
                      </div>

                      <div className="healthProList__group--full">
                        <HomeIcon size={11} />

                        <p className={pro.address ? "healthProList__address" : "healthProList__placeholder"}>
                          {pro.address || "Adresse (N°, adresse)"}
                        </p>
                      </div>

                      <div className="healthProList__group--split">
                        <p className={pro.postal_code ? "healthProList__postalCode" : "healthProList__placeholder"}>
                          {pro.postal_code || "CP"}
                        </p>
                      </div>

                      <div className="healthProList__group--split">
                        <p className={pro.city ? "healthProList__city" : "healthProList__placeholder"}>
                          {pro.city || "Ville"}
                        </p>
                      </div>
                    </div>

                    <div className="healthProList__row">
                      <div className="healthProList__group--list">
                        <Button
                          onClick={function() {
                            toggleDocs(pro.id);
                          }}
                          className="btn-list"
                        >
                          Vos documents

                          <Icon
                            name="arrowDown"
                            strokeWidth="1"
                            className={isOpenDocs === pro.id ? "btn-list__arrow--open" : "btn-list__arrow--close"}
                          />
                        </Button>

                        {isOpenDocs === pro.id && (
                          <div className="healthProList__documents--list">
                            {pro.documents && pro.documents.length === 0 && (
                              <p className="healthProList__empty">Aucun document ajouté</p>
                            )}

                            {pro.documents && pro.documents.length > 0 && (
                              <ul className="healthProList__list--items">
                                {pro.documents.map(function(doc) {
                                  return (
                                    <li key={doc.id} className="healthProList__list--item">
                                      <p className="healthProList__item--filename">
                                        {doc.filename}
                                      </p>
                                    </li>
                                  );
                                })}
                              </ul>
                            )}
                          </div>
                        )}
                      </div>

                      <div className="healthProList__actions">
                        <Button
                          onClick={function () {
                            removePro(pro);
                          }}
                          className="btn-round-grey"
                        >
                          <Icon name="trash" strokeWidth="1" />
                        </Button>

                        <Button
                          onClick={function () {
                            selectForUpdate(pro);
                          }}
                          className="btn-round-grey"
                        >
                          <Icon name="pen" strokeWidth="1" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="healthProList__item--close">
                    <Button
                      onClick={function() {
                        togglePro(pro.id);
                      }}
                      className="btn-list"
                    >
                      <p className="healthProList__group">
                        {translateSpeciality(pro.speciality)}
                      </p>

                      <p className="healthProList__group">
                        {pro.fullname}
                      </p>

                      <Icon
                        name="arrowDown"
                        strokeWidth="1.2"
                        size={11}
                      />
                    </Button>
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      )}

      <span className="healthProList__separator" />
    </div>
  );
}

export default HealthProList;
