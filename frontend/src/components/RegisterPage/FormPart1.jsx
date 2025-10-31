import React from "react";

// import de la logique du composant
import { FormPart1Logic } from "./FormPart1Logic";

// import des images et des icones
import illustrationRegisterOpen from "../../assets/register/InscriptionIllustrationEnchante.png";
import illustrationRegisterClose from "../../assets/register/InscriptionIllustrationEnchanteYeuxFerme.png";
import passwordIconOpen from "../../assets/icones/eye-open.png";
import passwordIconClose from "../../assets/icones/eye-close.png";
import redCross from "../../assets/icones/red-cross.png";

function FormPart1({ formData, updateFormData, nextStep }) {
    const {
        email, username, password, errorMessage, showPassword,
        handleChange, handleBlur, handleSubmit, togglePasswordVisibility
    } = FormPart1Logic(formData, updateFormData, nextStep);

    return (
        <div className="register-step1">
            <form onSubmit={handleSubmit} className="register-step1__form">
                <h1 className="register-step1__title">Avec quels identifiants voudras-tu te connecter ?</h1>
                <div className="register-step1__group">
                    <input id="email" name="email" type="email" value={email} onChange={handleChange} onBlur={handleBlur} placeholder="Adresse email" required className="register-step1__input" />
                </div>
                <div className="register-step1__group">
                    <input id="username" name="username" type="text" value={username} onChange={handleChange} onBlur={handleBlur} placeholder="Nom d'utilisateur" required className="register-step1__input" />
                </div>
                <div className="register-step1__group register-step1__group--password">
                    <input id="password" name="password" type={showPassword ? "text" : "password"} value={password} onChange={handleChange} placeholder="Mot de passe" required className="register-step1__input" />
                    <img src={showPassword ? passwordIconOpen : passwordIconClose} alt={showPassword ? "Icône œil ouvert" : "Icône œil fermé"} className="register-step1__icon" onClick={togglePasswordVisibility} />
                </div>
                {errorMessage && (
                    <p className="register-step1__message register-step1__message--error">
                        <img src={redCross} alt="Erreur" className="register-step1__icon--error" />
                        {errorMessage}
                    </p>
                )}
                <p className="register-step1__warning">En continuant, vous acceptez les Conditions d’utilisation de Sweet et vous confirmez avoir lu la Politique de confidentialité de Sweet.</p>
                <div className="register-step1__actions">
                    <button type="submit" className="register-step1__button">
                        Continuer
                    </button>
                </div>
            </form>
            <div className="register-step1__illustration">
                <img src={showPassword ? illustrationRegisterOpen : illustrationRegisterClose} alt="Mascotte Sweet" className="register-step1__mascot" />
            </div>
        </div>
    );
}

export default FormPart1;
