"""
[BACK][seed.py]

Database initialization script for SWEET.
Creates test admin, test user, 90 days of health data, and sample articles.
Run inside the virtual environment with Flask configured.
"""

from app import create_app, db
from app.models.user import User
from app.models.glycemia import Glycemia
from app.models.weight import Weight
from app.models.activity import Activity
from app.models.article import Article
from datetime import date, datetime, timedelta
import random

app = create_app()

with app.app_context():
    print("🧹 Réinitialisation de la base de données...")
    db.drop_all()
    db.create_all()

    # ----------------------------------------------------------
    # 👑 1. Création de l'administrateur
    # ----------------------------------------------------------
    print("👑 Création de l'administrateur...")

    admin = User()
    admin.email = "admin@sweet.fr"
    admin.username = "admin"
    admin.password_hash = "Admin123!"
    admin.first_name = "Admin"
    admin.last_name = "Sweet"
    admin.date_of_birth = date(1990, 1, 1)
    admin.gender = "female"
    admin.height = 165
    admin.city = "Laval"
    admin.first_login = False
    admin.role = "admin"

    db.session.add(admin)

    # ----------------------------------------------------------
    # 👩‍⚕️ 2. Création d'un utilisateur de test
    # ----------------------------------------------------------
    print("👩‍⚕️ Création du user de test...")

    user = User()
    user.email = "user@sweet.fr"
    user.username = "user"
    user.password_hash = "User123!"
    user.first_name = "Léa"
    user.last_name = "Martin"
    user.date_of_birth = date(1995, 5, 10)
    user.gender = "female"
    user.height = 160
    user.city = "Nantes"
    user.first_login = False
    user.role = "user"

    db.session.add(user)
    db.session.commit()

    # ----------------------------------------------------------
    # 📈 3. Génération des données de santé (90 jours)
    # ----------------------------------------------------------
    print("📈 Génération des données de santé pour l'utilisateur...")

    today = datetime.now()

    for i in range(90):
        day = today - timedelta(days=i)
        entry_date = day.date()

        # Glycémie
        gly = Glycemia()
        gly.user_id = user.id
        gly.glucose_level = random.randint(70, 180)
        gly.entry_date = entry_date
        db.session.add(gly)

        # Poids (un jour sur deux)
        if i % 2 == 0:
            w = Weight()
            w.user_id = user.id
            w.mass = round(60 + random.uniform(-1.0, 1.0), 1)
            w.entry_date = entry_date
            db.session.add(w)

        # Activité (aléatoire)
        if random.random() > 0.5:
            act = Activity()
            act.user_id = user.id
            act.description = random.choice([
                "marche", "natation", "vélo", "yoga", "pilates",
                "renforcement", "jardinage", "bricolage", "ménage", "escaliers"
            ])
            act.duration = random.randint(20, 90)
            act.entry_date = entry_date
            db.session.add(act)

    # ----------------------------------------------------------
    # 📰 4. Création d'articles pour l'admin
    # ----------------------------------------------------------
    print("📰 Création d'articles d'information...")

    articles_data = [
        {
            "title": "Comprendre sa glycémie",
            "content": "Apprenez à interpréter vos mesures et à identifier les variations liées à votre alimentation, votre stress ou votre activité physique quotidienne."
        },
        {
            "title": "Alimentation et diabète",
            "content": "Découvrez comment équilibrer vos repas sans frustration, en privilégiant les aliments à faible indice glycémique pour stabiliser votre glycémie."
        },
        {
            "title": "Activité physique et glycémie",
            "content": "Marche, yoga, natation : une activité douce et régulière aide à stabiliser votre glycémie tout en améliorant votre bien-être au quotidien."
        },
    ]

    for data in articles_data:
        article = Article()
        article.user_id = admin.id
        article.title = data["title"]
        article.content = data["content"]
        db.session.add(article)

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
