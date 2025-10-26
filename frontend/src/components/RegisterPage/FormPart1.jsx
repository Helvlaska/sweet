import React from "react";
import { FormPart1Logic } from "./FormPart1Logic";

function FormPart1({ formData, updateFormData, nextStep }) {
    const {
        email, username, password, errorMessage,
        handleChange, handleBlur, handleSubmit
    } = FormPart1Logic(formData, updateFormData, nextStep);

    return (
        <form onSubmit={handleSubmit} className="register-step1">
            <div className="form-group">
                <input id="email" name="email" type="email" value={email} onChange={handleChange} onBlur={handleBlur} placeholder="Adresse Email" required />
            </div>

            <div className="form-group">
                <input id="username" name="username" type="text" value={username} onChange={handleChange} onBlur={handleBlur} placeholder="Nom d'utilisateur" required />
            </div>

            <div className="form-group">
                <input id="password" name="password" type="password" value={password} onChange={handleChange} placeholder="Mot de passe" required />
            </div>

            {errorMessage && <p className="error-message">{errorMessage}</p>}

            <div className="form-actions">
                <button type="submit">Continuer</button>
            </div>
        </form>
    );
}

export default FormPart1;
