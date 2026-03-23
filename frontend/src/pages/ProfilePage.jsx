import React, { useState } from "react";

// Import des sous-pages et composants
import ProfilPageUpdate from "../components/ProfilePage/profileUpdate";
import ProfilPageMedication from "../components/ProfilePage/profileMedication";
import NavBar from "../components/NavBar/NavBar";

// Import des services backend
import { authPrivateService } from "../services/auth/authPrivateService";
import { medicationService } from "../services/health/medicationService";

function ProfilePage() {
    // Détermine quelle sous-page afficher (1 = profil, 2 = médicaments)
    const [step, setStep] = useState(1);

    // Données du profil utilisateur
    const [userData, setUserData] = useState({
        first_name: "",
        last_name: "",
        gender: "",
        height: 0,
        city: "",
        date_of_birth: "",
        profile_picture: null
    });

    // Données du médicament
    const [medicationData, setMedicationData] = useState({
        name: "",
        dose: "",
        stock: "",
        frequency: ""
    });

    function nextStep() {
        setStep(2);
    }

    function prevStep() {
        setStep(1);
    }

    function updateUserData(newData) {
        setUserData((prevData) => ({
            ...prevData,
            ...newData
        }));
    }

    function updateMedicationData(newData) {
        setMedicationData((prevData) => ({
            ...prevData,
            ...newData
        }));
    }

    // Met à jour le profil utilisateur
    async function handleUpdateSubmit(userData) {
        try {
            const response = await authPrivateService.update_profile(userData);
            console.log("Profil mis à jour :", response);
            alert("Profil mis à jour avec succès !");
        } catch (error) {
            console.error("Erreur lors de la mise à jour du profil :", error);
            alert("Une erreur est survenue lors de la mise à jour du profil.");
        }
    }

    // Ajoute un médicament
    async function handleMedicationSubmit(medicationData) {
        try {
            const response = await medicationService.create_medication_entry(medicationData);
            console.log("Médicament ajouté :", response);
            alert("Médicament ajouté avec succès !");
        } catch (error) {
            console.error("Erreur lors de l’ajout du médicament :", error);
            alert("Une erreur est survenue lors de l’ajout du médicament.");
        }
    }

    return (
        <div className="profile-page">
            <NavBar />

            {step === 1 && (
                <main className="profile__update">
                    <section className="update">
                        <ProfilPageUpdate
                            formData={userData}
                            updateFormData={updateUserData}
                            handleSubmit={handleUpdateSubmit}
                            nextStep={nextStep}
                        />
                    </section>
                </main>
            )}

            {step === 2 && (
                <main className="profile__medication">
                    <section className="medication">
                        <ProfilPageMedication
                            formData={medicationData}
                            updateFormData={updateMedicationData}
                            handleSubmit={handleMedicationSubmit}
                            prevStep={prevStep}
                        />
                    </section>
                </main>
            )}
        </div>
    );
}

export default ProfilePage;
