"""
[BACK][tests/test_article.py]

Test suite — article_bp blueprint (/article)

Covers:
  - Nominal flow (create, read, update, delete, like toggle)
  - Validation errors (missing fields, invalid values)
  - Authentication errors (missing token)
  - Authorization errors (non-admin write, own article like)
  - Edge cases (not found, double like)

Fixtures: client, login_user, create_admin_via_api (defined in conftest.py)
"""

from app import db
from app.models.article import Article
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


def _article_payload(title="Un article valide", content="Contenu valide suffisamment long pour passer la validation", **overrides):
    """Return a base article payload with optional overrides."""
    base = {"title": title, "content": content}
    base.update(overrides)
    return base


# ----------------------------- Create -----------------------------------------
def test_create_article_success(client, create_admin_via_api):
    """POST /article/ — admin can create an article, returns 201."""
    admin, cookie = create_admin_via_api(email="adminart@example.com", username="adminart")
    resp = client.post("/article/", json=_article_payload(title="Article Test"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body["title"] == "Article Test"
    assert body["id"] is not None


def test_create_article_missing_body(client, create_admin_via_api):
    """POST /article/ — missing body returns 400."""
    admin, cookie = create_admin_via_api(email="adminartbody@example.com", username="adminartbody")
    resp = client.post("/article/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_create_article_missing_fields(client, create_admin_via_api):
    """POST /article/ — missing required field (content) returns 422."""
    admin, cookie = create_admin_via_api(email="adminmissing@example.com", username="adminmissing")
    resp = client.post("/article/", json={"title": "Sans contenu"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_article_invalid_title(client, create_admin_via_api):
    """POST /article/ — invalid title returns 422."""
    admin, cookie = create_admin_via_api(email="admininvalid@example.com", username="admininvalid")
    resp = client.post("/article/", json=_article_payload(title=""), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_article_forbidden_user(client, login_user):
    """POST /article/ — non-admin user returns 403."""
    resp_login = login_user(email="userart@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/article/", json=_article_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 403
    assert "error" in body


def test_create_article_missing_token(client):
    """POST /article/ — missing JWT returns 401."""
    resp = client.post("/article/", json=_article_payload())
    assert resp.status_code == 401


# ----------------------------- Read all ---------------------------------------
def test_read_all_articles_success(client, create_admin_via_api):
    """GET /article/ — returns list of articles."""
    admin, cookie = create_admin_via_api(email="adminreadall@example.com", username="adminreadall")
    client.post("/article/", json=_article_payload(title="Article liste"), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/article/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)


def test_read_all_articles_missing_token(client):
    """GET /article/ — missing JWT returns 401."""
    resp = client.get("/article/")
    assert resp.status_code == 401


# ----------------------------- Read by id -------------------------------------
def test_read_article_success(client, create_admin_via_api):
    """GET /article/<id> — returns article data."""
    admin, cookie = create_admin_via_api(email="adminread@example.com", username="adminread")
    resp_create = client.post("/article/", json=_article_payload(title="Article lecture"), headers={"Cookie": f"access_token_cookie={cookie}"})
    article_id = _std(resp_create)["id"]
    resp = client.get(f"/article/{article_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["title"] == "Article lecture"


def test_read_article_not_found(client, create_admin_via_api):
    """GET /article/<id> — unknown id returns 404."""
    admin, cookie = create_admin_via_api(email="adminreadnotfound@example.com", username="adminreadnotfound")
    resp = client.get("/article/id-inexistant", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_read_article_missing_token(client):
    """GET /article/<id> — missing JWT returns 401."""
    resp = client.get("/article/some-id")
    assert resp.status_code == 401


# ----------------------------- Update -----------------------------------------
def test_update_article_success(client, create_admin_via_api):
    """PUT /article/<id> — admin can update an article, returns 200."""
    admin, cookie = create_admin_via_api(email="adminupdate@example.com", username="adminupdate")
    resp_create = client.post("/article/", json=_article_payload(title="Avant update"), headers={"Cookie": f"access_token_cookie={cookie}"})
    article_id = _std(resp_create)["id"]
    resp = client.put(f"/article/{article_id}", json=_article_payload(title="Après update"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["title"] == "Après update"


def test_update_article_not_found(client, create_admin_via_api):
    """PUT /article/<id> — unknown id returns 404."""
    admin, cookie = create_admin_via_api(email="adminupdatenotfound@example.com", username="adminupdatenotfound")
    resp = client.put("/article/id-inexistant", json=_article_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_update_article_invalid_field(client, create_admin_via_api):
    """PUT /article/<id> — missing required fields returns 422."""
    admin, cookie = create_admin_via_api(email="adminupdatebad@example.com", username="adminupdatebad")
    resp_create = client.post("/article/", json=_article_payload(title="BadField"), headers={"Cookie": f"access_token_cookie={cookie}"})
    article_id = _std(resp_create)["id"]
    resp = client.put(f"/article/{article_id}", json={"not_a_field": "value"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_article_forbidden_user(client, create_admin_via_api, login_user):
    """PUT /article/<id> — non-admin user returns 403."""
    admin, admin_cookie = create_admin_via_api(email="adminupdateforbidden@example.com", username="adminupdateforbidden")
    resp_create = client.post("/article/", json=_article_payload(title="Forbidden update"), headers={"Cookie": f"access_token_cookie={admin_cookie}"})
    article_id = _std(resp_create)["id"]
    resp_login = login_user(email="userupdateforbidden@example.com")
    user_cookie = _extract_access_cookie(resp_login)
    resp = client.put(f"/article/{article_id}", json=_article_payload(), headers={"Cookie": f"access_token_cookie={user_cookie}"})
    body = _std(resp)
    assert resp.status_code == 403
    assert "error" in body


def test_update_article_missing_token(client):
    """PUT /article/<id> — missing JWT returns 401."""
    resp = client.put("/article/some-id", json=_article_payload())
    assert resp.status_code == 401


# ----------------------------- Delete -----------------------------------------
def test_delete_article_success(client, create_admin_via_api):
    """DELETE /article/<id> — admin can delete an article, returns 204."""
    admin, cookie = create_admin_via_api(email="admindelete@example.com", username="admindelete")
    resp_create = client.post("/article/", json=_article_payload(title="A supprimer"), headers={"Cookie": f"access_token_cookie={cookie}"})
    article_id = _std(resp_create)["id"]
    resp = client.delete(f"/article/{article_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 204


def test_delete_article_not_found(client, create_admin_via_api):
    """DELETE /article/<id> — unknown id returns 404."""
    admin, cookie = create_admin_via_api(email="admindeletenotfound@example.com", username="admindeletenotfound")
    resp = client.delete("/article/id-inexistant", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_delete_article_forbidden_user(client, create_admin_via_api, login_user):
    """DELETE /article/<id> — non-admin user returns 403."""
    admin, admin_cookie = create_admin_via_api(email="admindeleteforbidden@example.com", username="admindeleteforbidden")
    resp_create = client.post("/article/", json=_article_payload(title="Forbidden delete"), headers={"Cookie": f"access_token_cookie={admin_cookie}"})
    article_id = _std(resp_create)["id"]
    resp_login = login_user(email="userdeleteforbidden@example.com")
    user_cookie = _extract_access_cookie(resp_login)
    resp = client.delete(f"/article/{article_id}", headers={"Cookie": f"access_token_cookie={user_cookie}"})
    body = _std(resp)
    assert resp.status_code == 403
    assert "error" in body


def test_delete_article_missing_token(client):
    """DELETE /article/<id> — missing JWT returns 401."""
    resp = client.delete("/article/some-id")
    assert resp.status_code == 401


# ----------------------------- Like -------------------------------------------
def test_like_article_toggle(client, create_admin_via_api, login_user):
    """POST /article/<id>/like — user can like then unlike an article."""
    admin, admin_cookie = create_admin_via_api(email="adminlike@example.com", username="adminlike")
    resp_create = client.post("/article/", json=_article_payload(title="Article à liker"), headers={"Cookie": f"access_token_cookie={admin_cookie}"})
    article_id = _std(resp_create)["id"]
    resp_login = login_user(email="userlike@example.com")
    user_cookie = _extract_access_cookie(resp_login)
    resp_like = client.post(f"/article/{article_id}/like", headers={"Cookie": f"access_token_cookie={user_cookie}"})
    assert resp_like.status_code == 200
    resp_unlike = client.post(f"/article/{article_id}/like", headers={"Cookie": f"access_token_cookie={user_cookie}"})
    assert resp_unlike.status_code == 200


def test_like_own_article_forbidden(client, create_admin_via_api):
    """POST /article/<id>/like — admin cannot like their own article, returns 403."""
    admin, cookie = create_admin_via_api(email="adminlikeown@example.com", username="adminlikeown")
    resp_create = client.post("/article/", json=_article_payload(title="Mon article"), headers={"Cookie": f"access_token_cookie={cookie}"})
    article_id = _std(resp_create)["id"]
    resp = client.post(f"/article/{article_id}/like", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 403
    assert "error" in body


def test_like_article_not_found(client, login_user):
    """POST /article/<id>/like — unknown article id returns 404."""
    resp_login = login_user(email="userlikenotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/article/id-inexistant/like", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_like_article_missing_token(client):
    """POST /article/<id>/like — missing JWT returns 401."""
    resp = client.post("/article/some-id/like")
    assert resp.status_code == 401
