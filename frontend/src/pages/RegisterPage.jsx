import React, {useState} from "react";

import FormPart1 from "../components/RegisterPage/FormPart1";
import FormPart2 from "../components/RegisterPage/FormPart2";

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
        <div>
            <h1>Avec quels identifiants veux tu te connecter ?</h1>
            <FormPart1 formData={formData} updateFormData={updateFormData} nextStep={nextStep} />
        </div>
    );
  }
  if (step === 2) {
    return (
        <div>
            <h1>Entre tes informations personnelles</h1>
            <FormPart2 formData={formData} updateFormData={updateFormData} prevStep={prevStep} handleSubmit={handleSubmit} />
        </div>
    );
  }

  // Envoie une erreur si ça se passe mal
  return (
    <div>
        <p>Erreur: étape inconnue</p>
    </div>
  )
}

export default RegisterPage;
