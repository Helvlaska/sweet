const SPECIALITY_LABELS = {
  general_practitioner: "Médecin généraliste",
  diabetologist: "Diabétologue",
  endocrinologist: "Endocrinologue",
  cardiologist: "Cardiologue",
  ophthalmologist: "Ophtalmologue",
  nephrologist: "Néphrologue",
  podiatrist: "Podologue",
  dentist: "Dentiste",
  dietitian: "Diététicien",
  nurse: "Infirmier",
  psychologist: "Psychologue",
  pharmacist: "Pharmacien",
  physiotherapist: "Kinésithérapeute",
  physical_educator: "Éducateur sportif",
  social_worker: "Assistant social",
  gynecologist: "Gynécologue",
};

function translateSpeciality(value) {
  if (SPECIALITY_LABELS[value]) {
    return SPECIALITY_LABELS[value];
  }

  return value;
}

export { translateSpeciality };
