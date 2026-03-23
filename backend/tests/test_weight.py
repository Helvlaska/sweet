"""
[BACK][tests/test_weight.py]

Test suite — weight_bp blueprint (/data/weight)

Covers:
  - Nominal flow (create, read, update, delete, stats)
  - Validation errors (missing body, invalid type, out of range)
  - Authentication errors (missing or invalid token)
  - Edge cases (empty list, entry not found, stats calculation)

Fixtures: client, login_user (defined in conftest.py)
"""

from app import db
from app.models.weight import Weight


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


def _weight_payload(mass=70.0, **overrides):
    """Return a base weight payload with optional overrides."""
    base = {"mass": mass}
    base.update(overrides)
    return base


# ----------------------------- Create -----------------------------------------
def test_create_weight_success(login_user, client):
    """POST /data/weight/ — valid payload returns 201."""
    resp_login = login_user(email="weightuser@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/weight/", json=_weight_payload(mass=72.5), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body["mass"] == 72.5


def test_create_weight_missing_body(login_user, client):
    """POST /data/weight/ — missing body returns 400."""
    resp_login = login_user(email="weightmissingbody@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/weight/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_create_weight_invalid_type(login_user, client):
    """POST /data/weight/ — non-numeric mass returns 422."""
    resp_login = login_user(email="weightmissing@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/weight/", json={"mass": "soixante"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_weight_invalid_value(login_user, client):
    """POST /data/weight/ — mass out of range returns 422."""
    resp_login = login_user(email="weightbadval@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/weight/", json=_weight_payload(mass=-10), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_weight_missing_token(client):
    """POST /data/weight/ — missing JWT returns 401."""
    resp = client.post("/data/weight/", json=_weight_payload())
    assert resp.status_code == 401


# ----------------------------- Read -------------------------------------------
def test_read_weight_success(login_user, client):
    """GET /data/weight/ — returns list containing created entry."""
    resp_login = login_user(email="weightread@example.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/weight/", json=_weight_payload(mass=68.0), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/weight/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert any(e.get("mass") == 68.0 for e in body)


def test_read_weight_empty(login_user, client):
    """GET /data/weight/ — returns empty list when no entries."""
    resp_login = login_user(email="weightnotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/weight/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert len(body) == 0


def test_read_weight_missing_token(client):
    """GET /data/weight/ — missing JWT returns 401."""
    fresh_client = client.application.test_client()
    resp = fresh_client.get("/data/weight/")
    assert resp.status_code == 401


def test_read_weight_invalid_token(client):
    """GET /data/weight/ — invalid JWT returns 401."""
    resp = client.get("/data/weight/", headers={"Cookie": "access_token_cookie=invalid"})
    assert resp.status_code == 401


# ----------------------------- Update -----------------------------------------
def test_update_weight_success(login_user, client):
    """PUT /data/weight/<id> — valid update returns 200."""
    resp_login = login_user(email="weightupdate@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/weight/", json=_weight_payload(mass=75.0), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.put(f"/data/weight/{entry_id}", json={"mass": 80.0}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["mass"] == 80.0


def test_update_weight_not_found(login_user, client):
    """PUT /data/weight/<id> — unknown id returns 404."""
    resp_login = login_user(email="weightupdatenotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/data/weight/id-inexistant", json={"mass": 70.0}, headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_update_weight_missing_body(login_user, client):
    """PUT /data/weight/<id> — missing body returns 400."""
    resp_login = login_user(email="weightupdatebody@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/weight/", json=_weight_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.put(f"/data/weight/{entry_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_update_weight_invalid_value(login_user, client):
    """PUT /data/weight/<id> — mass out of range returns 422."""
    resp_login = login_user(email="weightupdateinvalid@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/weight/", json=_weight_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.put(f"/data/weight/{entry_id}", json={"mass": 999.0}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_weight_missing_token(client):
    """PUT /data/weight/<id> — missing JWT returns 401."""
    resp = client.put("/data/weight/1", json={"mass": 65.0})
    assert resp.status_code == 401


# ----------------------------- Delete -----------------------------------------
def test_delete_weight_success(login_user, client):
    """DELETE /data/weight/<id> — valid delete returns 204."""
    resp_login = login_user(email="weightdelete@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/weight/", json=_weight_payload(mass=60.0), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.delete(f"/data/weight/{entry_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 204


def test_delete_weight_not_found(login_user, client):
    """DELETE /data/weight/<id> — unknown id returns 404."""
    resp_login = login_user(email="weightdeletenotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.delete("/data/weight/id-inexistant", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_delete_weight_missing_token(client):
    """DELETE /data/weight/<id> — missing JWT returns 401."""
    resp = client.delete("/data/weight/1")
    assert resp.status_code == 401


# ----------------------------- Role access ------------------------------------
def test_role_user_access(login_user, client):
    """GET /data/weight/ — standard user can access their entries."""
    resp_login = login_user(email="roleweight@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/weight/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200


# ----------------------------- Stats ------------------------------------------
def test_weight_stats(login_user, client):
    """GET /data/weight/stats — returns average field."""
    resp_login = login_user(email="weightstats@example.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/weight/", json=_weight_payload(mass=70.0), headers={"Cookie": f"access_token_cookie={cookie}"})
    client.post("/data/weight/", json=_weight_payload(mass=80.0), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/weight/stats", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert "average" in body


def test_weight_stats_value(login_user, client):
    """GET /data/weight/stats — average is correctly computed."""
    resp_login = login_user(email="weightstatsvalue@example.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/weight/", json=_weight_payload(mass=70.0), headers={"Cookie": f"access_token_cookie={cookie}"})
    client.post("/data/weight/", json=_weight_payload(mass=80.0), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/weight/stats", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["average"] == 75.0
