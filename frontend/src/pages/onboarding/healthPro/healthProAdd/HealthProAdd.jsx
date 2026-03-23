import React from "react";
import { useHealthProAdd } from "./useHealthProAdd";

import Button from "../../../../components/Button/buttons";
import Icon from "../../../../components/Icon/Icons";
import SelectedField from "../../../../components/Form/SelectedField/SelectedField";
import PhoneIcon from "../../../../components/Icon/Icons-custom/PhoneIcon";
import HomeIcon from "../../../../components/Icon/Icons-custom/HomeIcon";
import MailIcon from "../../../../components/Icon/Icons-custom/MailIcon";


function HealthProAdd({ fetchPros }) {
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
    isOpenFiles,
    isOpen,

    open,
    handleChange,
    handleFileChange,
    toggleFiles,
    removeFile,
    submit,
  } = useHealthProAdd(fetchPros);

  return (
    <div className="healthProAdd">
      <form onSubmit={submit} className="healthProAdd__form">
        {isOpen && (
          <div className="healthProAdd__fields">
            <div className="healthProAdd__row">
              <div className="healthProAdd__group--select">
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

              <div className="healthProAdd__group">
                <input
                  id="fullname"
                  name="fullname"
                  type="text"
                  value={fullname}
                  placeholder="Prénom et Nom (Requis)"
                  onChange={handleChange}
                />
              </div>

              <div className="healthProAdd__group">
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

            <div className="healthProAdd__row--split ">
              <div className="healthProAdd__group healthProAdd__group--full">
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

              <div className="healthProAdd__group healthProAdd__group--full">
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

              <div className="healthProAdd__group healthProAdd__group--split">
                <input
                  id="postal_code"
                  name="postalCode"
                  type="text"
                  value={postalCode}
                  placeholder="CP"
                  onChange={handleChange}
                />
              </div>

              <div className="healthProAdd__group healthProAdd__group--split">
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

            <div className="healthProAdd__row--split">
              <div className="healthProAdd__group--list">
                <Button onClick={toggleFiles} className="btn-list">
                  Vos documents
                  <Icon
                    name="arrowDown"
                    strokeWidth="1.5"
                    size={14}
                    className={isOpenFiles ? "btn-list__arrow--open" : "btn-list__arrow--close"}
                  />
                </Button>

                {isOpenFiles && (
                  <div className="healthProAdd__documents--list">
                    {files.length === 0 && (
                      <p className="healthProAdd__list--empty">Aucun document ajouté</p>
                    )}

                    {files.map(function(file, index) {
                      return (
                        <div key={index} className="healthProAdd__list--items">
                          <span className="healthProAdd__item--filename">{file.name}</span>

                          <Button className="btn-round-list-trash-grey" onClick={function() {
                            removeFile(index);
                          }}>
                            <Icon
                              name="trash"
                              strokeWidth="1"
                              size={13}
                            />
                          </Button>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              <div className="healthProAdd__group--files">
                <input
                  id="file"
                  name="file"
                  type="file"
                  multiple
                  onChange={handleFileChange}
                  className="healthProAdd__input--file"
                />

                <label
                  htmlFor="file"
                  className="healthProAdd__label--file"
                >
                  <span className="healthProAdd__placeholder--file">
                    Ajouter des documents (.jpg, .txt, .pdf)
                  </span>

                  <Icon
                    name="upload"
                    strokeWidth="1.5"
                    size={17}
                  />
                </label>
              </div>

              <div className="healthProAdd__submit">
                <Button type="submit" className="btn-round-grey">
                  <Icon
                    name="check"
                    strokeWidth="1"
                  />
                </Button>
              </div>
            </div>

            <span className="healthProAdd__separator" />
          </div>
        )}

        {errors.length > 0 && (
          <ul className="healthProAdd__errors">
            {errors.map(function (message, index) {
              return (
                <li key={index} className="healthProAdd__error">
                  <Icon
                    name="cross"
                    className="healthProAdd__error-icon"
                  />
                  {message}
                </li>
              );
            })}
          </ul>
        )}
      </form>

      <div className="healthProAdd__actions">
        <Button className="btn-pill-solid-kaki" onClick={open}>
          Rajouter un professionnel de santé
          <Icon
            name="plus"
            strokeWidth="2.5"
            className="healthProAdd__action--icon"
          />
        </Button>
      </div>
    </div>
  )
}

export default HealthProAdd;
