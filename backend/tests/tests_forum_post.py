import json
import pytest
from app import db
from app.models.forum_post import ForumPost
from app.models.user import User


def _std(resp):
    return resp.get_json() if resp.is_json else {}


def _extract_access_cookie(resp):
    cookies = resp.headers.getlist("Set-Cookie")
    for c in cookies:
        if c.startswith("access_token_cookie="):
            return c.split(";", 1)[0].split("=", 1)[1]
    return None


def _forum_post_payload(title="Un post", content="Contenu du post", **overrides):
    base = {
        "title": title,
        "content": content,
    }
    base.update(overrides)
    return base

# --------------------------- CREATE ------------------------------------------


def test_create_forum_post_success(login_user, client):
    resp_login = login_user(email="forumcreate@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    payload = _forum_post_payload(title="Post Test", content="Contenu test")
    resp = client.post("/data/forum/posts", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body["title"] == "Post Test"


def test_create_forum_post_unauthenticated(client):
    payload = _forum_post_payload(title="Post Test", content="Contenu test")
    resp = client.post("/data/forum/posts", json=payload)
    assert resp.status_code in (401, 422)

# --------------------------- READ --------------------------------------------


def test_get_all_forum_posts(client):
    resp = client.get("/data/forum/posts")
    assert resp.status_code == 200
    body = _std(resp)
    assert isinstance(body, list)


def test_get_forum_post_by_id(login_user, client):
    resp_login = login_user(email="forumget@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    payload = _forum_post_payload(title="Lecture", content="Contenu un peu plus long pour que l'attribut comprenne que c'est un texte")
    resp_create = client.post("/data/forum/posts", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
    post_id = _std(resp_create)["id"]
    resp = client.get(f"/data/forum/posts/{post_id}")
    body = _std(resp)
    assert resp.status_code == 200
    assert body["title"] == "Lecture"

# --------------------------- UPDATE ------------------------------------------


def test_update_forum_post_success(login_user, client):
    resp_login = login_user(email="forumupdate@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    payload = _forum_post_payload(title="Avant", content="Avant le texte était comme ça pour que le tet comprenne que c'était bien un texte")
    resp_create = client.post("/data/forum/posts", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
    post_id = _std(resp_create)["id"]
    resp = client.put(f"/data/forum/posts/{post_id}", json={"title": "Après"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["title"] == "Après"


def test_update_forum_post_unauthenticated(client):
    resp = client.put("/data/forum/posts/1", json={"title": "NoJWT"})
    assert resp.status_code in (401, 422)


def test_update_forum_post_not_author(login_user, client):
    # Création par user1
    resp_login1 = login_user(email="author@trucmuche.com")
    cookie1 = _extract_access_cookie(resp_login1)
    payload = _forum_post_payload(title="Auteur", content="Contenu doit être un peu plus long pour que l'attribut comprenne que c'est un texte")
    resp_create = client.post("/data/forum/posts", json=payload, headers={"Cookie": f"access_token_cookie={cookie1}"})
    post_id = _std(resp_create)["id"]
    # Tentative update par user2
    resp_login2 = login_user(email="notauthor@trucmuche.com")
    cookie2 = _extract_access_cookie(resp_login2)
    resp = client.put(f"/data/forum/posts/{post_id}", json={"title": "Fail"}, headers={"Cookie": f"access_token_cookie={cookie2}"})
    assert resp.status_code == 400

# --------------------------- DELETE ------------------------------------------


def test_delete_forum_post_success(login_user, client):
    resp_login = login_user(email="forumdelete@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    payload = _forum_post_payload(title="supprimer", content="Contenu doit être un peu plus long pour que l'attribut comprenne que c'est un texte")
    resp_create = client.post("/data/forum/posts", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
    post_id = _std(resp_create)["id"]
    resp = client.delete(
        f"/data/forum/posts/{post_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200


def test_delete_forum_post_unauthenticated(client):
    resp = client.delete("/data/forum/posts/1")
    assert resp.status_code == 401


def test_delete_forum_post_not_author(login_user, client):
    # Création par user1
    resp_login1 = login_user(email="author2@trucmuche.com")
    cookie1 = _extract_access_cookie(resp_login1)
    payload = _forum_post_payload(title="Auteur2", content="Contenu doit être un peu plus long pour que l'attribut comprenne que c'est un texte")
    resp_create = client.post("/data/forum/posts", json=payload, headers={"Cookie": f"access_token_cookie={cookie1}"})
    post_id = _std(resp_create)["id"]
    # Tentative suppression par user2
    resp_login2 = login_user(email="notauthor2@trucmuche.com")
    cookie2 = _extract_access_cookie(resp_login2)
    resp = client.delete(
        f"/data/forum/posts/{post_id}", headers={"Cookie": f"access_token_cookie={cookie2}"})
    assert resp.status_code == 400

# --------------------------- LIKE --------------------------------------------


def test_like_forum_post_toggle(login_user, client):
    resp_login = login_user(email="forumlike@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    payload = _forum_post_payload(title="Like", content="Contenu")
    resp_create = client.post("/data/forum/posts", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
    post_id = _std(resp_create)["id"]
    resp_login2 = login_user(email="userliked@trucmuche.com")
    cookie2 = _extract_access_cookie(resp_login2)
    # Like
    resp_like = client.post(
        f"/data/forum/posts/{post_id}/like", headers={"Cookie": f"access_token_cookie={cookie2}"})
    body_like = _std(resp_like)
    assert resp_like.status_code == 200
    # Unlike
    resp_unlike = client.post(
        f"/data/forum/posts/{post_id}/like", headers={"Cookie": f"access_token_cookie={cookie}"})
    body_unlike = _std(resp_unlike)
    assert resp_unlike.status_code == 200


def test_like_forum_post_unauthenticated(client):
    resp = client.post("/data/forum/posts/1/like")
    assert resp.status_code in (401, 422)
