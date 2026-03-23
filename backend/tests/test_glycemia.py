"""
[BACK][tests/test_glycemia.py]

Test suite — glycemia_bp blueprint (/data/glycemia)

Covers:
  - Nominal flow (create, read, update, delete, stats)
  - Validation errors (missing body, missing fields, out of range)
  - Authentication errors (missing or invalid token)
  - Edge cases (empty list, entry not found, stats calculation)

Fixtures: client, login_user (defined in conftest.py)
"""

from app import db
from app.models.glycemia import Glycemia


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


def _glycemia_payload(glucose_level=120, **overrides):
    """Return a base glycemia payload with optional overrides."""
    base = {"glucose_level": glucose_level}
    base.update(overrides)
    return base


# ----------------------------- Create -----------------------------------------
def test_create_glycemia_success(login_user, client):
    """POST /data/glycemia/ — valid payload returns 201."""
    resp_login = login_user(email="glyuser@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/glycemia/", json=_glycemia_payload(glucose_level=120), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body["glucose_level"] == 120


def test_create_glycemia_missing_body(login_user, client):
    """POST /data/glycemia/ — missing body returns 400."""
    resp_login = login_user(email="glymissingbody@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/glycemia/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_create_glycemia_missing_fields(login_user, client):
    """POST /data/glycemia/ — missing glucose_level returns 422."""
    resp_login = login_user(email="glymissing@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/glycemia/", json={"other_field": "value"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_glycemia_invalid_value(login_user, client):
    """POST /data/glycemia/ — glucose_level out of range returns 422."""
    resp_login = login_user(email="glybadval@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/glycemia/", json=_glycemia_payload(glucose_level=20), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_glycemia_missing_token(client):
    """POST /data/glycemia/ — missing JWT returns 401."""
    resp = client.post("/data/glycemia/", json=_glycemia_payload())
    assert resp.status_code == 401


# ----------------------------- Read -------------------------------------------
def test_read_glycemia_success(login_user, client):
    """GET /data/glycemia/ — returns list containing created entry."""
    resp_login = login_user(email="glyread@example.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/glycemia/", json=_glycemia_payload(glucose_level=90), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/glycemia/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert any(e.get("glucose_level") == 90 for e in body)


def test_read_glycemia_empty(login_user, client):
    """GET /data/glycemia/ — returns empty list when no entries exist."""
    resp_login = login_user(email="glynotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/glycemia/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert len(body) == 0


def test_read_glycemia_missing_token(client):
    """GET /data/glycemia/ — missing JWT returns 401."""
    fresh_client = client.application.test_client()
    resp = fresh_client.get("/data/glycemia/")
    assert resp.status_code == 401


def test_read_glycemia_invalid_token(client):
    """GET /data/glycemia/ — invalid JWT returns 401."""
    resp = client.get("/data/glycemia/", headers={"Cookie": "access_token_cookie=invalid"})
    assert resp.status_code == 401


# ----------------------------- Update -----------------------------------------
def test_update_glycemia_success(login_user, client):
    """PUT /data/glycemia/<id> — valid update returns 200."""
    resp_login = login_user(email="glyupdate@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/glycemia/", json=_glycemia_payload(glucose_level=100), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.put(f"/data/glycemia/{entry_id}", json={"glucose_level": 90}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["glucose_level"] == 90


def test_update_glycemia_not_found(login_user, client):
    """PUT /data/glycemia/<id> — unknown id returns 404."""
    resp_login = login_user(email="glyupdatenotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/data/glycemia/id-inexistant", json={"glucose_level": 100}, headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_update_glycemia_missing_body(login_user, client):
    """PUT /data/glycemia/<id> — missing body returns 400."""
    resp_login = login_user(email="glyupdatebody@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/glycemia/", json=_glycemia_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.put(f"/data/glycemia/{entry_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_update_glycemia_invalid_value(login_user, client):
    """PUT /data/glycemia/<id> — out of range value returns 422."""
    resp_login = login_user(email="glyupdateinvalid@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/glycemia/", json=_glycemia_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.put(f"/data/glycemia/{entry_id}", json={"glucose_level": 20}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_glycemia_missing_token(client):
    """PUT /data/glycemia/<id> — missing JWT returns 401."""
    resp = client.put("/data/glycemia/1", json={"glucose_level": 100})
    assert resp.status_code == 401


# ----------------------------- Delete -----------------------------------------
def test_delete_glycemia_success(login_user, client):
    """DELETE /data/glycemia/<id> — valid delete returns 204."""
    resp_login = login_user(email="glydelete@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/glycemia/", json=_glycemia_payload(glucose_level=110), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.delete(f"/data/glycemia/{entry_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 204


def test_delete_glycemia_not_found(login_user, client):
    """DELETE /data/glycemia/<id> — unknown id returns 404."""
    resp_login = login_user(email="glydeletenotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.delete("/data/glycemia/id-inexistant", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_delete_glycemia_missing_token(client):
    """DELETE /data/glycemia/<id> — missing JWT returns 401."""
    resp = client.delete("/data/glycemia/1")
    assert resp.status_code == 401


# ----------------------------- Role access ------------------------------------
def test_role_user_access(login_user, client):
    """GET /data/glycemia/ — standard user can access their entries."""
    resp_login = login_user(email="rolegly@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/glycemia/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200


# ----------------------------- Stats ------------------------------------------
def test_glycemia_stats(login_user, client):
    """GET /data/glycemia/stats — returns average field."""
    resp_login = login_user(email="glystats@example.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/glycemia/", json=_glycemia_payload(glucose_level=110), headers={"Cookie": f"access_token_cookie={cookie}"})
    client.post("/data/glycemia/", json=_glycemia_payload(glucose_level=120), headers={"Cookie": f"access_token_cookie={cookie}"})
    client.post("/data/glycemia/", json=_glycemia_payload(glucose_level=99), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/glycemia/stats", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert "average" in body


def test_glycemia_stats_value(login_user, client):
    """GET /data/glycemia/stats — average is correctly computed."""
    resp_login = login_user(email="glystatsvalue@example.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/glycemia/", json=_glycemia_payload(glucose_level=100), headers={"Cookie": f"access_token_cookie={cookie}"})
    client.post("/data/glycemia/", json=_glycemia_payload(glucose_level=200), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/glycemia/stats", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["average"] == 150
