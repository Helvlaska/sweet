import React, { useState, useEffect } from "react";
import { validateField } from "../../utils/validator";
import { formatData } from "../../utils/dataFormatter";
import { medicationService } from "../../services/medicationService";
import { useAuth } from "../../context/AuthContext";

// import image et icones
import DeleteIcon from "../../assets/profile/ProfileIconTrash.png";
import AddIcon from "../../assets/profile/ProfileIconValider.png"

function ProfileMedication({ formData, updateFormData, handleSubmit, prevStep }) {
    const {user} = useAuth();

    const [name, setName] = useState("");
    const [dose, setDose] = useState("");
    const [stock, setStock] = useState("");
    const [frequency, setFrequency] = useState("");

    const [errorMessage, setErrorMessage] = useState("");

    const [medicationsList, setMedicationsList] = useState([]);

    useEffect(() => {
        async function fetchMedications() {
            try {
                const response = await medicationService.get_medication_entries();
                setMedicationsList(response.data || []);
            } catch (error) {
                console.error("Erreur lors du chargement des médicaments :", error);
            }
        }
        fetchMedications();
    }, []);

    function validateForm() {
        const fields = { name, dose, stock, frequency };
        for (const key in fields) {
            if (!validateField(key, fields[key])) {
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
            name,
            dose: parseInt(dose),
            stock: parseInt(stock),
            frequency,
            alert_threshold: 1000
        };

        updateFormData(rawData);
        formatData("medication", rawData, async function(formattedData) {
            try {
                await handleSubmit(formattedData);

                // Recharge la liste après ajout
                const updatedList = await medicationService.get_medication_entries();
                setMedicationsList(updatedList.data || []);

                setErrorMessage("");
                setName("");
                setDose("");
                setStock("");
                setFrequency("");
            } catch (error) {
                console.error("Erreur lors de l’ajout :", error);
                setErrorMessage("❌ Une erreur est survenue lors de l’ajout du médicament.");
            }
        });

        setErrorMessage("");
        setName("");
        setDose("");
        setStock("");
        setFrequency("");

        // Recharge la liste après ajout
        const updatedList = await medicationService.get_medication_entries();
        setMedicationsList(updatedList.data || []);
    }

    async function handleDelete(id) {
        try {
            await medicationService.delete_medication_entry(id);
            setMedicationsList(medicationsList.filter((med) => med.id !== id));
        } catch (error) {
            console.error("Erreur lors de la suppression :", error);
        }
    }

    return (
        <div className="profile-medication">
            <header className="profile-medication__header">
                <img src={user?.profile_picture} alt="Profil" className="profile-medication__avatar" />
                <h2 className="header-dashboard__greeting">{user?.username}</h2>
                <div className="profile-medication__navigation">
                    <button
                        type="button"
                        onClick={prevStep}
                        className="profile-medication__button profile-update__button--secondary"
                    >
                        Informations personnelles
                    </button>
                    <button
                        type="button"
                        className="profile-medication__button profile-medication__button--secondary"
                    >
                        Médications et posologies
                    </button>
                </div>
            </header>
            <div className="profile-medication__body">
                <section className="profile-medication__list">
                    {medicationsList.length === 0 ? (
                        <p className="profile-medication__empty">Aucun médicament enregistré pour l’instant.</p>
                    ) : (
                        <ul className="medication-list">
                            {medicationsList.map((med) => (
                                <li key={med.id} className="medication-card">
                                    <div className="medication__card-item">
                                        {med.name}
                                    </div>
                                    <div  className="medication__card-item">
                                        Dose: {med.dose} mg/{med.frequency.replaceAll("_", " ")}
                                    </div>
                                    <div  className="medication__card-item">
                                        Stock : {med.stock}
                                    </div>
                                    <button
                                        className="medication-card__delete"
                                        onClick={() => handleDelete(med.id)}
                                    >
                                        <img src={DeleteIcon} className="profile-medication__button-img"/>
                                    </button>
                                </li>
                            ))}
                        </ul>
                    )}
                </section>
                <form onSubmit={onSubmit} className="profile-medication__form">
                    <div className="profile-medication__form-item">
                        <input
                            name="name"
                            type="text"
                            value={name}
                            placeholder="Nom du médicament"
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </div>
                    <div className="profile-medication__form-item">
                        <input
                            name="dose"
                            type="number"
                            value={dose}
                            placeholder="Dose (mg)"
                            onChange={(e) => setDose(e.target.value)}
                            required
                        />
                    </div>
                    <div className="profile-medication__form-item">
                        <input
                            name="stock"
                            type="number"
                            value={stock}
                            placeholder="Stock (mg)"
                            onChange={(e) => setStock(e.target.value)}
                            required
                        />
                    </div>
                    <div className="profile-medication__form-item">
                        <select
                            name="frequency"
                            value={frequency}
                            onChange={(e) => setFrequency(e.target.value)}
                            required
                        >
                            <option value="">Fréquence de prise</option>
                            <option value="once_a_day">1 fois / jour</option>
                            <option value="twice_a_day">2 fois / jour</option>
                            <option value="three_times_a_day">3 fois / jour</option>
                            <option value="as_needed">Selon besoin</option>
                        </select>
                    </div>
                    <button type="submit" className="profile-medication__button">
                            <img src={AddIcon} className="profile-medication__button-img"/>
                    </button>
                </form>
                {errorMessage && (
                    <p className="profile-medication__message profile-medication__message--error">
                        {errorMessage}
                    </p>
                )}
            </div>
        </div>
    );
}

export default ProfileMedication;
