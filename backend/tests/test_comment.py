"""
[BACK][tests/test_comment.py]

Test suite — comment_bp blueprint (/forum/posts/<post_id>/comments)

Covers:
  - Nominal flow (create, read, update, delete, like toggle)
  - Validation errors (missing fields, invalid content)
  - Authentication errors (missing token)
  - Authorization errors (not author, own comment like)
  - Edge cases (post not found, comment not found)

Fixtures: client, login_user (defined in conftest.py)
"""

from app import db
from app.models.comment import Comment
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


def _comment_payload(content="Un commentaire valide", **overrides):
    """Return a base comment payload with optional overrides."""
    base = {"content": content}
    base.update(overrides)
    return base


def _create_post_and_cookie(client, login_user, email):
    """Helper — register, login and create a forum post. Returns (post_id, cookie)."""
    resp_login = login_user(email=email)
    cookie = _extract_access_cookie(resp_login)
    resp = client.post(
        "/forum/posts/",
        json={"title": "Post de test", "content": "Contenu du post de test"},
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    post_id = _std(resp)["id"]
    return post_id, cookie


# ----------------------------- Create -----------------------------------------
def test_create_comment_success(login_user, client):
    """POST /forum/posts/<id>/comments/ — valid payload returns 201."""
    post_id, cookie = _create_post_and_cookie(client, login_user, email="commentcreate@trucmuche.com")
    resp = client.post(f"/forum/posts/{post_id}/comments/", json=_comment_payload(content="Commentaire Test"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body["content"] == "Commentaire Test"


def test_create_comment_missing_body(login_user, client):
    """POST /forum/posts/<id>/comments/ — missing body returns 400."""
    post_id, cookie = _create_post_and_cookie(client, login_user, email="commentbody@trucmuche.com")
    resp = client.post(f"/forum/posts/{post_id}/comments/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_create_comment_post_not_found(login_user, client):
    """POST /forum/posts/<id>/comments/ — unknown post id returns 404."""
    resp_login = login_user(email="commentpostnotfound@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/forum/posts/id-inexistant/comments/", json=_comment_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_create_comment_missing_token(client):
    """POST /forum/posts/<id>/comments/ — missing JWT returns 401."""
    resp = client.post("/forum/posts/some-id/comments/", json=_comment_payload())
    assert resp.status_code == 401


# ----------------------------- Read -------------------------------------------
def test_get_comments_success(login_user, client):
    """GET /forum/posts/<id>/comments/ — returns list of comments."""
    post_id, cookie = _create_post_and_cookie(client, login_user, email="commentget@trucmuche.com")
    client.post(f"/forum/posts/{post_id}/comments/", json=_comment_payload(content="Lecture commentaire"), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get(f"/forum/posts/{post_id}/comments/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert any(c["content"] == "Lecture commentaire" for c in body)


def test_get_comments_post_not_found(login_user, client):
    """GET /forum/posts/<id>/comments/ — unknown post id returns 404."""
    resp_login = login_user(email="commentgetnotfound@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/forum/posts/id-inexistant/comments/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_get_comments_missing_token(client):
    """GET /forum/posts/<id>/comments/ — missing JWT returns 401."""
    resp = client.get("/forum/posts/some-id/comments/")
    assert resp.status_code == 401


# ----------------------------- Update -----------------------------------------
def test_update_comment_success(login_user, client):
    """PUT /forum/posts/<id>/comments/<id> — author can update their comment."""
    post_id, cookie = _create_post_and_cookie(client, login_user, email="commentupdate@trucmuche.com")
    resp_create = client.post(f"/forum/posts/{post_id}/comments/", json=_comment_payload(content="Avant"), headers={"Cookie": f"access_token_cookie={cookie}"})
    comment_id = _std(resp_create)["id"]
    resp = client.put(f"/forum/posts/{post_id}/comments/{comment_id}", json=_comment_payload(content="Après"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["content"] == "Après"


def test_update_comment_not_author(login_user, client):
    """PUT /forum/posts/<id>/comments/<id> — non-author returns 403."""
    post_id, cookie1 = _create_post_and_cookie(client, login_user, email="authorcomment@trucmuche.com")
    resp_create = client.post(f"/forum/posts/{post_id}/comments/", json=_comment_payload(content="Auteur"), headers={"Cookie": f"access_token_cookie={cookie1}"})
    comment_id = _std(resp_create)["id"]
    resp_login2 = login_user(email="notauthorcomment@trucmuche.com")
    cookie2 = _extract_access_cookie(resp_login2)
    resp = client.put(f"/forum/posts/{post_id}/comments/{comment_id}", json=_comment_payload(content="Fail"), headers={"Cookie": f"access_token_cookie={cookie2}"})
    body = _std(resp)
    assert resp.status_code == 403
    assert "error" in body


def test_update_comment_invalid_content(login_user, client):
    """PUT /forum/posts/<id>/comments/<id> — invalid content returns 422."""
    post_id, cookie = _create_post_and_cookie(client, login_user, email="commentupdateinvalid@trucmuche.com")
    resp_create = client.post(f"/forum/posts/{post_id}/comments/", json=_comment_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    comment_id = _std(resp_create)["id"]
    resp = client.put(f"/forum/posts/{post_id}/comments/{comment_id}", json=_comment_payload(content=""), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_comment_missing_token(client):
    """PUT /forum/posts/<id>/comments/<id> — missing JWT returns 401."""
    resp = client.put("/forum/posts/some-id/comments/some-comment", json=_comment_payload())
    assert resp.status_code == 401


# ----------------------------- Delete -----------------------------------------
def test_delete_comment_success(login_user, client):
    """DELETE /forum/posts/<id>/comments/<id> — author can delete their comment, returns 204."""
    post_id, cookie = _create_post_and_cookie(client, login_user, email="commentdelete@trucmuche.com")
    resp_create = client.post(f"/forum/posts/{post_id}/comments/", json=_comment_payload(content="A supprimer"), headers={"Cookie": f"access_token_cookie={cookie}"})
    comment_id = _std(resp_create)["id"]
    resp = client.delete(f"/forum/posts/{post_id}/comments/{comment_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 204


def test_delete_comment_not_author(login_user, client):
    """DELETE /forum/posts/<id>/comments/<id> — non-author returns 403."""
    post_id, cookie1 = _create_post_and_cookie(client, login_user, email="authorcomment2@trucmuche.com")
    resp_create = client.post(f"/forum/posts/{post_id}/comments/", json=_comment_payload(content="Auteur2"), headers={"Cookie": f"access_token_cookie={cookie1}"})
    comment_id = _std(resp_create)["id"]
    resp_login2 = login_user(email="notauthorcomment2@trucmuche.com")
    cookie2 = _extract_access_cookie(resp_login2)
    resp = client.delete(f"/forum/posts/{post_id}/comments/{comment_id}", headers={"Cookie": f"access_token_cookie={cookie2}"})
    body = _std(resp)
    assert resp.status_code == 403
    assert "error" in body


def test_delete_comment_missing_token(client):
    """DELETE /forum/posts/<id>/comments/<id> — missing JWT returns 401."""
    resp = client.delete("/forum/posts/some-id/comments/some-comment")
    assert resp.status_code == 401


# ----------------------------- Like -------------------------------------------
def test_toggle_like_comment_success(login_user, client):
    """POST /forum/posts/<id>/comments/<id>/like — user can like then unlike a comment."""
    post_id, cookie1 = _create_post_and_cookie(client, login_user, email="commentlikeauthor@trucmuche.com")
    resp_create = client.post(f"/forum/posts/{post_id}/comments/", json=_comment_payload(content="A liker"), headers={"Cookie": f"access_token_cookie={cookie1}"})
    comment_id = _std(resp_create)["id"]
    resp_login2 = login_user(email="commentlikeuser@trucmuche.com")
    cookie2 = _extract_access_cookie(resp_login2)
    resp_like = client.post(f"/forum/posts/{post_id}/comments/{comment_id}/like", headers={"Cookie": f"access_token_cookie={cookie2}"})
    assert resp_like.status_code == 200
    resp_unlike = client.post(f"/forum/posts/{post_id}/comments/{comment_id}/like", headers={"Cookie": f"access_token_cookie={cookie2}"})
    assert resp_unlike.status_code == 200


def test_toggle_like_own_comment_forbidden(login_user, client):
    """POST /forum/posts/<id>/comments/<id>/like — cannot like own comment, returns 403."""
    post_id, cookie = _create_post_and_cookie(client, login_user, email="commentlikeown@trucmuche.com")
    resp_create = client.post(f"/forum/posts/{post_id}/comments/", json=_comment_payload(content="Mon commentaire"), headers={"Cookie": f"access_token_cookie={cookie}"})
    comment_id = _std(resp_create)["id"]
    resp = client.post(f"/forum/posts/{post_id}/comments/{comment_id}/like", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 403
    assert "error" in body


def test_toggle_like_comment_missing_token(client):
    """POST /forum/posts/<id>/comments/<id>/like — missing JWT returns 401."""
    resp = client.post("/forum/posts/some-id/comments/some-comment/like")
    assert resp.status_code == 401
