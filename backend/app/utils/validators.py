import re

# ------------------ Générateur de regex texte pour le formulaire d'inscription
def make_identity_pattern(max_length: int, min_length: int = 1) -> str:
    """Génère une regex whitelist pour champs texte. Autorise lettres, chiffres, accents, espaces, tirets, apostrophes"""
    return rf"^[\wÀ-ÿ .,'’\-]{{{min_length},{max_length}}}$"


# --------- Générateur de regex pour les champs texte (Forum, comment, article)
def make_content_pattern(max_length: int, min_length: int = 1, multiline: bool = False) -> str:
    """Génère une regex whitelist pour champs de texte libre (forum, article, commentaire). Autorise lettres, chiffres, accents, ponctuation et espaces. Si multiline=True → autorise les retours à la ligne"""
    base_chars = r"\wÀ-ÿ .,!?;:'\"()\-"
    if multiline:
        return rf"^[{base_chars}\n]{{{min_length},{max_length}}}$"
    return rf"^[{base_chars}]{{{min_length},{max_length}}}$"


# ----------------------------------- Fonction générique de validation de champ
def is_valid(value: str, pattern: str) -> bool:
    """Vérifie si une valeur correspond au pattern regex donné. Retourne True si valide, False sinon"""
    if not isinstance(value, str):
        return False
    return re.fullmatch(pattern, value) is not None


# ----------------------------------------------------------------------- Regex
USERNAME_PATTERN = r"^[a-zA-Z0-9._-]{3,30}$"
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
PROFILE_URL_PATTERN = r"^https?://[^\s]{1,2000}$"

PHONE_PATTERN = r"^(?:\+|00)?\d[\d\s\-]{7,19}$"

FIRSTNAME_PATTERN = make_identity_pattern(75)
LASTNAME_PATTERN = make_identity_pattern(100)
CITY_PATTERN = make_identity_pattern(120)

FORUM_TITLE_PATTERN = make_content_pattern(150, 2)
FORUM_CONTENT_PATTERN = make_content_pattern(10000, 2, multiline=True)

COMMENT_CONTENT_PATTERN = make_content_pattern(2000, 3, multiline=True)

ARTICLE_TITLE_PATTERN = make_content_pattern(200, 5)
ARTICLE_CONTENT_PATTERN = make_content_pattern(50000, 20, multiline=True)
