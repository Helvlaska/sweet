import { useState } from "react";
import { validateField } from "../../utils/validator";
import { formatData } from "../../utils/dataFormatter";
import { authService } from "../../services/authService";

function FormPart1Logic(formData, updateFormData, nextStep) {
    const [email, setEmail] = useState(formData.email || "");
    const [username, setUsername] = useState(formData.username || "");
    const [password, setPassword] = useState(formData.password || "");
    const [errorMessage, setErrorMessage] = useState("");

    function handleChange(event) {
        const { name, value } = event.target;
        if (name === "email") setEmail(value);
        if (name === "username") setUsername(value);
        if (name === "password") setPassword(value);

        const isValid = validateField(name, value);
        setErrorMessage(isValid ? "" : "Champ invalide : " + name);
    }

    async function handleBlur(event) {
        const { name, value } = event.target;
        if (!value.trim()) return;

        try {
            const response = await authService.check_email_username({ [name]: value });
            const data = response.data;
            if (name === "email" && !data.email_available) {
                setErrorMessage("Adresse email déjà utilisée.");
            } else if (name === "username" && !data.username_available) {
                setErrorMessage("Nom d'utilisateur déjà utilisé.");
            } else {
                setErrorMessage("");
            }
        } catch (error) {
            console.log(error);
            setErrorMessage("Erreur lors de la vérification. Réessaie plus tard.");
        }
    }

    function validateForm() {
        if (!validateField("email", email)) {
            setErrorMessage("Adresse email invalide.");
            return false;
        }
        if (!validateField("username", username)) {
            setErrorMessage("Nom d'utilisateur invalide.");
            return false;
        }
        if (!validateField("password", password)) {
            setErrorMessage("Mot de passe invalide.");
            return false;
        }
        setErrorMessage("");
        return true;
    }

    function handleSubmit(event) {
        event.preventDefault();
        if (!validateForm()) return;

        const rawData = { email, username, password };

        formatData("user", rawData, function(formattedData) {
            updateFormData(formattedData);
            nextStep();
        });
    }

    return {
        email, username, password, errorMessage,
        handleChange, handleBlur, handleSubmit
    };
}

export { FormPart1Logic };
