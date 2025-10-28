// utils/validator/validateUser.js

import {EMAIL_PATTERN, USERNAME_PATTERN, PASSWORD_PATTERN, FIRSTNAME_PATTERN, LASTNAME_PATTERN, CITY_PATTERN} from "../validator.jsx";
import { isValid } from "../validator.jsx";

function validateUser(name, value) {
    switch (name) {
        case "email":
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            return isValid(value, EMAIL_PATTERN);

        case "username":
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            return isValid(value, USERNAME_PATTERN);

        case "password":
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            return isValid(value, PASSWORD_PATTERN);

        case "first_name":
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            return isValid(value, FIRSTNAME_PATTERN);

        case "last_name":
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            return isValid(value, LASTNAME_PATTERN);

        case "date_of_birth": {
            if (!value) {
                return false;
            }
            const dateValue = new Date(value);
            const today = new Date();
            const minDate = new Date("1900-01-01");
            return dateValue < today && dateValue > minDate;
        }

        case "gender": {
            const allowedGenders = ["male", "female", "other", "prefer_not_say"];
            return allowedGenders.includes(value);
        }

        case "height": {
            const parsedHeight = parseInt(value, 10);
            if (isNaN(parsedHeight)) {
                return false;
            }
            return parsedHeight >= 30 && parsedHeight <= 300;
        }

        case "city":
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            return isValid(value, CITY_PATTERN);

        case "profile_picture": {
            if (!value) {
                return true;
            }
            if (!(value instanceof File)) {
                return false;
            }
            const allowedTypes = ["image/jpeg", "image/png"];
            const maxSize = 2 * 1024 * 1024; // 2 Mo
            return allowedTypes.includes(value.type) && value.size <= maxSize;
        }

        default:
            return true;
    }
}

export { validateUser };
