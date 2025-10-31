import React, {useState} from "react";

// import des formulaires
import FormPart1 from "../components/RegisterPage/FormPart1";
import FormPart2 from "../components/RegisterPage/FormPart2";

// import des images
import redCross from "../assets/icones/red-cross.png";

function RegisterPage() {
    // Détermine quelle sous page useState doit afficher: useState(1) = Step1
    const [step, setStep] = useState(1);

    // Préparation de l'objet qui contiendra toutes les infos du user
    const [formData, setFromData] = useState({
        email: "",
        username: "",
        password: "",
        first_name: "",
        last_name: "",
        gender: "",
        height: 0,
        city: "",
        date_of_birth: "",
        profile_picture: null
    });

    // Fonction pour switcher entre les sous pages
    function nextStep() {
        setStep(step + 1);
    }
    function prevStep() {
        setStep(step - 1);
    }

    // Fonction pour ajouter en deux fois les données dans l'objet
    function updateFormData(newData) {
        setFromData({
            ...formData,
            ...newData
        });
    }

    // Fonction pour envoyer les données vers la route de création du user
    function handleSubmit() {
        console.log("Formulaire complet:", formData);
    }

    // Affichage des sous pages
    if (step === 1) {
        return (
            <main className="register-page">
                <section className="register">
                    <FormPart1 formData={formData} updateFormData={updateFormData} nextStep={nextStep} />
                </section>
            </main>
        );
    }
    if (step === 2) {
        return (
            <main className="register-page">
                <section className="register">
                    <FormPart2 formData={formData} updateFormData={updateFormData} prevStep={prevStep} handleSubmit={handleSubmit} />
                </section>
            </main>
        );
    }

    // Envoie une erreur si ça se passe mal
    return (
        <main className="register-page">
            <section className="register">
                <img src= {redCross} />
                <p className="register__error">Erreur : étape inconnue</p>
            </section>
        </main>
    );
}

export default RegisterPage;
