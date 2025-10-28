import React from "react";
import { useNavigate } from "react-router-dom";
import { FormPart2Logic } from "./FormPart2Logic";

function FormPart2({ formData, updateFormData, prevStep }) {
    const navigate = useNavigate();

    function handleSuccess() {
        navigate("/dashboard");
    }
    const {
        firstName, lastName, gender, height, city, dateOfBirth, errorMessage, successMessage,
        handleChange, handleSubmit
    } = FormPart2Logic(formData, updateFormData, handleSuccess);

    return (
        <form onSubmit={(e) => handleSubmit(e)} className="register-step2">

            <div className="form-group">
                <input name="profile_picture" type="file" accept="image/*" onChange={handleChange} />
            </div>

            <div className="form-group">
                <input name="first_name" type="text" value={firstName} placeholder="Prénom" onChange={handleChange} required />
            </div>

            <div className="form-group">
                <input name="last_name" type="text" value={lastName} placeholder="Nom" onChange={handleChange} required />
            </div>

            <div className="form-group">
                <select name="gender" value={gender} onChange={handleChange} required>
                    <option value="">Genre</option>
                    <option value="male">Homme</option>
                    <option value="female">Femme</option>
                    <option value="other">Autre</option>
                    <option value="prefer_not_say">Préférer ne pas dire</option>
                </select>
            </div>

            <div className="form-group">
                <input name="height" type="number" value={height} placeholder="Taille (cm)" onChange={handleChange} required />
            </div>

            <div className="form-group">
                <input name="city" type="text" value={city} placeholder="Ville" onChange={handleChange} required />
            </div>

            <div className="form-group">
                <input name="date_of_birth" type="date" value={dateOfBirth} onChange={handleChange} required />
            </div>

            {errorMessage && <p className="error-message">{errorMessage}</p>}
            {successMessage && <p className="success-message">{successMessage}</p>}

            <div className="form-actions">
                <button type="button" onClick={prevStep}>Retour</button>
                <button type="submit">Créer mon compte</button>
            </div>
        </form>
    );
}

export default FormPart2;
