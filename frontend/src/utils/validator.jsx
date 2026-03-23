import { validateUser } from "./validator/validateUser";
import { validateData } from "./validator/validateData";
import { validateForum } from "./validator/validateForum";
import { validateProfessional } from "./validator/validateProfessional";
import { validateArticle } from "./validator/validateArticle";


// Fonction pour vérifier les champs d'identification
function makeIdentityPattern(maxLength, minLength = 1) {
    const pattern = "^[\\wÀ-ÿ .,'’\\-]{" + minLength + "," + maxLength + "}$";
    return new RegExp(pattern, "u");
}


// Fonction pour vérifier les champs texte
function makeContentPattern(maxLength, minLength = 1, multiline = false) {
    const baseChars = "\\wÀ-ÿ .,!?;:'\"()\\-";
    const pattern = multiline
        ? "^[ " + baseChars + "\\n]{" + minLength + "," + maxLength + "}$"
        : "^[ " + baseChars + "]{" + minLength + "," + maxLength + "}$";
    return new RegExp(pattern, "u");
}


// Fonction modulable de vérification de Regex
function isValid(value, pattern) {
    if (typeof value !== "string") {
        return false;
    }
    return pattern.test(value);
}

export { makeIdentityPattern, makeContentPattern, isValid };


// Champs d'identité
const USERNAME_PATTERN = /^[a-zA-Z0-9._-]{3,30}$/;
const EMAIL_PATTERN = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
const PASSWORD_PATTERN = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
const PROFILE_URL_PATTERN = /^https?:\/\/[^\s]{1,2000}$/;
const PHONE_PATTERN = /^(?:\+|00)?\d[\d\s-]{7,19}$/;

// Champs texte simples
const FIRSTNAME_PATTERN = makeIdentityPattern(75);
const LASTNAME_PATTERN = makeIdentityPattern(100);
const CITY_PATTERN = makeIdentityPattern(120);

// Champs forum et articles
const FORUM_TITLE_PATTERN = makeContentPattern(150, 2);
const FORUM_CONTENT_PATTERN = makeContentPattern(10000, 2, true);

const COMMENT_CONTENT_PATTERN = makeContentPattern(2000, 3, true);

const ARTICLE_TITLE_PATTERN = makeContentPattern(200, 5);
const ARTICLE_CONTENT_PATTERN = makeContentPattern(50000, 20, true);

export { USERNAME_PATTERN, EMAIL_PATTERN, PASSWORD_PATTERN, PROFILE_URL_PATTERN, PHONE_PATTERN, FIRSTNAME_PATTERN, LASTNAME_PATTERN, CITY_PATTERN, FORUM_TITLE_PATTERN, FORUM_CONTENT_PATTERN, COMMENT_CONTENT_PATTERN, ARTICLE_TITLE_PATTERN, ARTICLE_CONTENT_PATTERN };


// Fonction toggle pour vérifier les données (bornages, champs vides)
function validateField(name, value) {

    // Nettoyage de base pour les strings
    if (typeof value === "string") {
        value = value.trim();
    }

    if ([
        "email", "username", "password", "first_name", "last_name",
        "date_of_birth", "gender", "height", "city", "profile_picture"
    ].includes(name)) {
        return validateUser(name, value);
    }

    if ([
        "glycemia", "weight", "activity", "meal", "medication", "mood"
    ].includes(name)) {
        return validateData(name, value);
    }

    if ([
        "forum_post_title", "forum_post_content", "comment_content"
    ].includes(name)) {
        return validateForum(name, value);
    }

    if ([
        "fullname", "speciality", "phone", "note_title", "note_content"
    ].includes(name)) {
        return validateProfessional(name, value);
    }

    if ([
        "article_title", "article_content"
    ].includes(name)) {
        return validateArticle(name, value);
    }

    // Si aucun cas ne correspond, on renvoie true (pas de vérification spécifique)
    return true;
}

export { validateField };


function checkPasswordRules(password) {
    // Sécurité : toujours travailler avec une string
    if (typeof password !== "string") {
        password = "";
    }

    const hasMinLength = password.length >= 8;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialChar = /[@$!%*?&]/.test(password);

    return {
        hasMinLength,
        hasUppercase,
        hasLowercase,
        hasNumber,
        hasSpecialChar,
    };
}

export { checkPasswordRules };

