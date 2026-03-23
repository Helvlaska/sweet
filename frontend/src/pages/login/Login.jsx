/**
 * SWEET — Login Page (Structure)
 * ==============================
 * Page component representing the user login form.
 *
 * Role:
 * -----
 * - Display the login form.
 * - Structure authentication fields and related actions.
 * - Delegate all business logic to the useLogin hook.
 *
 * Content:
 * --------
 * - Authentication fields:
 *   - Email or username (either one).
 *   - Password with conditional visibility.
 * - "Remember me" option.
 * - Display of user-facing error messages.
 * - Links to:
 *   - Password reset page.
 *   - Registration page.
 * - Dynamic illustration linked to password visibility.
 *
 * Interaction:
 * ------------
 * - Events (change, submit, password toggle)
 *   are handled by the useLogin hook.
 * - This component contains no validation logic
 *   and no API calls.
 *
 * Architecture:
 * -------------
 * - Business logic is centralized in useLogin.js.
 * - Navigation is handled via React Router (<Link />).
 * - Button and Icon components come from the SWEET Design System.
 * - Styles are defined in the associated SCSS file.
 *
 * Maintenance:
 * ------------
 * - Any change to the authentication flow must be done
 *   in the useLogin hook.
 * - Changes in this file must remain structural (JSX).
 * - Visual elements must remain consistent with the Design System.
 */


import { Link } from "react-router-dom";
import { useLogin } from "./useLogin";

import imgLoginOpen from "../../assets/login/mascot-eyes-open.webp";
import imgLoginClose from "../../assets/login/mascot-eyes-closed.webp";
import Button from "../../components/Button/buttons";
import Icon from "../../components/Icon/Icons";

function Login() {
  const {
    email,
    username,
    password,
    rememberMe,
    showPassword,
    errors,

    handleChange,
    togglePasswordVisibility,
    handleSubmit,
  } = useLogin();

  return (
    <div className="login">
      <form onSubmit={handleSubmit} className="login__form">
        <div className="login__form--wrapper">
          <div className="login__group">
            <input
              id="email"
              name="email"
              type="email"
              value={email}
              onChange={handleChange}
              placeholder="Adresse mail"
              className="login__input"
            />
          </div>

          <div className="login__separator">
            <div className="login__separator-line"></div>
            <p className="login__separator-text">ou</p>
            <div className="login__separator-line"></div>
          </div>

          <div className="login__group">
            <input
              id="username"
              name="username"
              type="text"
              value={username}
              onChange={handleChange}
              placeholder="Nom d'utilisateur"
              className="login__input"
            />
          </div>
        </div>

        <div className="login__group login__group--password">
          <input
            id="password"
            name="password"
            type={showPassword ? "text" : "password"}
            value={password}
            onChange={handleChange}
            placeholder="Mot de passe"
            className="login__input"
          />
          <Button>
            <Icon
              name={showPassword ? "eyeOff" : "eye"}
              className="login__icon"
              strokeWidth="1"
              onClick={togglePasswordVisibility}
            />
          </Button>
        </div>

        {errors.length > 0 && (
          <ul className="login__errors">
            {errors.map(function (message, index) {
              return (
                <li key={index} className="login__error">
                  <Icon
                    name="cross" className="login__error-icon"
                  />
                  {message}
                </li>
              );
            })}
          </ul>
        )}

        <div className="login__extras">
          <label htmlFor="rememberMe" className="login__remember">
            <input
              type="checkbox"
              id="rememberMe"
              name="rememberMe"
              checked={rememberMe}
              onChange={handleChange}
              className="login__checkbox"
            />
            &nbsp;Se souvenir de moi
          </label>
          <div className="login__forgot">
            <Link to="/forgot-password" className="login__forgot-link">
              Mot de passe oublié ?
            </Link>
          </div>
        </div>

        <div className="login__actions">
          <Button type="submit" className="btn-pill-outline-blue">
            Se connecter
          </Button>
        </div>

        <div className="login__cta">
          <p>
            Pas encore de compte ?{" "}
            <Link to="/register" className="login__link">
              Inscription ici.
            </Link>
          </p>
        </div>
      </form>

      <div className="login__illustration">
        <img
          src={showPassword ? imgLoginClose : imgLoginOpen}
          alt="Mascotte Sweet en train de dire bonjour"
          className="login__mascot"
        />
      </div>
    </div>
  );
}

export default Login;
