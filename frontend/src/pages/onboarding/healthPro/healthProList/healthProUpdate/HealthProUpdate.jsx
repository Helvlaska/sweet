import React from "react";
import { useHealthProUpdate } from "./useHealthProUpdate";
import { translateSpeciality } from "../../../../../utils/translateEnum/translateSpecialities";

import Button from "../../../../../components/Button/buttons";
import Icon from "../../../../../components/Icon/Icons";
import PhoneIcon from "../../../../../components/Icon/Icons-custom/PhoneIcon";
import HomeIcon from "../../../../../components/Icon/Icons-custom/HomeIcon";
import MailIcon from "../../../../../components/Icon/Icons-custom/MailIcon";
import SelectedField from "../../../../../components/Form/SelectedField/SelectedField";


function HealthProUpdate({ fetchPros, selectedPro, setSelectedPro, togglePro }) {
  const {
    speciality,
    fullname,
    phone,
    email,
    address,
    postalCode,
    city,
    files,
    errors,
    isOpenDocs,

    close,
    handleChange,
    handleFileChange,
    toggleDocs,
    removeFiles,
    removeDoc,
    submit,
  } = useHealthProUpdate(fetchPros, selectedPro, setSelectedPro);

  return (
    <div className="healthProUpdate">
      <Button
        onClick={function() {
          togglePro(selectedPro.id);
        }}
        className="btn-list"
      >
        <p className="healthProUpdate__group">
          {translateSpeciality(selectedPro.speciality)}
        </p>

        <p className="healthProUpdate__group">
          {selectedPro.fullname}
        </p>

        <Icon
          name="arrowDown"
          strokeWidth="1.2"
          size={11}
        />
      </Button>

      <form onSubmit={submit} className="healthProUpdate__form">
        <div className="healthProUpdate__row">
          <div className="healthProUpdate__group--select">
            <SelectedField
              name="speciality"
              placeholder="Spécialité (Requis)"
              value={speciality}
              onChange={handleChange}
              options={[
                { value: "general_practitioner", label: "Médecin généraliste" },
                { value: "diabetologist", label: "Diabétologue" },
                { value: "endocrinologist", label: "Endocrinologue" },
                { value: "cardiologist", label: "Cardiologue" },
                { value: "ophthalmologist", label: "Ophtalmologue" },
                { value: "nephrologist", label: "Néphrologue" },
                { value: "podiatrist", label: "Podologue" },
                { value: "dentist", label: "Dentiste" },
                { value: "dietitian", label: "Diététicien" },
                { value: "nurse", label: "Infirmier" },
                { value: "psychologist", label: "Psychologue" },
                { value: "pharmacist", label: "Pharmacien" },
                { value: "physiotherapist", label: "Kinésithérapeute" },
                { value: "physical_educator", label: "Éducateur physique" },
                { value: "social_worker", label: "Assistant social" },
                { value: "gynecologist", label: "Gynécologue" },
              ]}
            />
          </div>

          <div className="healthProUpdate__group">
            <input
              id="fullname"
              name="fullname"
              type="text"
              value={fullname}
              placeholder="Prénom et Nom (Requis)"
              onChange={handleChange}
            />
          </div>

          <div className="healthProUpdate__group">
            <PhoneIcon size={11} />

            <input
              id="phone"
              name="phone"
              type="text"
              value={phone}
              placeholder="N° de téléphone"
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="healthProUpdate__row--split">
          <div className="healthProUpdate__group--full">
            <MailIcon size={11} />

            <input
              id="email"
              name="email"
              type="email"
              value={email}
              placeholder="Adresse mail"
              onChange={handleChange}
            />
          </div>

          <div className="healthProUpdate__group--full">
            <HomeIcon size={11} />

            <input
              id="address"
              name="address"
              type="text"
              value={address}
              placeholder="Adresse (N°, adresse)"
              onChange={handleChange}
            />
          </div>

          <div className="healthProUpdate__group--split">
            <input
              id="postal_code"
              name="postalCode"
              type="text"
              value={postalCode}
              placeholder="CP"
               onChange={handleChange}
             />
           </div>

          <div className="healthProUpdate__group--split">
            <input
              id="city"
              name="city"
              type="text"
              value={city}
              placeholder="Ville"
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="healthProUpdate__row">
          <div className="healthProUpdate__group--list">
            <Button
              onClick={function() {
                toggleDocs(selectedPro.id);
              }}
              className="btn-list"
            >
              Vos documents

              <Icon
                name="arrowDown"
                strokeWidth="1.3"
                size={14}
                className={isOpenDocs === selectedPro.id ? "btn-list__arrow--open" : "btn-list__arrow--close"}
              />
            </Button>

            {isOpenDocs === selectedPro.id && (
              <div className="healthProUpdate__documents--list">
                {selectedPro.documents && selectedPro.documents.length === 0 && files.length === 0 && (
                  <p className="healthProUpdate__empty">Aucun document ajouté</p>
                )}

                <ul className="healthProUpdate__documents--items">
                  {selectedPro.documents && selectedPro.documents.map(function(doc) {
                    return (
                      <li key={doc.id} className="healthProUpdate__document--item">
                        <p className="healthProUpdate__document--filename">
                          {doc.filename}
                        </p>
                        <Button
                          onClick={function() {
                            removeDoc(selectedPro.id, doc.id);
                          }}
                          className="btn-round-list-trash-grey"
                        >
                          <Icon name="trash" strokeWidth="1" size={13} />
                        </Button>
                      </li>
                    );
                  })}

                  {files.map(function(file, index) {
                    return (
                      <li key={index} className="healthProUpdate__document--item">
                        <span className="healthProUpdate__document--filename">
                          {file.name}
                        </span>
                        <Button
                          onClick={function() {
                            removeFiles(index);
                          }}
                          className="btn-round-list-trash-grey"
                        >
                          <Icon name="trash" strokeWidth="1" />
                        </Button>
                      </li>
                    );
                  })}
                </ul>
              </div>
            )}
          </div>

          <div className="healthProUpdate__group--files">
            <input
              id="file"
              name="file"
              type="file"
              multiple
              onChange={handleFileChange}
              className="healthProUpdate__input--file"
            />

            <label htmlFor="file" className="healthProUpdate__label--file">
              <p className="healthProUpdate__placeholder--file">
                Ajouter des documents (.jpg, .txt, .pdf)
              </p>

              <Icon name="upload" strokeWidth="1.5" />
            </label>
          </div>


          <div className="healthProUpdate__actions">
            <Button
              type="submit"
              className="btn-round-grey"
            >
              <Icon name="check" strokeWidth="1" />
            </Button>

            <Button
              onClick={close}
              className="btn-round-grey"
            >
              <Icon name="cross" strokeWidth="1" />
            </Button>
          </div>
        </div>

        {errors.length > 0 && (
          <ul className="healthProUpdate__errors">
            {errors.map(function (message, index) {
              return (
                <li key={index} className="healthProUpdate__error">
                  <Icon name="cross" className="healthProUpdate__error--icon" />
                  {message}
                </li>
              );
            })}
          </ul>
        )}
       </form>

       <span className="healthProUpdate__separator" />
     </div>
  );
}

export default HealthProUpdate;
