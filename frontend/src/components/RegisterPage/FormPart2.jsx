import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FormPart2Logic } from "./FormPart2Logic";

// import images et icônes
import PlusIcon from "../../assets/register/InscriptionIconPlus.png";
import ArrowUp from "../../assets/register/InscriptionIconArrowHaut.svg";
import ArrowDown from "../../assets/register/InscriptionIconArrowBas.svg";
import illusRegister from "../../assets/register/InscriptionIllustrationEnchante.png";

function FormPart2({ formData, updateFormData, prevStep }) {
    const navigate = useNavigate();
    const [isOpen, setIsOpen] = useState(false);

    function handleSuccess() {
        navigate("/dashboard");
    }

    const {
        firstName, lastName, gender, height, city, dateOfBirth, errorMessage, successMessage, preview,
        handleChange, handleSubmit, handleFileChange
    } = FormPart2Logic(formData, updateFormData, handleSuccess);

    return (
        <form onSubmit={handleSubmit} className="register-step2">
            <div className="register-step2__content">
                <h1 className="register-step2__title">Création de ton profil</h1>
                <div className="profile-upload">
                    <input type="file" id="profilePicture" className="profile-upload__input" accept="image/*" onChange={handleFileChange} />
                    <label htmlFor="profilePicture" className="profile-upload__label">
                        <div className="profile-upload__circle">
                            {preview ? (
                                <img src={preview} alt="Aperçu" className="profile-upload__preview" />
                            ) : (
                                <span className="profile-upload__text">Ajoute une photo de profil</span>
                            )}
                            <div className="profile-upload__icon">
                                <img src={PlusIcon} alt="Icône plus" />
                            </div>
                        </div>
                    </label>
                </div>
                <div className="register-step2__row--first">
                    <div className="form-group">
                        <input name="first_name" type="text" value={firstName} placeholder="Prénom" onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <input name="last_name" type="text" value={lastName} placeholder="Nom" onChange={handleChange} required />
                    </div>
                </div>
                <div className="register-step2__row">
                    <div className="form-group">
                        <input name="height" type="number" value={height} placeholder="Taille (cm)" onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <input name="city" type="text" value={city} placeholder="Ville" onChange={handleChange} required />
                    </div>
                </div>
                <div className="register-step2__row">
                    <div className="form-group">
                        <input name="date_of_birth" type="date" value={dateOfBirth} onChange={handleChange} required />
                    </div>
                    <div className="form-group form-group--select">
                        <div className="custom-select">
                            <select name="gender" value={gender} onChange={handleChange} onFocus={() => setIsOpen(true)} onBlur={() => setIsOpen(false)} required>
                                <option value="">Genre</option>
                                <option value="male">Homme</option>
                                <option value="female">Femme</option>
                                <option value="other">Autre</option>
                                <option value="prefer_not_say">Préférer ne pas dire</option>
                            </select>
                            <img src={isOpen ? ArrowUp : ArrowDown} alt="Flèche déroulante" className="custom-select__icon" />
                        </div>
                    </div>
                </div>
                {errorMessage && (
                    <p className="register-step2__message register-step2__message--error">{errorMessage}</p>
                )}
                {successMessage && (
                    <p className="register-step2__message register-step2__message--success">{successMessage}</p>
                )}
                <div className="register-step2__actions">
                    <button type="button" onClick={prevStep} className="register-step2__button">Retour</button>
                    <button type="submit" className="register-step2__button">Créer mon compte</button>
                </div>
             </div>
            <div className="register-step2__illustration">
                <img src={illusRegister} alt="Illustration inscription" className="register-step2__image" />
            </div>
        </form>
    );
}

export default FormPart2;
