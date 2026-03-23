from app import db
from app.models.user import User
from app.models.glycemia import Glycemia
from app.models.weight import Weight
from app.models.activity import Activity
from app.models.meal import Meal
from app.models.mood import Mood
from app.models.medication import Medication
from app.models.health_professional import HealthProfessional
from app.models.health_document import HealthDocument
from app.models.note import Note
from app.models.forum_post import ForumPost
from app.models.comment import Comment
from app.models.article import Article


__all__ = ["User", "Glycemia", "Weight", "Activity", "Meal", "Mood", "Medication", "HealthProfessional", "HealthDocument", "Note", "ForumPost", "Comment", "Article"]


user_likes_post = db.Table(
    "user_likes_post",
    db.Column("user_id", db.String(36), db.ForeignKey("users.id"), primary_key=True),
    db.Column("post_id", db.String(36), db.ForeignKey("forum_posts.id"), primary_key=True)
)

user_likes_comment = db.Table(
    "user_likes_comment",
    db.Column("user_id", db.String(36), db.ForeignKey("users.id"), primary_key=True),
    db.Column("comment_id", db.String(36), db.ForeignKey("comments.id"), primary_key=True)
)

user_likes_article = db.Table(
    "user_likes_article",
    db.Column("user_id", db.String(36), db.ForeignKey("users.id"), primary_key=True),
    db.Column("article_id", db.String(36), db.ForeignKey("articles.id"), primary_key=True)
)
