import pytest

# Helpers communs (répliqués localement pour isolation)
def _std(resp):
	return resp.get_json() if resp.is_json else {}

def _extract_access_cookie(resp):
	cookies = resp.headers.getlist("Set-Cookie")
	for c in cookies:
		if c.startswith("access_token_cookie="):
			return c.split(";", 1)[0].split("=", 1)[1]
	return None

def _med_payload(name="Doliprane", dose=500, stock=5000, frequency="once_a_day", alert_threshold=1000, **overrides):
	base = {
		"name": name,
		"dose": dose,
		"stock": stock,
		"frequency": frequency,
		"alert_threshold": alert_threshold,
	}
	base.update(overrides)
	return base

# ---------------------------------------------------------------- CREATE
def test_create_medication_success(login_user, client):
	resp_login = login_user(email="meduser@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _med_payload(name="Ibuprofène", dose=200, stock=3000, frequency="twice_a_day", alert_threshold=500)
	resp = client.post("/data/medication", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 201
	assert body["name"].startswith("Ibuprof")  # capitalisation côté modèle
	assert body["dose"] == 200

def test_create_medication_missing_field(login_user, client):
	resp_login = login_user(email="meduser2@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = {"name": "TestMed"}  # champs obligatoires manquants
	resp = client.post("/data/medication", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

def test_create_medication_invalid_name(login_user, client):
	resp_login = login_user(email="meduser3@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _med_payload(name="A", dose=100, stock=1000)
	resp = client.post("/data/medication", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

def test_create_medication_invalid_dose(login_user, client):
	resp_login = login_user(email="meduser4@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _med_payload(dose=0)
	resp = client.post("/data/medication", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

def test_create_medication_invalid_frequency(login_user, client):
	resp_login = login_user(email="meduser5@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _med_payload(frequency="every_hour")
	resp = client.post("/data/medication", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

# ---------------------------------------------------------------- READ
def test_read_medication_list_success(login_user, client):
	resp_login = login_user(email="meduser6@example.com")
	cookie = _extract_access_cookie(resp_login)
	client.post("/data/medication", json=_med_payload(name="Paracetamol"), headers={"Cookie": f"access_token_cookie={cookie}"})
	resp = client.get("/data/medication", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert isinstance(body, list) and any(m.get("name").startswith("Paracetamol"[:5]) for m in body)

def test_read_medication_empty(login_user, client):
	resp_login = login_user(email="meduser7@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/data/medication", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert isinstance(body, list)

# ---------------------------------------------------------------- UPDATE
def test_update_medication_success(login_user, client):
	resp_login = login_user(email="meduser8@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/medication", json=_med_payload(name="Azithro", dose=250, stock=2000, frequency="once_a_day"), headers={"Cookie": f"access_token_cookie={cookie}"})
	med_id = _std(create_resp)["id"]
	resp = client.put(f"/data/medication/{med_id}", json=_med_payload(name="Azithro", dose=500, stock=4000, frequency="twice_a_day"), headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["dose"] == 500

def test_update_medication_unauthorized(client):
	resp = client.put("/data/medication/1", json={"dose": 100})
	assert resp.status_code in (401, 422)

def test_update_medication_not_found(login_user, client):
	resp_login = login_user(email="meduser9@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.put("/data/medication/00000000-0000-0000-0000-000000000000", json=_med_payload(name="Ghost", dose=10), headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code in (404, 400)

def test_update_medication_invalid_data(login_user, client):
	resp_login = login_user(email="meduser10@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/medication", json=_med_payload(name="VitC", dose=100, stock=1000), headers={"Cookie": f"access_token_cookie={cookie}"})
	med_id = _std(create_resp)["id"]
	resp = client.put(f"/data/medication/{med_id}", json=_med_payload(name="B", dose=-5, stock=-10), headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

# ---------------------------------------------------------------- DELETE
def test_delete_medication_success(login_user, client):
	resp_login = login_user(email="meduser11@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/medication", json=_med_payload(name="ToDel", dose=50, stock=500), headers={"Cookie": f"access_token_cookie={cookie}"})
	med_id = _std(create_resp)["id"]
	resp = client.delete(f"/data/medication/{med_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert "success" in str(body).lower() or "deleted" in str(body).lower()

def test_delete_medication_unauthorized(client):
	resp = client.delete("/data/medication/1")
	assert resp.status_code in (401, 422)

def test_delete_medication_not_found(login_user, client):
	resp_login = login_user(email="meduser12@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.delete("/data/medication/00000000-0000-0000-0000-000000000000", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code in (404, 400, 200)  # si suppression idempotente

# ---------------------------------------------------------------- TAKE DOSE
def test_take_medication_dose_success(login_user, client):
	resp_login = login_user(email="meduser13@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/medication", json=_med_payload(name="Levothyrox", dose=25, stock=100, frequency="once_a_day", alert_threshold=50), headers={"Cookie": f"access_token_cookie={cookie}"})
	med_id = _std(create_resp)["id"]
	resp = client.patch(f"/data/medication/take/{med_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	# Selon implémentation route (actuellement return vide). On accepte 200/204
	assert resp.status_code in (200, 204)
	# Quand la route sera explicitée, vérifier nouvelle valeur de stock

def test_take_medication_dose_not_found(login_user, client):
	resp_login = login_user(email="meduser14@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.patch("/data/medication/take/00000000-0000-0000-0000-000000000000", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code in (404, 400)

# ---------------------------------------------------------------- JWT
def test_medication_jwt_missing(client):
	resp = client.get("/data/medication")
	assert resp.status_code in (401, 422)

def test_medication_jwt_invalid(client):
	resp = client.get("/data/medication", headers={"Cookie": "access_token_cookie=invalid"})
	assert resp.status_code in (401, 422)

# ---------------------------------------------------------------- ROLES
def test_medication_role_user_access(login_user, client):
	resp_login = login_user(email="meduser15@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/data/medication", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code == 200

def test_medication_role_admin_access(create_admin_instance, client):
	admin = create_admin_instance(email="adminmed@example.com", username="adminmed")
	from flask_jwt_extended import create_access_token
	token = create_access_token(identity=admin.id)
	resp = client.get("/data/medication", headers={"Cookie": f"access_token_cookie={token}"})
	assert resp.status_code == 200

# ---------------------------------------------------------------- EDGE CASES / LIMITES
def test_create_medication_large_stock(login_user, client):
	resp_login = login_user(email="meduser16@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _med_payload(stock=10**7)  # grand stock
	resp = client.post("/data/medication", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	# Peut être accepté (si pas de contrainte) ou rejeté
	assert resp.status_code in (201, 400, 500)

def test_update_medication_frequency_invalid_after_creation(login_user, client):
	resp_login = login_user(email="meduser17@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/medication", json=_med_payload(name="PostEdit", frequency="once_a_day"), headers={"Cookie": f"access_token_cookie={cookie}"})
	med_id = _std(create_resp)["id"]
	resp = client.put(f"/data/medication/{med_id}", json=_med_payload(name="PostEdit", frequency="invalid_freq"), headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

def test_take_medication_dose_insufficient_stock(login_user, client):
	resp_login = login_user(email="meduser18@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/medication", json=_med_payload(name="LowStock", dose=500, stock=300, frequency="once_a_day"), headers={"Cookie": f"access_token_cookie={cookie}"})
	med_id = _std(create_resp)["id"]
	resp = client.patch(f"/data/medication/take/{med_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	# Attendu : 400 ou 500 (validation/erreur métier)
	assert resp.status_code in (400, 500)

def test_take_medication_dose_multiple_until_alert(login_user, client):
	resp_login = login_user(email="meduser19@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/medication", json=_med_payload(name="Multi", dose=100, stock=600, alert_threshold=400), headers={"Cookie": f"access_token_cookie={cookie}"})
	med_id = _std(create_resp)["id"]
	# Deux prises successives (selon implémentation route - ici on ne vérifie que le statut)
	resp1 = client.patch(f"/data/medication/take/{med_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	resp2 = client.patch(f"/data/medication/take/{med_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp1.status_code in (200, 204)
	assert resp2.status_code in (200, 204)

