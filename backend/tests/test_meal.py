"""
[BACK][tests/test_meal.py]

Test suite — meal_bp blueprint (/data/meal)

Covers:
  - Nominal flow (create, read, update, delete)
  - Validation errors (missing body, invalid type, invalid description)
  - Authentication errors (missing or invalid token)
  - Edge cases (empty list, entry not found, date range filter)

Fixtures: client, login_user (defined in conftest.py)
"""

from datetime import datetime, timezone
from app import db
from app.models.meal import Meal


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


def _meal_payload(meal_type="lunch", description="Repas de test", **overrides):
    """Return a base meal payload with optional overrides."""
    base = {"meal_type": meal_type, "description": description}
    base.update(overrides)
    return base


# ----------------------------- Create -----------------------------------------
def test_create_meal_success(login_user, client):
    """POST /data/meal/ — valid payload returns 201."""
    resp_login = login_user(email="mealcreate@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/meal/", json=_meal_payload(meal_type="breakfast", description="Oeufs brouillés"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body.get("meal_type") == "breakfast"
    assert "Oeufs" in (body.get("description") or "")


def test_create_meal_missing_body(login_user, client):
    """POST /data/meal/ — missing body returns 400."""
    resp_login = login_user(email="mealmissingbody@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/meal/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_create_meal_missing_description(login_user, client):
    """POST /data/meal/ — missing description returns 422."""
    resp_login = login_user(email="mealmiss@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/meal/", json={"meal_type": "dinner"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_meal_invalid_meal_type(login_user, client):
    """POST /data/meal/ — invalid meal_type returns 422."""
    resp_login = login_user(email="mealbadtype@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/meal/", json=_meal_payload(meal_type="brunch"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_meal_invalid_description(login_user, client):
    """POST /data/meal/ — description too short returns 422."""
    resp_login = login_user(email="mealbaddesc@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/meal/", json=_meal_payload(description="ab"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_meal_description_too_long(login_user, client):
    """POST /data/meal/ — description too long returns 422."""
    resp_login = login_user(email="meallongdesc@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/data/meal/", json=_meal_payload(description="a" * 301), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_meal_missing_token(client):
    """POST /data/meal/ — missing JWT returns 401."""
    resp = client.post("/data/meal/", json=_meal_payload())
    assert resp.status_code == 401


# ----------------------------- Read -------------------------------------------
def test_get_meal_list_success(login_user, client):
    """GET /data/meal/ — returns list of meal entries."""
    resp_login = login_user(email="mealread@example.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/meal/", json=_meal_payload(meal_type="lunch", description="Salade"), headers={"Cookie": f"access_token_cookie={cookie}"})
    client.post("/data/meal/", json=_meal_payload(meal_type="dinner", description="Soupe"), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/meal/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    descs = [m.get("description") for m in body]
    assert any("Salade" in (d or "") for d in descs)
    assert any("Soupe" in (d or "") for d in descs)


def test_get_meal_list_with_range_day(login_user, client):
    """GET /data/meal/?range_type=day — returns entries for today."""
    resp_login = login_user(email="mealrangeday@example.com")
    cookie = _extract_access_cookie(resp_login)
    client.post("/data/meal/", json=_meal_payload(meal_type="snack", description="Barre protéinée"), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get("/data/meal/?range_type=day", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200


def test_get_meal_list_with_target_date(login_user, client):
    """GET /data/meal/?range_type=day&target_date=<today> — returns filtered entries."""
    resp_login = login_user(email="mealrangetarget@example.com")
    cookie = _extract_access_cookie(resp_login)
    date = datetime.now(timezone.utc).date().isoformat()
    client.post("/data/meal/", json=_meal_payload(meal_type="lunch", description="Date Filtree"), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get(f"/data/meal/?range_type=day&target_date={date}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200


def test_get_meal_missing_token(client):
    """GET /data/meal/ — missing JWT returns 401."""
    fresh_client = client.application.test_client()
    resp = fresh_client.get("/data/meal/")
    assert resp.status_code == 401


def test_get_meal_invalid_token(client):
    """GET /data/meal/ — invalid JWT returns 401."""
    resp = client.get("/data/meal/", headers={"Cookie": "access_token_cookie=invalid"})
    assert resp.status_code == 401


# ----------------------------- Update -----------------------------------------
def test_update_meal_success(login_user, client):
    """PUT /data/meal/<id> — valid update returns 200."""
    resp_login = login_user(email="mealupdate@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/meal/", json=_meal_payload(meal_type="dinner", description="Pâtes"), headers={"Cookie": f"access_token_cookie={cookie}"})
    meal_id = _std(resp_create).get("id")
    resp = client.put(f"/data/meal/{meal_id}", json=_meal_payload(meal_type="dinner", description="Pâtes complètes"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert "Pâtes complètes" in (body.get("description") or "")


def test_update_meal_not_found(login_user, client):
    """PUT /data/meal/<id> — unknown id returns 404."""
    resp_login = login_user(email="mealupdatenotfound@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/data/meal/id-inexistant", json=_meal_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_update_meal_missing_body(login_user, client):
    """PUT /data/meal/<id> — missing body returns 400."""
    resp_login = login_user(email="mealupdatebody@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/meal/", json=_meal_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    meal_id = _std(resp_create).get("id")
    resp = client.put(f"/data/meal/{meal_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_update_meal_invalid_meal_type(login_user, client):
    """PUT /data/meal/<id> — invalid meal_type returns 422."""
    resp_login = login_user(email="mealbadfield@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/meal/", json=_meal_payload(meal_type="snack", description="Barre"), headers={"Cookie": f"access_token_cookie={cookie}"})
    meal_id = _std(resp_create).get("id")
    resp = client.put(f"/data/meal/{meal_id}", json=_meal_payload(meal_type="random", description="Barre"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_meal_invalid_description(login_user, client):
    """PUT /data/meal/<id> — invalid description returns 422."""
    resp_login = login_user(email="mealbaddescupd@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/meal/", json=_meal_payload(meal_type="lunch", description="Salade verte"), headers={"Cookie": f"access_token_cookie={cookie}"})
    meal_id = _std(resp_create).get("id")
    resp = client.put(f"/data/meal/{meal_id}", json=_meal_payload(description="ok"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_meal_missing_token(client):
    """PUT /data/meal/<id> — missing JWT returns 401."""
    resp = client.put("/data/meal/abc", json=_meal_payload())
    assert resp.status_code == 401


# ----------------------------- Delete -----------------------------------------
def test_delete_meal_success(login_user, client):
    """DELETE /data/meal/<id> — valid delete returns 204."""
    resp_login = login_user(email="mealdel@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp_create = client.post("/data/meal/", json=_meal_payload(meal_type="lunch", description="Salade"), headers={"Cookie": f"access_token_cookie={cookie}"})
    meal_id = _std(resp_create).get("id")
    resp = client.delete(f"/data/meal/{meal_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 204


def test_delete_meal_not_found(login_user, client):
    """DELETE /data/meal/<id> — unknown id returns 404."""
    resp_login = login_user(email="mealnotexist@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.delete("/data/meal/ffffffff-ffff-ffff-ffff-ffffffffffff", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_delete_meal_missing_token(client):
    """DELETE /data/meal/<id> — missing JWT returns 401."""
    resp = client.delete("/data/meal/abc")
    assert resp.status_code == 401


# ----------------------------- Role access ------------------------------------
def test_meal_access_with_user(login_user, client):
    """GET /data/meal/ — standard user can access their entries."""
    resp_login = login_user(email="mealroleuser@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/data/meal/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200
