
// Fonction pour convertir une image en largeBinary
function convertFileToBase64(file, callback) {
    const reader = new FileReader();
    reader.onload = function(event) {
        const base64String = event.target.result.split(",")[1];
        callback(base64String);
    };
    reader.readAsDataURL(file);
}


// Fonction pour formater les données du user
function formatUser(data, callback) {
    const formatted = { ...data };

    if (formatted.height) {
        formatted.height = parseInt(formatted.height, 10);
    }
    if (formatted.date_of_birth instanceof Date) {
        formatted.date_of_birth = formatted.date_of_birth.toISOString().split("T")[0];
    }
    if (formatted.profile_picture instanceof File) {
        console.log(
            "DEBUG formatUser → type de profile_picture :",
            typeof formatted.profile_picture,
            formatted.profile_picture
        );
        convertFileToBase64(formatted.profile_picture, function(base64Image) {
            formatted.profile_picture = base64Image;
            callback(formatted);
        });
        return;
    }

    callback(formatted);
}


// Fonction pour formater les données de santé
function formatDataEntry(data) {
    const formatted = { ...data };

    if (formatted.glycemia) {
        formatted.glycemia = parseInt(formatted.glycemia, 10);
    }
    if (formatted.weight) {
        formatted.weight = parseFloat(formatted.weight);
    }
    if (formatted.activity && formatted.activity.duration) {
        formatted.activity.duration = parseInt(formatted.activity.duration, 10);
    }
    if (formatted.medication) {
        formatted.medication.dose = parseInt(formatted.medication.dose, 10);
        formatted.medication.stock = parseInt(formatted.medication.stock, 10);
    }

    return formatted;
}


// Fonction pour formater les infos des professionels de santé
function formatProfessional(data) {
    const formatted = { ...data };

    return formatted;
}

// Fonction pour formater les données de type texte
function formatContent(data) {
    const formatted = { ...data };
    for (const key in formatted) {
        if (typeof formatted[key] === "string") {
            formatted[key] = formatted[key].trim();
        }
    }

    return formatted;
}

// Fonction toggle pour envoyé la bonne fonction selon le besoin
function formatData(entity, data, callback) {
    switch (entity) {
        case "user":
            return formatUser(data, callback);

        case "data":
            return callback(formatDataEntry(data));

        case "professional":
            return callback(formatProfessional(data));

        case "forum":
        case "article":
        case "comment":
            return callback(formatContent(data));

        default:
            return callback(data);
    }
}

export { formatData };
