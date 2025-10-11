from flask import current_app as app
from app.models.base import BaseModel
from app import db

class Medication(BaseModel):
    __tablename__ = "medications"

    UNIT = "mg"

    _name = db.Column(db.String(100), nullable=False)
    _dose = db.Column(db.Integer, nullable=False)
    _stock = db.Column(db.Integer, nullable=False)
    _frequency = db.Column(db.Enum("once_a_day", "twice_a_day", "three_times_a_day", "as_needed"), nullable=False)
    _alert_threshold = db.Column(db.Integer, default=1000)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            app.logger.error("[BACK][models/Medication][name.setter] Le nom du médicament doit être une chaîne de caractères")
            raise TypeError("Le nom du médicament doit être une chaîne de caractères")
        cleaned_name = value.strip()
        if not (2 <= len(cleaned_name) <= 100):
            app.logger.error("[BACK][models/Medication][name.setter] Le nom du médicament doit comporter entre 2 et 100 caractères")
            raise ValueError("Le nom du médicament doit comporter entre 2 et 100 caractères")
        app.logger.info("[BACK][models/Medication][name.setter] Le nom du médicament est valide")
        self._name = cleaned_name.capitalize()  # capitalize() formate le name avec une majuscule en début de mot le reste en minuscule, permet de standardiser

    @property
    def dose(self):
        return self._dose

    @dose.setter
    def dose(self, value):
        if not isinstance(value, int) or value <= 0:
            app.logger.error("[BACK][models/Medication][dose.setter] La dose doit être un entier positif (mg)")
            raise ValueError("La dose doit être un entier positif (mg)")
        app.logger.info("[BACK][models/Medication][dose.setter] La posologie est valide")
        self._dose = value

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        if not isinstance(value, int) or value < 0:
            app.logger.error("[BACK][models/Medication][stock.setter] Le stock doit être un entier positif (mg)")
            raise ValueError("Le stock doit être un entier positif (mg)")
        app.logger.info("[BACK][models/Medication][stock.setter] Le stock est valide")
        self._stock = value

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        allowed = {"once_a_day", "twice_a_day", "three_times_a_day", "as_needed"}
        if not isinstance(value, str):
            app.logger.error(f"[BACK][models/Medication][stock.setter] La fréquence doit être une chaîne de caractères parmi : {allowed}")
            raise TypeError(f"La fréquence doit être une chaîne de caractères parmi : {allowed}")
        if value not in allowed:
            app.logger.error(f"[BACK][models/Medication][stock.setter] La fréquence doit être parmi : {allowed}")
            raise ValueError(f"La fréquence doit être parmi : {allowed}")
        app.logger.info("[BACK][models/Medication][stock.setter] La fréquence de prise est valide")
        self._frequency = value


    def take_dose(self):
        """Soustrait une dose du stock si le stock est suffisant"""
        app.logger.info(f"[BACK][models/Medication][take_dose()] Vérification avant prise : {self._stock} mg disponibles, dose prescrite : {self._dose} mg")
        if not isinstance(self._dose, int) or not isinstance(self._stock, int):
            app.logger.error("[BACK][models/Medication][take_dose()] Types invalides pour dose ou stock")
            raise TypeError("Les attributs 'dose' et 'stock' doivent être des entiers")
        if self._dose <= 0:
            app.logger.error("[BACK][models/Medication][take_dose()] Dose invalide (<= 0)")
            raise ValueError("La dose doit être supérieure à 0 mg")
        if self._stock < 0:
            app.logger.error("[BACK][models/Medication][take_dose()] Stock négatif détecté")
            raise ValueError("Le stock ne peut pas être négatif")
        if self._stock < self._dose:
            app.logger.warning(f"[BACK][models/Medication][take_dose()] Stock insuffisant : {self._stock} mg restants pour une dose de {self._dose} mg")
            raise ValueError(f"Stock insuffisant pour effectuer la prise : {self._stock} mg disponibles pour {self._dose} mg nécessaires")
        old_stock = self._stock
        new_stock = old_stock - self._dose
        self._stock = new_stock
        app.logger.info(f"[BACK][models/Medication][take_dose()] Prise de {self._dose} mg effectuée pour {self._name}. Ancien stock : {old_stock} mg → Nouveau stock : {new_stock} mg")
        if self.alert_low_stock():
            app.logger.warning(f"[BACK][models/Medication][take_dose()] Attention : le stock de {self._name} est bas ({self._stock} mg restants, seuil {self._alert_threshold} mg)")
        try:
            self.save()
            app.logger.info(f"[BACK][models/Medication][take_dose()] Mise à jour sauvegardée pour {self._name} (stock actuel : {self._stock} mg)")
        except Exception as e:
            app.logger.error(f"[BACK][models/Medication][take_dose()] Erreur lors de la sauvegarde du stock : {e}")
            raise


    def alert_low_stock(self):
        """Retourne True si le stock est inférieur au seuil d’alerte"""
        current_stock = self._stock
        threshold = self._alert_threshold
        app.logger.info(f"[BACK][models/Medication][alert_low_stock()] Vérification du stock : {current_stock} mg, seuil {threshold} mg")
        if current_stock < threshold:
            app.logger.warning(f"[BACK][models/Medication][alert_low_stock()] Stock faible détecté ({current_stock} mg restants)")
            return True
        app.logger.info("[BACK][models/Medication][alert_low_stock()] Stock suffisant, aucune alerte nécessaire")
        return False
