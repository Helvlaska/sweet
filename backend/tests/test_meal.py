from datetime import datetime, timezone


def _std(resp):
	return resp.get_json() if resp.is_json else {}


def _extract_access_cookie(resp):
	cookies = resp.headers.getlist("Set-Cookie")
	for c in cookies:
		if c.startswith("access_token_cookie="):
			return c.split(";", 1)[0].split("=", 1)[1]
	return None


def _meal_payload(meal_type="lunch", description="Repas de test", **overrides):
	# Le modèle Meal attend meal_type (enum) et description (string)
	base = {"meal_type": meal_type, "description": description}
	base.update(overrides)
	return base


# --------------------------- CREATE -------------------------------------------
def test_create_meal_success(login_user, client):
	resp_login = login_user(email="mealcreate@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _meal_payload(meal_type="breakfast", description="Oeufs brouillés")
	resp = client.post("/data/meal", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 201
	assert body.get("meal_type") == "breakfast"
	assert "Oeufs" in (body.get("description") or "")


def test_create_meal_missing_description(login_user, client):
	resp_login = login_user(email="mealmiss@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = {"meal_type": "dinner"}  # description manquante
	resp = client.post("/data/meal", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body


def test_create_meal_invalid_meal_type(login_user, client):
	resp_login = login_user(email="mealbadtype@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _meal_payload(meal_type="brunch")  # valeur non autorisée
	resp = client.post("/data/meal", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body


def test_create_meal_invalid_description(login_user, client):
	resp_login = login_user(email="mealbaddesc@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _meal_payload(description="ab")  # trop court
	resp = client.post("/data/meal", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body


def test_create_meal_description_too_long(login_user, client):
	resp_login = login_user(email="meallongdesc@example.com")
	cookie = _extract_access_cookie(resp_login)
	long_desc = "a" * 301
	payload = _meal_payload(description=long_desc)
	resp = client.post("/data/meal", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body


# --------------------------- READ (LIST) --------------------------------------
def test_get_meal_list_success(login_user, client):
	resp_login = login_user(email="mealread@example.com")
	cookie = _extract_access_cookie(resp_login)
	client.post("/data/meal", json=_meal_payload(meal_type="lunch", description="Salade"), headers={"Cookie": f"access_token_cookie={cookie}"})
	client.post("/data/meal", json=_meal_payload(meal_type="dinner", description="Soupe"), headers={"Cookie": f"access_token_cookie={cookie}"})
	resp = client.get("/data/meal", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert isinstance(body, list)
	descs = [m.get("description") for m in body]
	assert any("Salade" in (d or "") for d in descs)
	assert any("Soupe" in (d or "") for d in descs)


def test_get_meal_list_with_range_day(login_user, client):
	resp_login = login_user(email="mealrangeday@example.com")
	cookie = _extract_access_cookie(resp_login)
	client.post("/data/meal", json=_meal_payload(meal_type="snack", description="Barre protéinée"), headers={"Cookie": f"access_token_cookie={cookie}"})
	resp = client.get("/data/meal?range_type=day", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code == 200


def test_get_meal_list_with_target_date(login_user, client):
	resp_login = login_user(email="mealrangetarget@example.com")
	cookie = _extract_access_cookie(resp_login)
	date = datetime.now(timezone.utc).date().isoformat()
	client.post("/data/meal", json=_meal_payload(meal_type="lunch", description="Date Filtree"), headers={"Cookie": f"access_token_cookie={cookie}"})
	resp = client.get(f"/data/meal?range_type=day&target_date={date}", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code == 200


# --------------------------- UPDATE ------------------------------------------
def test_update_meal_success(login_user, client):
	resp_login = login_user(email="mealupdate@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/meal", json=_meal_payload(meal_type="dinner", description="Pâtes"), headers={"Cookie": f"access_token_cookie={cookie}"})
	meal_id = _std(create_resp).get("id")
	resp = client.put(f"/data/meal/{meal_id}", json={"meal_type": "dinner", "description": "Pâtes complètes"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert "Pâtes complètes" in (body.get("description") or "")


def test_update_meal_invalid_meal_type(login_user, client):
	resp_login = login_user(email="mealbadfield@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/meal", json=_meal_payload(meal_type="snack", description="Barre"), headers={"Cookie": f"access_token_cookie={cookie}"})
	meal_id = _std(create_resp).get("id")
	resp = client.put(f"/data/meal/{meal_id}", json={"meal_type": "random", "description": "Barre"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body


def test_update_meal_invalid_description(login_user, client):
	resp_login = login_user(email="mealbaddescupd@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/meal", json=_meal_payload(meal_type="lunch", description="Salade verte"), headers={"Cookie": f"access_token_cookie={cookie}"})
	meal_id = _std(create_resp).get("id")
	resp = client.put(f"/data/meal/{meal_id}", json={"description": "ok"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body


def test_update_meal_unauthorized(client):
	resp = client.put("/data/meal/abc", json={"description": "X"})
	assert resp.status_code in (401, 422)


# --------------------------- DELETE ------------------------------------------
def test_delete_meal_success(login_user, client):
	resp_login = login_user(email="mealdel@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/meal", json=_meal_payload(meal_type="lunch", description="Salade"), headers={"Cookie": f"access_token_cookie={cookie}"})
	meal_id = _std(create_resp).get("id")
	resp = client.delete(f"/data/meal/{meal_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert "deleted" in str(body).lower() or "success" in str(body).lower()


def test_delete_meal_not_existing(login_user, client):
	resp_login = login_user(email="mealnotexist@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.delete("/data/meal/ffffffff-ffff-ffff-ffff-ffffffffffff", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code in (200, 400, 404)


def test_delete_meal_unauthorized(client):
	resp = client.delete("/data/meal/abc")
	assert resp.status_code in (401, 422)


# --------------------------- JWT ---------------------------------------------
def test_meal_jwt_missing(client):
	resp = client.get("/data/meal")
	assert resp.status_code in (401, 422)


def test_meal_jwt_invalid(client):
	resp = client.get("/data/meal", headers={"Cookie": "access_token_cookie=invalid"})
	assert resp.status_code in (401, 422)


# --------------------------- RÔLES -------------------------------------------
def test_meal_access_with_admin(create_admin_instance, client):
	admin = create_admin_instance(email="adminmeal@example.com", username="adminmeal")
	from flask_jwt_extended import create_access_token
	token = create_access_token(identity=admin.id)
	resp = client.get("/data/meal", headers={"Cookie": f"access_token_cookie={token}"})
	assert resp.status_code == 200


def test_meal_access_with_user(login_user, client):
	resp_login = login_user(email="mealroleuser@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/data/meal", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code == 200

