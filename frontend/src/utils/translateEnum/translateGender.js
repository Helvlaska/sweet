export const GENDER_LABELS = {
  male: "Homme",
  female: "Femme",
  other: "Autre",
  prefer_not_say: "Ne pas préciser",
};

function translateGender(value) {
  if (GENDER_LABELS[value]) {
    return GENDER_LABELS[value];
  }

  return value;
}

export { translateGender };
