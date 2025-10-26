import { useState } from "react";
import { authService } from "../../services/authService";
import { validateField } from "../../utils/validator";
import { formatData } from "../../utils/dataFormatter";
import { Navigate } from "react-router-dom";

function FormPart2Logic(formData, updateFormData) {
    const [firstName, setFirstName] = useState(formData.first_name || "");
    const [lastName, setLastName] = useState(formData.last_name || "");
    const [gender, setGender] = useState(formData.gender || "");
    const [height, setHeight] = useState(formData.height || "");
    const [city, setCity] = useState(formData.city || "");
    const [dateOfBirth, setDateOfBirth] = useState(formData.date_of_birth || "");
    const [profilePicture, setProfilePicture] = useState(null);

    const [errorMessage, setErrorMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");

    function handleChange(event) {
        const { name, value, files } = event.target;
        console.log("[handleChange] name:", name, "value:", value, "type:", typeof value);

        if (name === "first_name") setFirstName(value);
        if (name === "last_name") setLastName(value);
        if (name === "gender") setGender(value);
        if (name === "height") setHeight(value);
        if (name === "city") setCity(value);
        if (name === "date_of_birth") setDateOfBirth(value);
        if (name === "profile_picture" && files && files[0]) {
            setProfilePicture(files[0]);
        }

        // Validation immédiate
        const isValid = validateField(name, value);
        if (!isValid) {
            setErrorMessage("Champ invalide : " + name);
        } else {
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
            date_of_birth: dateOfBirth
        };

        for (const key in fields) {
            if (!validateField(key, fields[key])) {
                setErrorMessage("Champ invalide : " + key);
                return false;
            }
        }

        setErrorMessage("");
        return true;
    }

    function handleSubmit(event) {
        event.preventDefault();

        if (!validateForm()) {
            return;
        }

        const rawData = {
            ...formData,
            first_name: firstName,
            last_name: lastName,
            gender: gender,
            height: height,
            city: city,
            date_of_birth: dateOfBirth,
            profile_picture: profilePicture
        };

        updateFormData(rawData);

        formatData("user", rawData, async function(formattedData) {
            try {
                const registerResponse = await authService.register(formattedData);
                console.log("Inscription réussie :", registerResponse.data);
                setSuccessMessage("Compte créé avec succès !");
                setErrorMessage("");

                // connexion auto
                const loginData = {
                email: formattedData.email,
                password: formattedData.password,
                };
                const loginResponse = await authService.login(loginData);
                console.log("Connexion automatique réussie :", loginResponse.data);

                Navigate("/dashboard");
            } catch (error) {
                console.log(error);
                setErrorMessage("Erreur lors de la création ou de la connexion du compte.");
                setSuccessMessage("");
            }
        });
    }

    return {
        firstName, lastName, gender, height, city, dateOfBirth, profilePicture,
        errorMessage, successMessage,
        handleChange, handleSubmit
    };
}

export { FormPart2Logic };
