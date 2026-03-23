"""
[BACK][tests/test_mood.py]

Test suite — mood_bp blueprint (/data/mood)

Covers:
  - Nominal flow (create, read, update, delete)
  - Validation errors (missing body, empty body, invalid description)
  - Authentication errors (missing or invalid token)
  - Edge cases (empty list, entry not found)

Fixtures: client, login_user (defined in conftest.py)
"""

from app import db
from app.models.mood import Mood


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


def _mood_payload(description="Joyeux", **overrides):
    """Return a base mood payload with optional overrides."""
    base = {"description": description}
    base.update(overrides)
    return base


# ----------------------------- Create -----------------------------------------
def test_create_mood_success(login_user, client):
    """POST /data/mood/ — valid payload returns 201."""
    resp_login = login_user(email="mooduser@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/mood/", json=_mood_payload(description="Joyeux"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body["description"] == "Joyeux"


def test_create_mood_missing_body(login_user, client):
    """POST /data/mood/ — missing body returns 400."""
    resp_login = login_user(email="moodmissingbody@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/mood/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_create_mood_missing_description(login_user, client):
    """POST /data/mood/ — empty body returns 400."""
    resp_login = login_user(email="mooduser2@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/mood/", json={}, headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_create_mood_invalid_description(login_user, client):
    """POST /data/mood/ — invalid description value returns 422."""
    resp_login = login_user(email="mooduser3@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/mood/", json=_mood_payload(description="Inconnu"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_mood_missing_token(client):
    """POST /data/mood/ — missing JWT returns 401."""
    resp = client.post("/data/mood/", json=_mood_payload())
    assert resp.status_code == 401


# ----------------------------- Read -------------------------------------------
def test_read_mood_list_success(login_user, client):
    """GET /data/mood/ — returns list of mood entries."""
    resp_login = login_user(email="mooduser4@example.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/mood/", json=_mood_payload(description="Joyeux"), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/mood/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert any(m.get("description") == "Joyeux" for m in body)


def test_read_mood_empty(login_user, client):
    """GET /data/mood/ — returns empty list when no entries."""
    resp_login = login_user(email="mooduser5@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/mood/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert len(body) == 0


def test_read_mood_missing_token(client):
    """GET /data/mood/ — missing JWT returns 401."""
    fresh_client = client.application.test_client()
    resp = fresh_client.get("/data/mood/")
    assert resp.status_code == 401


def test_read_mood_invalid_token(client):
    """GET /data/mood/ — invalid JWT returns 401."""
    resp = client.get("/data/mood/", headers={"Cookie": "access_token_cookie=invalid"})
    assert resp.status_code == 401


# ----------------------------- Update -----------------------------------------
def test_update_mood_success(login_user, client):
    """PUT /data/mood/<id> — valid update returns 200."""
    resp_login = login_user(email="mooduser6@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/mood/", json=_mood_payload(description="Joyeux"), headers={"Cookie": f"access_token_cookie={cookie}"})
    mood_id = _std(resp_create)["id"]
    resp = client.put(f"/data/mood/{mood_id}", json=_mood_payload(description="Motivé"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["description"] == "Motivé"


def test_update_mood_not_found(login_user, client):
    """PUT /data/mood/<id> — unknown id returns 404."""
    resp_login = login_user(email="moodupdatenotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/data/mood/id-inexistant", json=_mood_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_update_mood_missing_body(login_user, client):
    """PUT /data/mood/<id> — missing body returns 400."""
    resp_login = login_user(email="moodupdatebody@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/mood/", json=_mood_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    mood_id = _std(resp_create)["id"]
    resp = client.put(f"/data/mood/{mood_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_update_mood_invalid_description(login_user, client):
    """PUT /data/mood/<id> — invalid description returns 422."""
    resp_login = login_user(email="moodupdateinvalid@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/mood/", json=_mood_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    mood_id = _std(resp_create)["id"]
    resp = client.put(f"/data/mood/{mood_id}", json=_mood_payload(description="Inconnu"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_mood_missing_token(client):
    """PUT /data/mood/<id> — missing JWT returns 401."""
    resp = client.put("/data/mood/1", json=_mood_payload())
    assert resp.status_code == 401


# ----------------------------- Delete -----------------------------------------
def test_delete_mood_success(login_user, client):
    """DELETE /data/mood/<id> — valid delete returns 204."""
    resp_login = login_user(email="mooduser9@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/mood/", json=_mood_payload(description="Motivé"), headers={"Cookie": f"access_token_cookie={cookie}"})
    mood_id = _std(resp_create)["id"]
    resp = client.delete(f"/data/mood/{mood_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 204


def test_delete_mood_not_found(login_user, client):
    """DELETE /data/mood/<id> — unknown id returns 404."""
    resp_login = login_user(email="mooduser10@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.delete("/data/mood/00000000-0000-0000-0000-000000000000", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_delete_mood_missing_token(client):
    """DELETE /data/mood/<id> — missing JWT returns 401."""
    resp = client.delete("/data/mood/1")
    assert resp.status_code == 401


# ----------------------------- Role access ------------------------------------
def test_mood_role_user_access(login_user, client):
    """GET /data/mood/ — standard user can access their mood entries."""
    resp_login = login_user(email="mooduser11@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/mood/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200
