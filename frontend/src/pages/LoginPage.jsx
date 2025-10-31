import React,{ useState } from "react";

// Import des outils
import { validateField } from "../utils/validator";
import { formatData } from "../utils/dataFormatter";
import { useAuth } from "../context/AuthContext";
import { Link, useNavigate } from "react-router-dom";

// Import des images
import illustrationLoginOpen from "../assets/login/ConnextionIllustration.png";
import illustrationLoginClose from "../assets/login/ConnextionIllustrationYeuxFerme.png";
import passwordIconOpen from "../assets/icones/eye-open.png";
import passwordIconClose from "../assets/icones/eye-close.png";
import redCross from "../assets/icones/red-cross.png";

function LoginPage() {
    // Stockage des champs du formulaire
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [rememberMe, setRememberMe] = useState(false);

    // Gestion du password visible/invisible
    const [showPassword, setShowPassword] = useState(false);

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

    function togglePasswordVisibility() {
        setShowPassword(!showPassword);
    };

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
        <div className="login">
            <form onSubmit={handleSubmit} className="login__form">
                <div className="login__group">
                    <input id="email" name="email" type="email" value={email} onChange={handleChange} placeholder="Adresse mail" className="login__input" />
                </div>
                <div className="login__group">
                    <input id="username" name="username" type="text" value={username} onChange={handleChange} placeholder="Ou Nom d'utilisateur" className="login__input" />
                </div>
                <div className="login__group login__group--password">
                    <input id="password" name="password" type={showPassword ? "text" : "password"} value={password} onChange={handleChange} placeholder="Mot de passe" className="login__input" />
                    <img
                        src={showPassword ? passwordIconOpen : passwordIconClose}
                        alt={showPassword ? "Icône œil ouvert" : "Icône œil fermé"}
                        className="login__icon"
                        onClick={togglePasswordVisibility} />
                </div>
                {errorMessage &&
                    <p className="login__message login__message--error">
                        <img src= {redCross} className="login__message--error-redcross" />
                        {errorMessage}
                    </p>}
                {successMessage && <p className="login__message login__message--success">{successMessage}</p>}
                <div className="login__extras">
                    <label htmlFor="rememberMe" className="login__remember">
                        <input type="checkbox" id="rememberMe" name="rememberMe" checked={rememberMe} onChange={handleChange} className="login__checkbox" />
                        &nbsp;Se souvenir de moi
                    </label>
                </div>
                <div className="login__actions">
                    <button type="submit" className="login__button">Se connecter</button>
                </div>
                <div className="login__cta">
                    <p>
                        Pas encore de compte ?{" "}
                        <Link to="/register" className="login__link">Inscription ici</Link>
                    </p>
                </div>
            </form>
            <div className="login__illustration">
                <img src={showPassword ? illustrationLoginOpen : illustrationLoginClose} alt="Mascotte Sweet en train de dire bonjour" className="login__mascot" />
            </div>
        </div>
    )
}
export default LoginPage
