# app/seed.py
"""
🌱 Script d’initialisation de la base de données SWEET
-----------------------------------------------------
Ce script crée :
- Un admin et un user de test
- Des données de santé (glycémie, poids, activité)
- Des articles d'information
À exécuter dans un environnement virtuel avec Flask configuré.
"""

from app import create_app, db, bcrypt
from app.models.user import User
from app.models.glycemia import Glycemia
from app.models.weight import Weight
from app.models.activity import Activity
from app.models.article import Article
from datetime import date, datetime, timedelta
import random

# --------------------------------------------------------------
# ⚙️ Création de l'application et du contexte Flask
# --------------------------------------------------------------
app = create_app()

with app.app_context():
    print("🧹 Réinitialisation de la base de données...")
    db.drop_all()
    db.create_all()

    # ----------------------------------------------------------
    # 👑 1. Création de l’administrateur
    # ----------------------------------------------------------
    print("👑 Création de l'administrateur...")

    admin = User(
        email="admin@sweet.fr",
        username="admin",
        password_hash="Admin123!",  # le setter hash automatiquement
        first_name="Admin",
        last_name="Sweet",
        date_of_birth=date(1990, 1, 1),
        gender="female",
        height=165,
        city="Laval",
        profile_picture=None,
        first_login=False,
        role="admin"
    )

    db.session.add(admin)

    # ----------------------------------------------------------
    # 👩‍⚕️ 2. Création d’un utilisateur de test
    # ----------------------------------------------------------
    print("👩‍⚕️ Création du user de test...")

    user = User(
        email="user@sweet.fr",
        username="user",
        password_hash="User123!",
        first_name="Léa",
        last_name="Martin",
        date_of_birth=date(1995, 5, 10),
        gender="female",
        height=160,
        city="Nantes",
        profile_picture=None,
        first_login=False,
        role="user"
    )

    db.session.add(user)
    db.session.commit()

    # ----------------------------------------------------------
    # 📈 3. Génération des données de santé (90 jours)
    # ----------------------------------------------------------
    print("📈 Génération des données de santé pour l'utilisateur...")

    today = datetime.now()
    for i in range(90):
        day = today - timedelta(days=i)

        # Glycémie : valeurs entre 70 et 180 mg/dL
        glycemia_value = random.randint(70, 180)
        gly = Glycemia(
            user_id=user.id,
            glucose_level=glycemia_value,
        )
        db.session.add(gly)

        # Poids : variation légère tous les 2 jours
        if i % 2 == 0:
            weight_value = round(60 + random.uniform(-1.0, 1.0), 1)
            w = Weight(
                user_id=user.id,
                mass=weight_value,
            )
            db.session.add(w)

        # Activité : aléatoire un jour sur deux
        if random.random() > 0.5:
            activity_type = random.choice(["marche","natation","vélo","yoga", "pilates", "renforcement", "jardinage", "bricolage", "ménage", "escaliers"])
            duration = random.randint(20, 90)
            act = Activity(
                user_id=user.id,
                description=activity_type,
                duration=duration,
            )
            db.session.add(act)

    # ----------------------------------------------------------
    # 📰 4. Création d’articles pour l’admin
    # ----------------------------------------------------------
    print("📰 Création d'articles d'information...")

    articles = [
        Article(
            user_id=admin.id,
            title="Comprendre sa glycémie",
            content=(
                "Apprenez à interpréter vos mesures et à identifier les variations liées à votre alimentation, votre stress ou votre activité. "
            )
        ),
        Article(
            user_id=admin.id,
            title="Comprendre sa glycémiee",
            content=(
                "Découvrez comment équilibrer vos repas sans frustration, en privilégiant les aliments à faible indice glycémique. "
            )
        ),
        Article(
            user_id=admin.id,
            title="Comprendre sa glycémie",
            content=(
                "Marche, yoga, natation… une activité douce et régulière aide à stabiliser votre glycémie tout en améliorant votre bien-être. "
            )
        ),
    ]
    db.session.add_all(articles)

    # ----------------------------------------------------------
    # 💾 5. Validation et résumé
    # ----------------------------------------------------------
    db.session.commit()

    print("\n✅ Base de données initialisée avec succès !")
    print("-----------------------------------------------------")
    print("👑 Admin → email: admin@sweet.fr | mdp: Admin123!")
    print("👩‍⚕️ User  → email: user@sweet.fr  | mdp: User123!")
    print("-----------------------------------------------------")
    print("📊 Données de santé créées pour 90 jours.")
    print("📰 Articles admin disponibles pour affichage.")
    print("-----------------------------------------------------")
