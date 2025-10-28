import { isValid, makeIdentityPattern, makeContentPattern, PHONE_PATTERN } from "../validator.jsx";

function validateProfessional(name, value) {
    switch (name) {
        case "fullname": {
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            const FULLNAME_PATTERN = makeIdentityPattern(100, 2);
            return isValid(value, FULLNAME_PATTERN);
        }

        case "speciality": {
            const allowedSpecialities = [
                "general_practitioner", "diabetologist", "endocrinologist", "cardiologist",
                "ophthalmologist", "nephrologist", "podiatrist", "dentist", "dietitian",
                "nurse", "psychologist", "pharmacist", "physiotherapist", "physical_educator",
                "social_worker", "gynecologist"
            ];
            return allowedSpecialities.includes(value);
        }

        case "phone": {
            if (value === null || value === undefined || value === "") {
                // Champ facultatif → on autorise vide
                return true;
            }
            if (typeof value !== "string") {
                return false;
            }
            return isValid(value, PHONE_PATTERN);
        }

        case "note_title": {
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            const TITLE_PATTERN = makeContentPattern(80, 3);
            return isValid(value, TITLE_PATTERN);
        }

        case "note_content": {
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            const CONTENT_PATTERN = makeContentPattern(1000, 10, true);
            return isValid(value, CONTENT_PATTERN);
        }

        default:
            return true;
    }
}

export { validateProfessional };
