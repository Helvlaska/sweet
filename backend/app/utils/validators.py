import re

# --------------------------------------------------- Générateur de regex texte
def make_text_pattern(max_length: int, min_length: int = 1) -> str:
    """
    Génère une regex whitelist pour champs texte.
    Autorise lettres, chiffres, accents, espaces, tirets, apostrophes.
    """
    return rf"^[\wÀ-ÿ .,'’\-]{{{min_length},{max_length}}}$"

# ----------------------------------------------------------------------- Regex
USERNAME_PATTERN = r"^[a-zA-Z0-9._-]{3,30}$"
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
PROFILE_URL_PATTERN = r"^https?://[^\s]{1,2000}$"
FIRSTNAME_PATTERN = make_text_pattern(75)
LASTNAME_PATTERN = make_text_pattern(100)
CITY_PATTERN = make_text_pattern(120)

# ----------------------------------- Fonction générique de validation de champ
def is_valid(value: str, pattern: str) -> bool:
    """
    Vérifie si une valeur correspond au pattern regex donné.
    Retourne True si valide, False sinon.
    """
    if not isinstance(value, str):
        return False
    return re.fullmatch(pattern, value) is not None
