"""
[BACK][tests/test_health_professional.py]

Test suite — professional_bp blueprint (/data/health_professionals)

Covers:
  - Nominal flow (create, read, update, delete)
  - Validation errors (missing body, missing fields, invalid values)
  - Authentication errors (missing or invalid token)
  - Edge cases (not found, empty list)

Fixtures: client, login_user (defined in conftest.py)
"""

from app import db
from app.models.health_professional import HealthProfessional


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


def _pro_payload(fullname="Dr. Test", speciality="diabetologist", **overrides):
    """Return a base health professional payload with optional overrides."""
    base = {"fullname": fullname, "speciality": speciality}
    base.update(overrides)
    return base


# ----------------------------- Create -----------------------------------------
def test_create_health_professional_success(login_user, client):
    """POST /data/health_professionals/ — valid payload returns 201."""
    resp_login = login_user(email="prouser@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/health_professionals/", json=_pro_payload(fullname="Jean Bonblanc", speciality="diabetologist"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body["fullname"] == "Jean Bonblanc"
    assert body["speciality"] == "diabetologist"


def test_create_health_professional_missing_body(login_user, client):
    """POST /data/health_professionals/ — missing body returns 400."""
    resp_login = login_user(email="promissingbody@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/health_professionals/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_create_health_professional_missing_fields(login_user, client):
    """POST /data/health_professionals/ — missing required field (speciality) returns 422."""
    resp_login = login_user(email="promissing@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/health_professionals/", json={"fullname": "Dr. Missing"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_health_professional_invalid_phone(login_user, client):
    """POST /data/health_professionals/ — invalid phone format returns 422."""
    resp_login = login_user(email="probadphone@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/health_professionals/", json=_pro_payload(phone="notaphone"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_health_professional_invalid_specialty(login_user, client):
    """POST /data/health_professionals/ — invalid speciality returns 422."""
    resp_login = login_user(email="probadsp@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/health_professionals/", json=_pro_payload(speciality="invalid"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_health_professional_missing_token(client):
    """POST /data/health_professionals/ — missing JWT returns 401."""
    resp = client.post("/data/health_professionals/", json=_pro_payload())
    assert resp.status_code == 401


# ----------------------------- Read all ---------------------------------------
def test_read_health_professionals_success(login_user, client):
    """GET /data/health_professionals/ — returns list of professionals."""
    resp_login = login_user(email="proread@example.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/health_professionals/", json=_pro_payload(fullname="Dr. Read"), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/health_professionals/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert any(e.get("fullname") == "Dr. Read" for e in body)


def test_read_health_professionals_empty(login_user, client):
    """GET /data/health_professionals/ — returns empty list when no entries."""
    resp_login = login_user(email="pronotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/health_professionals/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert len(body) == 0


def test_read_health_professionals_missing_token(client):
    """GET /data/health_professionals/ — missing JWT returns 401."""
    fresh_client = client.application.test_client()
    resp = fresh_client.get("/data/health_professionals/")
    assert resp.status_code == 401


def test_read_health_professionals_invalid_token(client):
    """GET /data/health_professionals/ — invalid JWT returns 401."""
    resp = client.get("/data/health_professionals/", headers={"Cookie": "access_token_cookie=invalid"})
    assert resp.status_code == 401


# ----------------------------- Read by id -------------------------------------
def test_read_health_professional_with_details_success(login_user, client):
    """GET /data/health_professionals/<id> — returns professional with notes and documents."""
    resp_login = login_user(email="prodetails@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/health_professionals/", json=_pro_payload(fullname="Dr. Details"), headers={"Cookie": f"access_token_cookie={cookie}"})
    pro_id = _std(resp_create)["id"]
    resp = client.get(f"/data/health_professionals/{pro_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["fullname"] == "Dr. Details"
    assert "notes" in body
    assert "documents" in body


def test_read_health_professional_with_details_not_found(login_user, client):
    """GET /data/health_professionals/<id> — unknown id returns 404."""
    resp_login = login_user(email="prodetailsnotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/health_professionals/id-inexistant", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


# ----------------------------- Update -----------------------------------------
def test_update_health_professional_success(login_user, client):
    """PUT /data/health_professionals/<id> — valid update returns 200."""
    resp_login = login_user(email="proupdate@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/health_professionals/", json=_pro_payload(fullname="Dr. Update"), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.put(f"/data/health_professionals/{entry_id}", json={"speciality": "endocrinologist"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["speciality"] == "endocrinologist"


def test_update_health_professional_not_found(login_user, client):
    """PUT /data/health_professionals/<id> — unknown id returns 404."""
    resp_login = login_user(email="proupdatenotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/data/health_professionals/id-inexistant", json={"speciality": "endocrinologist"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_update_health_professional_missing_token(client):
    """PUT /data/health_professionals/<id> — missing JWT returns 401."""
    resp = client.put("/data/health_professionals/1", json={"speciality": "endocrinologist"})
    assert resp.status_code == 401


# ----------------------------- Delete -----------------------------------------
def test_delete_health_professional_success(login_user, client):
    """DELETE /data/health_professionals/<id> — valid delete returns 204."""
    resp_login = login_user(email="prodelete@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/health_professionals/", json=_pro_payload(fullname="Dr. Delete", speciality="psychologist"), headers={"Cookie": f"access_token_cookie={cookie}"})
    entry_id = _std(resp_create)["id"]
    resp = client.delete(f"/data/health_professionals/{entry_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 204


def test_delete_health_professional_not_found(login_user, client):
    """DELETE /data/health_professionals/<id> — unknown id returns 404."""
    resp_login = login_user(email="prodeletenotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.delete("/data/health_professionals/id-inexistant", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_delete_health_professional_missing_token(client):
    """DELETE /data/health_professionals/<id> — missing JWT returns 401."""
    resp = client.delete("/data/health_professionals/1")
    assert resp.status_code == 401


# ----------------------------- Role access ------------------------------------
def test_role_user_access(login_user, client):
    """GET /data/health_professionals/ — standard user can access their entries."""
    resp_login = login_user(email="rolepro@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/health_professionals/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200
