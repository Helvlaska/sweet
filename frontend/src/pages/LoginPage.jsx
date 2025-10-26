import { useState } from "react";
import { authService } from "../services/authService";

function LoginPage() {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    function handleChange(event) {
        const name = event.target.name;
        const value = event.target.value;
        if (name === "email") {
            setEmail(value);
        }
        else if (name === "username") {
            setUsername(value);
        }
        if (name === "password") {
            setPassword(value);
        }
    }
    const handleSubmit = (event) => {
        event.preventDefault();
        authService.login();
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

            <div>
                <div>
                    <input type="checkbox" id="remindMe" name="remindMe" />
                    <label for="scales">Se souvenir de moi</label>
                </div>

                <a href="*">Mot de passe oublié ?</a>
            </div>


            <div className="form-actions">
                <button type="submit">Se connecter</button>
            </div>

            <div>
                <p>Pas encore de compte ? Inscrit toi
                </p>
            </div>
        </form>
    )
}
export default LoginPage
