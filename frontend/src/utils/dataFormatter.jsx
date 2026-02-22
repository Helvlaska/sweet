
// Fonction pour convertir une image en largeBinary
function convertFileToBase64(file) {
  return new Promise(function (resolve, reject) {
    const reader = new FileReader();

    reader.onload = function (event) {
      const base64String = event.target.result.split(",")[1];
      resolve(base64String);
    };

    reader.onerror = function () {
      reject("Erreur lors de la conversion de l'image.");
    };

    reader.readAsDataURL(file);
  });
}



// Fonction pour formater les données du user
async function formatUser(data) {
  const formatted = { ...data };

  if (formatted.height) {
    formatted.height = parseInt(formatted.height, 10);
  }

  if (formatted.profile_picture instanceof File) {
    const base64Image = await convertFileToBase64(formatted.profile_picture);
    formatted.profile_picture = base64Image;
  }

  return formatted;
}

// Fonction pour formater les documents d'un pro
async function formatProfessional(data) {
  const formatted = { ...data };

  if (
    formatted.documents &&
    Array.isArray(formatted.documents) &&
    formatted.documents.length > 0
  ) {
    const formattedDocuments = [];

    for (let i = 0; i < formatted.documents.length; i++) {
      const file = formatted.documents[i];

      if (file instanceof File) {
        const base64 = await convertFileToBase64(file);

        formattedDocuments.push({
          filename: file.name,
          file: base64,
        });
      }
    }

    formatted.documents = formattedDocuments;
  }

  return formatted;
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
async function formatData(entity, data) {
  switch (entity) {
    case "user":
      return await formatUser(data);

    case "data":
      return formatDataEntry(data);

    case "professional":
      return formatProfessional(data);

    case "forum":
    case "article":
    case "comment":
      return formatContent(data);

    default:
      return data;
  }
}

export {formatData};
