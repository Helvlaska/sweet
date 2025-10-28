import React,{ useState } from "react";

// Import des outils
import { validateField } from "../utils/validator";
import { formatData } from "../utils/dataFormatter";
import { useAuth } from "../context/AuthContext";
import { Link, useNavigate } from "react-router-dom";

function LoginPage() {
    // Stockage des champs du formulaire
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [rememberMe, setRememberMe] = useState(false);

    // Gestion des succes/error messages
    const [errorMessage, setErrorMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");

    // Gestion de la redirection
    const navigate = useNavigate();
    const {login} = useAuth();

    // Fonction pour écouter les changements dans le formulaire
    function handleChange(event) {
        // Cible les clefs/valeurs dans les champs du formulaire
        const name = event.target.name;
        const value = event.target.value;
        const type = event.target.type;
        const checked = event.target.checked;

        if (type === "checkbox") {
            setRememberMe(checked);
            return;
        }
        if (name === "email") {
            setEmail(value);
        }
        else if (name === "username") {
            setUsername(value);
        }
        if (name === "password") {
            setPassword(value);
        }

        // Validation immédiate
        const isValid = validateField(name, value);
        if (!isValid) {
            setErrorMessage("Champ invalide : " + name);
        } else {
            setErrorMessage("");
        }
    }

    // Vérification du contenu des champs
    function validateForm() {
        if (!password) {
            setErrorMessage("Le mot de passe est obligatoire.");
            return false;
        }
        if (!email && !username) {
            setErrorMessage("Renseigne l'email OU le nom d'utilisateur.");
            return false;
        }
        if (email && !validateField("email", email)) {
            setErrorMessage("Adresse email invalide.");
            return false;
        }
        if (username && !validateField("username", username)) {
            setErrorMessage("Nom d'utilisateur invalide.");
            return false;
        }
        setErrorMessage("");
        return true;
    }

    // Fonction d'envoie de l'objet vers le backend
    async function handleSubmit(event) {
        event.preventDefault();
        if (!validateForm()) return;

        const rawData = {
        email: email || undefined,
        username: username || undefined,
        password,
        remember_me: rememberMe,
        };

        formatData("user", rawData, async (formattedData) => {
        try {
            await login(formattedData);

            setSuccessMessage("Connexion réussie !");
            setErrorMessage("");

            navigate("/dashboard");
        } catch (err) {
            console.error("[LoginPage] Erreur de connexion :", err);
            setErrorMessage("Identifiants incorrects ou erreur serveur.");
            setSuccessMessage("");
        }
    });
  }
    return (
        <form onSubmit={handleSubmit} className="login">
            <div className="login-group">
                <label></label>
                <input id="email" name="email" type="email" value={email} onChange={handleChange} placeholder="Email" />
            </div>

            <div className="login-group">
                <label></label>
                <input id="username" name="username" type="text" value={username} onChange={handleChange} placeholder="Username" />
            </div>

            <div className="login-group">
                <label></label>
                <input id="password" name="password" type="password" value={password} onChange={handleChange} placeholder="Password" />
            </div>

            <div className="login-extras">
                <label htmlFor="rememberMe">
                    <input type="checkbox" id="rememberMe" name="rememberMe" checked={rememberMe} onChange={handleChange} />
                    &nbsp;Se souvenir de moi
                </label>
            </div>

            {errorMessage && <p className="error-message">{errorMessage}</p>}
            {successMessage && <p className="success-message">{successMessage}</p>}

            <div className="form-actions">
                <button type="submit">Se connecter</button>
            </div>

             <div className="register-cta">
                <p>
                    Pas encore de compte ?
                    <Link to="/register">Inscris-toi</Link>
                </p>
            </div>
        </form>
    )
}
export default LoginPage
