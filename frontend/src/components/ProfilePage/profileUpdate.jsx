import React, { useState } from "react";
import { validateField } from "../../utils/validator";
import { formatData } from "../../utils/dataFormatter";
import { useAuth } from "../../context/AuthContext";

// Imports d’assets (à adapter à ton arborescence)
import ModifyIcon from "../../assets/profile/ProfileIconModifier.png"

function ProfileUpdate({ formData, updateFormData, handleSubmit, nextStep }) {

    const {user} = useAuth();

    const [firstName, setFirstName] = useState(formData.first_name || "");
    const [lastName, setLastName] = useState(formData.last_name || "");
    const [gender, setGender] = useState(formData.gender || "");
    const [height, setHeight] = useState(formData.height || "");
    const [city, setCity] = useState(formData.city || "");
    const [dateOfBirth, setDateOfBirth] = useState(formData.date_of_birth || "");
    const [profilePicture, setProfilePicture] = useState(formData.profile_picture || null);

    const [errorMessage, setErrorMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const [preview, setPreview] = useState(null);

    function handleChange(event) {
        const { name, value, files } = event.target;

        if (name === "first_name") setFirstName(value);
        if (name === "last_name") setLastName(value);
        if (name === "gender") setGender(value);
        if (name === "height") setHeight(value);
        if (name === "city") setCity(value);
        if (name === "date_of_birth") setDateOfBirth(value);

        if (name === "profile_picture" && files && files[0]) {
            setProfilePicture(files[0]);
            setPreview(URL.createObjectURL(files[0]));
        }

        // Validation immédiate
        if (value) {
            const isValid = validateField(name, value);
            setErrorMessage(isValid ? "" : `Champ invalide : ${name}`);
        } else {
            // Pas de validation pour les champs laissés vides (update partielle)
            setErrorMessage("");
        }
    }

    function validateForm() {
        const fields = {
            first_name: firstName,
            last_name: lastName,
            gender: gender,
            height: height,
            city: city,
            date_of_birth: dateOfBirth,
            profile_picture: profilePicture
        };

        for (const key in fields) {
            const value = fields[key];

            if (value && !validateField(key, value)) {
                setErrorMessage(`Champ invalide : ${key}`);
                return false;
            }
        }
        setErrorMessage("");
        return true;
    }

    async function onSubmit(event) {
        event.preventDefault();

        if (!validateForm()) return;

        const rawData = {
            ...formData,
            first_name: firstName,
            last_name: lastName,
            gender,
            height,
            city,
            date_of_birth: dateOfBirth,
            profile_picture: profilePicture
        };

        // Mise à jour de l’objet dans le parent
        updateFormData(rawData);

        formatData("user", rawData, async function(formattedData) {
            try {
                await handleSubmit(formattedData);
                setSuccessMessage("Profil mis à jour avec succès !");
                setErrorMessage("");
            } catch (error) {
                console.error("Erreur lors de la mise à jour :", error);
                setErrorMessage("Une erreur est survenue lors de la mise à jour du profil.");
            }
        });
    }

    return (
        <form onSubmit={onSubmit} className="profile-update">
            <header className="profile-update__header">
                <div className="profile-upload__profile-picture">
                    <input
                        type="file"
                        id="profilePicture"
                        name="profile_picture"
                        className="profile-upload__input"
                        accept="image/*"
                        onChange={handleChange}
                    />
                    <label htmlFor="profilePicture" className="profile-upload__label">
                        <div className="profile-upload__circle">
                            {preview ? (
                                <img src={preview} alt="Aperçu" className="profile-upload__preview" />
                            ) : (
                                <img src={user?.profile_picture} alt="Profil" className="profile-upload__avatar" />
                            )}
                            <div className="profile-upload__icon">
                                <img src={ModifyIcon} alt="Icône modification" />
                            </div>
                        </div>
                    </label>
                </div>
                <h2 className="header-dashboard__greeting">{user?.username}</h2>
                <div className="profile-update__navigation">
                    <button
                        type="button"
                        className="profile__button profile-update__button--secondary"
                    >
                        Informations personnelles
                    </button>
                    <button
                        type="button"
                        onClick={nextStep}
                        className="profile__button profile-medication__button--secondary"
                    >
                        Médications et posologies
                    </button>
                </div>
            </header>
            <div className="profile-update__body">
                <div className="profile-update__body-form">
                    <input
                        name="first_name"
                        type="text"
                        value={firstName}
                        placeholder={user?.first_name}
                        onChange={handleChange}
                    />
                </div>
                <div className="profile-update__body-form">
                    <input
                        name="last_name"
                        type="text"
                        value={lastName}
                        placeholder={user?.last_name}
                        onChange={handleChange}
                    />
                </div>
                <div className="profile-update__body-form">
                    <input
                        name="height"
                        type="number"
                        value={height}
                        placeholder={user?.height}
                        onChange={handleChange}
                    />
                </div>
                <div className="profile-update__body-form">
                    <input
                        name="city"
                        type="text"
                        value={city}
                        placeholder={user?.city}
                        onChange={handleChange}
                    />
                </div>
                <div className="profile-update__body-form">
                    <input
                        name="date_of_birth"
                        type="date"
                        value={dateOfBirth}
                        placeholder={user?.date_of_birth}
                        onChange={handleChange}
                    />
                </div>
                <div className="profile-update__body-form">
                    <select
                        name="gender"
                        value={gender}
                        onChange={handleChange}
                    >
                        <option value="">Genre</option>
                        <option value="male">Homme</option>
                        <option value="female">Femme</option>
                        <option value="other">Autre</option>
                        <option value="prefer_not_say">Préfère ne pas répondre</option>
                    </select>
                </div>
                {errorMessage && (
                    <p className="profile-update__message profile-update__message--error">
                        {errorMessage}
                    </p>
                )}
                {successMessage && (
                    <p className="profile-update__message profile-update__message--success">
                        {successMessage}
                    </p>
                )}
            </div>
            <button type="submit" className="profile-update__button">
                Modifier
            </button>
        </form>
    );
}

export default ProfileUpdate;
