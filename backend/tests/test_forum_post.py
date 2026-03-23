"""
[BACK][tests/test_forum_post.py]

Test suite — forum_bp blueprint (/forum/posts)

Covers:
  - Nominal flow (create, read, update, delete, like toggle)
  - Validation errors (missing body, invalid data)
  - Authentication errors (missing token)
  - Authorization errors (not author, own post like)
  - Edge cases (post not found, double like)

Fixtures: client, login_user (defined in conftest.py)
"""

from app import db
from app.models.forum_post import ForumPost
from app.models.user import User


# ----------------------------- Helpers ----------------------------------------
def _std(resp):
    """Extract JSON body from a Flask response, or return an empty dict."""
    return resp.get_json() if resp.is_json else {}


def _extract_access_cookie(resp):
    """Extract access_token_cookie value from a Flask response."""
    cookies = resp.headers.getlist("Set-Cookie")
    for c in cookies:
        if c.startswith("access_token_cookie="):
            return c.split(";", 1)[0].split("=", 1)[1]
    return None


def _forum_post_payload(title="Un post valide", content="Contenu du post suffisamment long pour passer la validation", **overrides):
    """Return a base forum post payload with optional overrides."""
    base = {"title": title, "content": content}
    base.update(overrides)
    return base


# ----------------------------- Create -----------------------------------------
def test_create_forum_post_success(login_user, client):
    """POST /forum/posts/ — valid payload returns 201."""
    resp_login = login_user(email="forumcreate@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/forum/posts/", json=_forum_post_payload(title="Post Test"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body["title"] == "Post Test"


def test_create_forum_post_missing_body(login_user, client):
    """POST /forum/posts/ — missing body returns 400."""
    resp_login = login_user(email="forummissingbody@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/forum/posts/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_create_forum_post_invalid_data(login_user, client):
    """POST /forum/posts/ — missing required fields returns 422."""
    resp_login = login_user(email="foruminvalid@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/forum/posts/", json={"title": "Sans contenu"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_forum_post_missing_token(client):
    """POST /forum/posts/ — missing JWT returns 401."""
    resp = client.post("/forum/posts/", json=_forum_post_payload())
    assert resp.status_code == 401


# ----------------------------- Read all ---------------------------------------
def test_get_all_forum_posts_success(login_user, client):
    """GET /forum/posts/ — returns list of posts."""
    resp_login = login_user(email="forumreadall@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/forum/posts/", json=_forum_post_payload(title="Post liste"), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/forum/posts/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)


def test_get_all_forum_posts_missing_token(client):
    """GET /forum/posts/ — missing JWT returns 401."""
    fresh_client = client.application.test_client()
    resp = fresh_client.get("/forum/posts/")
    assert resp.status_code == 401


# ----------------------------- Read by id -------------------------------------
def test_get_forum_post_by_id_success(login_user, client):
    """GET /forum/posts/<id> — returns post with comments."""
    resp_login = login_user(email="forumget@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/forum/posts/", json=_forum_post_payload(title="Lecture"), headers={"Cookie": f"access_token_cookie={cookie}"})
    post_id = _std(resp_create)["id"]
    resp = client.get(f"/forum/posts/{post_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["title"] == "Lecture"
    assert "comments" in body


def test_get_forum_post_by_id_not_found(login_user, client):
    """GET /forum/posts/<id> — unknown id returns 404."""
    resp_login = login_user(email="forumgetnotfound@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/forum/posts/id-inexistant", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_get_forum_post_by_id_missing_token(client):
    """GET /forum/posts/<id> — missing JWT returns 401."""
    fresh_client = client.application.test_client()
    resp = fresh_client.get("/forum/posts/some-id")
    assert resp.status_code == 401


# ----------------------------- Update -----------------------------------------
def test_update_forum_post_success(login_user, client):
    """PUT /forum/posts/<id> — author can update their post."""
    resp_login = login_user(email="forumupdate@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/forum/posts/", json=_forum_post_payload(title="Avant"), headers={"Cookie": f"access_token_cookie={cookie}"})
    post_id = _std(resp_create)["id"]
    resp = client.put(f"/forum/posts/{post_id}", json={"title": "Après"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["title"] == "Après"


def test_update_forum_post_not_found(login_user, client):
    """PUT /forum/posts/<id> — unknown id returns 404."""
    resp_login = login_user(email="forumupdatenotfound@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/forum/posts/id-inexistant", json={"title": "Fail"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_update_forum_post_not_author(login_user, client):
    """PUT /forum/posts/<id> — non-author returns 403."""
    resp_login1 = login_user(email="author@trucmuche.com")
    cookie1 = _extract_access_cookie(resp_login1)
    resp_create = client.post("/forum/posts/", json=_forum_post_payload(title="Auteur"), headers={"Cookie": f"access_token_cookie={cookie1}"})
    post_id = _std(resp_create)["id"]
    resp_login2 = login_user(email="notauthor@trucmuche.com")
    cookie2 = _extract_access_cookie(resp_login2)
    resp = client.put(f"/forum/posts/{post_id}", json={"title": "Fail"}, headers={"Cookie": f"access_token_cookie={cookie2}"})
    body = _std(resp)
    assert resp.status_code == 403
    assert "error" in body


def test_update_forum_post_missing_token(client):
    """PUT /forum/posts/<id> — missing JWT returns 401."""
    resp = client.put("/forum/posts/some-id", json={"title": "NoJWT"})
    assert resp.status_code == 401


# ----------------------------- Delete -----------------------------------------
def test_delete_forum_post_success(login_user, client):
    """DELETE /forum/posts/<id> — author can delete their post, returns 204."""
    resp_login = login_user(email="forumdelete@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/forum/posts/", json=_forum_post_payload(title="A supprimer"), headers={"Cookie": f"access_token_cookie={cookie}"})
    post_id = _std(resp_create)["id"]
    resp = client.delete(f"/forum/posts/{post_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 204


def test_delete_forum_post_not_found(login_user, client):
    """DELETE /forum/posts/<id> — unknown id returns 404."""
    resp_login = login_user(email="forumdeletenotfound@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.delete("/forum/posts/id-inexistant", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_delete_forum_post_not_author(login_user, client):
    """DELETE /forum/posts/<id> — non-author returns 403."""
    resp_login1 = login_user(email="author2@trucmuche.com")
    cookie1 = _extract_access_cookie(resp_login1)
    resp_create = client.post("/forum/posts/", json=_forum_post_payload(title="Auteur2"), headers={"Cookie": f"access_token_cookie={cookie1}"})
    post_id = _std(resp_create)["id"]
    resp_login2 = login_user(email="notauthor2@trucmuche.com")
    cookie2 = _extract_access_cookie(resp_login2)
    resp = client.delete(f"/forum/posts/{post_id}", headers={"Cookie": f"access_token_cookie={cookie2}"})
    body = _std(resp)
    assert resp.status_code == 403
    assert "error" in body


def test_delete_forum_post_missing_token(client):
    """DELETE /forum/posts/<id> — missing JWT returns 401."""
    resp = client.delete("/forum/posts/some-id")
    assert resp.status_code == 401


# ----------------------------- Like -------------------------------------------
def test_like_forum_post_toggle(login_user, client):
    """POST /forum/posts/<id>/like — user can like then unlike a post."""
    resp_login1 = login_user(email="forumlike@trucmuche.com")
    cookie1 = _extract_access_cookie(resp_login1)
    resp_create = client.post("/forum/posts/", json=_forum_post_payload(title="Post à liker"), headers={"Cookie": f"access_token_cookie={cookie1}"})
    post_id = _std(resp_create)["id"]
    resp_login2 = login_user(email="userliked@trucmuche.com")
    cookie2 = _extract_access_cookie(resp_login2)
    resp_like = client.post(f"/forum/posts/{post_id}/like", headers={"Cookie": f"access_token_cookie={cookie2}"})
    assert resp_like.status_code == 200
    resp_unlike = client.post(f"/forum/posts/{post_id}/like", headers={"Cookie": f"access_token_cookie={cookie2}"})
    assert resp_unlike.status_code == 200


def test_like_own_post_forbidden(login_user, client):
    """POST /forum/posts/<id>/like — cannot like own post, returns 403."""
    resp_login = login_user(email="forumlikeown@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/forum/posts/", json=_forum_post_payload(title="Mon post"), headers={"Cookie": f"access_token_cookie={cookie}"})
    post_id = _std(resp_create)["id"]
    resp = client.post(f"/forum/posts/{post_id}/like", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 403
    assert "error" in body


def test_like_forum_post_not_found(login_user, client):
    """POST /forum/posts/<id>/like — unknown post id returns 404."""
    resp_login = login_user(email="forumlikenotfound@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/forum/posts/id-inexistant/like", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_like_forum_post_missing_token(client):
    """POST /forum/posts/<id>/like — missing JWT returns 401."""
    resp = client.post("/forum/posts/some-id/like")
    assert resp.status_code == 401
