"""
[BACK][tests/test_medication.py]

Test suite — medication_bp blueprint (/data/medication)

Covers:
  - Nominal flow (create, read, update, delete, take dose)
  - Validation errors (missing body, invalid fields, insufficient stock)
  - Authentication errors (missing or invalid token)
  - Edge cases (not found, low stock alert, large stock)

Fixtures: client, login_user (defined in conftest.py)
"""

from app import db
from app.models.medication import Medication


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


def _med_payload(name="Doliprane", dose=500, stock=5000, frequency="once_a_day", **overrides):
    """Return a base medication payload with optional overrides."""
    base = {"name": name, "dose": dose, "stock": stock, "frequency": frequency}
    base.update(overrides)
    return base


# ----------------------------- Create -----------------------------------------
def test_create_medication_success(login_user, client):
    """POST /data/medication/ — valid payload returns 201."""
    resp_login = login_user(email="meduser@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/medication/", json=_med_payload(name="Ibuprofène", dose=200, stock=3000, frequency="twice_a_day"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body["name"].startswith("Ibuprof")
    assert body["dose"] == 200


def test_create_medication_missing_body(login_user, client):
    """POST /data/medication/ — missing body returns 400."""
    resp_login = login_user(email="medmissingbody@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/medication/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_create_medication_missing_field(login_user, client):
    """POST /data/medication/ — missing required fields returns 422."""
    resp_login = login_user(email="meduser2@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/medication/", json={"name": "TestMed"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_medication_invalid_name(login_user, client):
    """POST /data/medication/ — name too short returns 422."""
    resp_login = login_user(email="meduser3@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/medication/", json=_med_payload(name="A"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_medication_invalid_dose(login_user, client):
    """POST /data/medication/ — dose <= 0 returns 422."""
    resp_login = login_user(email="meduser4@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/medication/", json=_med_payload(dose=0), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_medication_invalid_frequency(login_user, client):
    """POST /data/medication/ — invalid frequency returns 422."""
    resp_login = login_user(email="meduser5@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/medication/", json=_med_payload(frequency="every_hour"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_medication_missing_token(client):
    """POST /data/medication/ — missing JWT returns 401."""
    resp = client.post("/data/medication/", json=_med_payload())
    assert resp.status_code == 401


def test_create_medication_large_stock(login_user, client):
    """POST /data/medication/ — very large stock is accepted (no upper bound in model)."""
    resp_login = login_user(email="meduser16@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/medication/", json=_med_payload(stock=10**7), headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 201


# ----------------------------- Read -------------------------------------------
def test_read_medication_list_success(login_user, client):
    """GET /data/medication/ — returns list of medications."""
    resp_login = login_user(email="meduser6@example.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/medication/", json=_med_payload(name="Paracetamol"), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/medication/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert any(m.get("name", "").startswith("Parace") for m in body)


def test_read_medication_empty(login_user, client):
    """GET /data/medication/ — returns empty list when no entries."""
    resp_login = login_user(email="meduser7@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/medication/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert len(body) == 0


def test_read_medication_missing_token(client):
    """GET /data/medication/ — missing JWT returns 401."""
    fresh_client = client.application.test_client()
    resp = fresh_client.get("/data/medication/")
    assert resp.status_code == 401


def test_read_medication_invalid_token(client):
    """GET /data/medication/ — invalid JWT returns 401."""
    resp = client.get("/data/medication/", headers={"Cookie": "access_token_cookie=invalid"})
    assert resp.status_code == 401


# ----------------------------- Update -----------------------------------------
def test_update_medication_success(login_user, client):
    """PUT /data/medication/<id> — valid update returns 200."""
    resp_login = login_user(email="meduser8@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/medication/", json=_med_payload(name="Azithro", dose=250, stock=2000, frequency="once_a_day"), headers={"Cookie": f"access_token_cookie={cookie}"})
    med_id = _std(resp_create)["id"]
    resp = client.put(f"/data/medication/{med_id}", json=_med_payload(name="Azithro", dose=500, stock=4000, frequency="twice_a_day"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["dose"] == 500


def test_update_medication_not_found(login_user, client):
    """PUT /data/medication/<id> — unknown id returns 404."""
    resp_login = login_user(email="medupdatenotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/data/medication/id-inexistant", json=_med_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_update_medication_missing_body(login_user, client):
    """PUT /data/medication/<id> — missing body returns 400."""
    resp_login = login_user(email="medupdatebody@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/medication/", json=_med_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    med_id = _std(resp_create)["id"]
    resp = client.put(f"/data/medication/{med_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_update_medication_invalid_data(login_user, client):
    """PUT /data/medication/<id> — invalid fields return 422."""
    resp_login = login_user(email="meduser10@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/medication/", json=_med_payload(name="VitC", dose=100, stock=1000), headers={"Cookie": f"access_token_cookie={cookie}"})
    med_id = _std(resp_create)["id"]
    resp = client.put(f"/data/medication/{med_id}", json=_med_payload(name="B", dose=-5, stock=-10), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_medication_invalid_frequency(login_user, client):
    """PUT /data/medication/<id> — invalid frequency returns 422."""
    resp_login = login_user(email="meduser17@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/medication/", json=_med_payload(name="PostEdit", frequency="once_a_day"), headers={"Cookie": f"access_token_cookie={cookie}"})
    med_id = _std(resp_create)["id"]
    resp = client.put(f"/data/medication/{med_id}", json=_med_payload(name="PostEdit", frequency="invalid_freq"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_medication_missing_token(client):
    """PUT /data/medication/<id> — missing JWT returns 401."""
    resp = client.put("/data/medication/1", json=_med_payload())
    assert resp.status_code == 401


# ----------------------------- Delete -----------------------------------------
def test_delete_medication_success(login_user, client):
    """DELETE /data/medication/<id> — valid delete returns 204."""
    resp_login = login_user(email="meduser11@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/medication/", json=_med_payload(name="ToDel", dose=50, stock=500), headers={"Cookie": f"access_token_cookie={cookie}"})
    med_id = _std(resp_create)["id"]
    resp = client.delete(f"/data/medication/{med_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 204


def test_delete_medication_not_found(login_user, client):
    """DELETE /data/medication/<id> — unknown id returns 404."""
    resp_login = login_user(email="meduser12@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.delete("/data/medication/00000000-0000-0000-0000-000000000000", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_delete_medication_missing_token(client):
    """DELETE /data/medication/<id> — missing JWT returns 401."""
    resp = client.delete("/data/medication/1")
    assert resp.status_code == 401


# ----------------------------- Take dose --------------------------------------
def test_take_medication_dose_success(login_user, client):
    """PATCH /data/medication/<id>/take — valid intake returns 200 with updated stock."""
    resp_login = login_user(email="meduser13@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/medication/", json=_med_payload(name="Levothyrox", dose=25, stock=100, frequency="once_a_day"), headers={"Cookie": f"access_token_cookie={cookie}"})
    med_id = _std(resp_create)["id"]
    resp = client.patch(f"/data/medication/{med_id}/take", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["stock"] == 75


def test_take_medication_dose_not_found(login_user, client):
    """PATCH /data/medication/<id>/take — unknown id returns 404."""
    resp_login = login_user(email="meduser14@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.patch("/data/medication/00000000-0000-0000-0000-000000000000/take", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_take_medication_dose_insufficient_stock(login_user, client):
    """PATCH /data/medication/<id>/take — insufficient stock returns 422."""
    resp_login = login_user(email="meduser18@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/medication/", json=_med_payload(name="LowStock", dose=500, stock=300, frequency="once_a_day"), headers={"Cookie": f"access_token_cookie={cookie}"})
    med_id = _std(resp_create)["id"]
    resp = client.patch(f"/data/medication/{med_id}/take", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_take_medication_dose_multiple(login_user, client):
    """PATCH /data/medication/<id>/take — multiple doses decrease stock correctly."""
    resp_login = login_user(email="meduser19@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/medication/", json=_med_payload(name="Multi", dose=100, stock=600, frequency="once_a_day"), headers={"Cookie": f"access_token_cookie={cookie}"})
    med_id = _std(resp_create)["id"]
    resp1 = client.patch(f"/data/medication/{med_id}/take", headers={"Cookie": f"access_token_cookie={cookie}"})
    resp2 = client.patch(f"/data/medication/{med_id}/take", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp1.status_code == 200
    assert resp2.status_code == 200
    assert _std(resp2)["stock"] == 400


# ----------------------------- Role access ------------------------------------
def test_medication_role_user_access(login_user, client):
    """GET /data/medication/ — standard user can access their medications."""
    resp_login = login_user(email="meduser15@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/medication/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200
