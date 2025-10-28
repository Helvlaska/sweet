import { isValid, makeContentPattern, makeIdentityPattern } from "../validator.jsx";

function validateData(name, value) {
    switch (name) {
        case "activity": {
            if (typeof value !== "object" || value === null) {
                return false;
            }
            const { description, duration } = value;
            const allowedActivities = [
                "marche", "natation", "vélo", "yoga", "pilates", "renforcement",
                "jardinage", "bricolage", "ménage", "escaliers"
            ];
            if (!allowedActivities.includes(description)) {
                return false;
            }
            if (isNaN(duration)) {
                return false;
            }
            const durationValue = Number(duration);
            return durationValue > 0 && durationValue <= 600;
        }

        case "glycemia": {
            if (value === null || value === undefined) {
                return false;
            }
            if (isNaN(value)) {
                return false;
            }
            const glucoseValue = Number(value);
            return glucoseValue >= 50 && glucoseValue <= 350;
        }

        case "weight": {
            if (value === null || value === undefined) {
                return false;
            }
            if (isNaN(value)) {
                return false;
            }
            const massValue = parseFloat(value);
            return massValue >= 1.0 && massValue <= 400.0;
        }

        case "meal": {
            if (typeof value !== "object" || value === null) {
                return false;
            }
            const { meal_type, description } = value;
            const allowedMeals = ["breakfast", "lunch", "dinner", "snack"];
            if (!allowedMeals.includes(meal_type)) {
                return false;
            }
            const DESCRIPTION_PATTERN = makeContentPattern(300, 2, true);
            return isValid(description, DESCRIPTION_PATTERN);
        }

        case "medication": {
            if (typeof value !== "object" || value === null) {
                return false;
            }
            const { name, dose, stock, frequency } = value;
            const allowedFrequencies = [
                "once_a_day", "twice_a_day", "three_times_a_day", "as_needed"
            ];
            const NAME_PATTERN = makeIdentityPattern(100, 2);
            if (!isValid(name, NAME_PATTERN)) {
                return false;
            }
            if (isNaN(dose) || isNaN(stock)) {
                return false;
            }
            const doseValue = Number(dose);
            const stockValue = Number(stock);
            if (doseValue <= 0 || stockValue < 0) {
                return false;
            }
            return allowedFrequencies.includes(frequency);
        }

        case "mood": {
            const allowedMoods = [
                "Joyeux", "Calme", "Motivé", "Fatigué", "Anxieux",
                "Irritable", "Déprimé", "Neutre"
            ];
            return allowedMoods.includes(value);
        }

        default:
            return true;
    }
}

export { validateData };
