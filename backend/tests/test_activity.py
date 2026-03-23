"""
[BACK][tests/test_activity.py]

Test suite — activity_bp blueprint (/data/activity)

Covers:
  - Nominal flow (create, read, update, delete, stats)
  - Validation errors (missing fields, invalid values)
  - Authentication errors (missing or invalid token)
  - Edge cases (empty list, double delete, auto entry_date)

Fixtures: client, login_user (defined in conftest.py)
"""


from app import db
from app.models.activity import Activity
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


def _activity_payload(description="marche", duration=30, **overrides):
    """Return a base activity payload with optional overrides."""
    base = {"description": description, "duration": duration}
    base.update(overrides)
    return base


# ----------------------------- Create -----------------------------------------
def test_create_activity_success(login_user, client):
    """POST /data/activity/ — valid payload returns 201 and entry data."""
    resp_login = login_user(email="actuser@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    payload = _activity_payload(description="marche", duration=45)
    resp = client.post("/data/activity/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body["description"] == "marche"
    assert body["duration"] == 45


def test_create_activity_missing_body(login_user, client):
    """POST /data/activity/ — missing body returns 400."""
    resp_login = login_user(email="actmissingbody@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/activity/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_create_activity_missing_fields(login_user, client):
    """POST /data/activity/ — missing required field (duration) returns 422."""
    resp_login = login_user(email="actmissing@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    payload = {"description": "marche"}
    resp = client.post("/data/activity/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_activity_invalid_description(login_user, client):
    """POST /data/activity/ — invalid description value returns 422."""
    resp_login = login_user(email="actbaddesc@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    payload = _activity_payload(description="invalid_sport", duration=30)
    resp = client.post("/data/activity/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_activity_invalid_duration(login_user, client):
    """POST /data/activity/ — duration out of range returns 422."""
    resp_login = login_user(email="actbaddur@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    payload = _activity_payload(description="marche", duration=0)
    resp = client.post("/data/activity/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


# ----------------------------- Read -------------------------------------------
def test_read_activity_success(login_user, client):
    """GET /data/activity/ — returns list containing created entry."""
    resp_login = login_user(email="actread@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/activity/", json=_activity_payload(description="yoga", duration=60), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/activity/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert any(e.get("description") == "yoga" for e in body)


def test_read_activity_empty(login_user, client):
    """GET /data/activity/ — returns empty list when user has no entries."""
    resp_login = login_user(email="actnotfound@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/activity/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert len(body) == 0


# ----------------------------- Update -----------------------------------------
def test_update_activity_success(login_user, client):
    """PUT /data/activity/<id> — valid update returns 200 and updated data."""
    resp_login = login_user(email="actupdate@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/activity/", json=_activity_payload(description="vélo", duration=20), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.put(f"/data/activity/{entry_id}", json={"duration": 50}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["duration"] == 50


def test_update_activity_not_found(login_user, client):
    """PUT /data/activity/<id> — unknown id returns 404."""
    resp_login = login_user(email="actupdate404@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/data/activity/9999", json={"duration": 50}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 404
    assert "error" in body


def test_update_activity_invalid_value(login_user, client):
    """PUT /data/activity/<id> — invalid duration value returns 422."""
    resp_login = login_user(email="actupdateinvalid@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/activity/", json=_activity_payload(description="marche", duration=30), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.put(f"/data/activity/{entry_id}", json={"duration": 0}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_activity_unauthorized(client):
    """PUT /data/activity/<id> — missing JWT returns 401."""
    resp = client.put("/data/activity/1", json={"duration": 10})
    assert resp.status_code == 401


# ----------------------------- Delete -----------------------------------------
def test_delete_activity_success(login_user, client):
    """DELETE /data/activity/<id> — valid delete returns 204."""
    resp_login = login_user(email="actdelete@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/activity/", json=_activity_payload(description="natation", duration=30), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.delete(f"/data/activity/{entry_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 204


def test_delete_activity_not_found(login_user, client):
    """DELETE /data/activity/<id> — unknown id returns 404."""
    resp_login = login_user(email="actdelete404@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.delete("/data/activity/9999", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 404
    assert "error" in body


def test_delete_activity_twice(login_user, client):
    """DELETE /data/activity/<id> — second delete on same id returns 404."""
    resp_login = login_user(email="actdelete2@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/activity/", json=_activity_payload(description="bricolage", duration=45), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp1 = client.delete(f"/data/activity/{entry_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp1.status_code == 204
    resp2 = client.delete(f"/data/activity/{entry_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp2.status_code == 404


def test_delete_activity_unauthorized(client):
    """DELETE /data/activity/<id> — missing JWT returns 401."""
    resp = client.delete("/data/activity/1")
    assert resp.status_code == 401


# ----------------------------- Entry date -------------------------------------
def test_activity_entry_date_auto_generated(login_user, client):
    """POST /data/activity/ — entry_date is auto-generated on creation."""
    resp_login = login_user(email="actdate@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/activity/", json=_activity_payload(description="bricolage", duration=25), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert "entry_date" in body
    assert isinstance(body["entry_date"], str)


# ----------------------------- JWT --------------------------------------------
def test_jwt_missing(client):
    """GET /data/activity/ — missing JWT returns 401."""
    resp = client.get("/data/activity/")
    assert resp.status_code == 401


def test_jwt_invalid(client):
    """GET /data/activity/ — invalid JWT returns 401."""
    resp = client.get("/data/activity/", headers={"Cookie": "access_token_cookie=invalid"})
    assert resp.status_code == 401


# ----------------------------- Role access ------------------------------------
def test_role_user_access(login_user, client):
    """GET /data/activity/ — standard user can access their entries."""
    resp_login = login_user(email="roleact@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/activity/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200


# ----------------------------- Stats ------------------------------------------
def test_activity_stats(login_user, client):
    """GET /data/activity/stats — returns average field."""
    resp_login = login_user(email="actstats@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/activity/", json=_activity_payload(description="marche", duration=30), headers={"Cookie": f"access_token_cookie={cookie}"})
    client.post("/data/activity/", json=_activity_payload(description="vélo", duration=60), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/activity/stats", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert "average" in body


def test_activity_stats_value(login_user, client):
    """GET /data/activity/stats — average is correctly computed."""
    resp_login = login_user(email="actstatsfields@trucmuche.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/activity/", json=_activity_payload(description="marche", duration=30), headers={"Cookie": f"access_token_cookie={cookie}"})
    client.post("/data/activity/", json=_activity_payload(description="vélo", duration=60), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/activity/stats", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["average"] == 45
