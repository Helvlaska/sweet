import json
from app import db
from app.models.weight import Weight
from app.models.user import User

def _std(resp):
	return resp.get_json() if resp.is_json else {}

def _extract_access_cookie(resp):
	cookies = resp.headers.getlist("Set-Cookie")
	for c in cookies:
		if c.startswith("access_token_cookie="):
			return c.split(";", 1)[0].split("=", 1)[1]
	return None

def _weight_payload(value=70.00, **overrides):
	base = {
		"mass": value,
	}
	base.update(overrides)
	return base

# --------------------------- Tests CREATE -------------------------------------
def test_create_weight_success(login_user, client):
	resp_login = login_user(email="weightuser@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _weight_payload(value=72.50)
	resp = client.post("/data/weight", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 201
	assert body["mass"] == 72.50

def test_create_weight_missing_fields(login_user, client):
	resp_login = login_user(email="weightmissing@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = {"mass": "soixante"}  # time manquant
	resp = client.post("/data/weight", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

# --------------------------- Tests READ ---------------------------------------
def test_read_weight_success(login_user, client):
	resp_login = login_user(email="weightread@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _weight_payload(value=68.0)
	client.post("/data/weight", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	resp = client.get("/data/weight", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert any(e.get("mass") == 68.0 for e in body)

def test_read_weight_not_found(login_user, client):
	resp_login = login_user(email="weightnotfound@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/data/weight", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert isinstance(body, list)

# --------------------------- Tests UPDATE -------------------------------------
def test_update_weight_success(login_user, client):
	resp_login = login_user(email="weightupdate@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _weight_payload(value=75.0)
	resp_create = client.post("/data/weight", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	entry_id = _std(resp_create)["id"]
	resp = client.put(f"/data/weight/{entry_id}", json={"mass": 80.0}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["mass"] == 80.0

def test_update_weight_unauthorized(client):
	resp = client.put("/data/weight/1", json={"mass": 65.0})
	assert resp.status_code in (401, 422)

# --------------------------- Tests DELETE -------------------------------------
def test_delete_weight_success(login_user, client):
	resp_login = login_user(email="weightdelete@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _weight_payload(value=60.0)
	resp_create = client.post("/data/weight", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	entry_id = _std(resp_create)["id"]
	resp = client.delete(f"/data/weight/{entry_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert "success" in str(body).lower() or "deleted" in str(body).lower()

def test_delete_weight_unauthorized(client):
	resp = client.delete("/data/weight/1")
	assert resp.status_code in (401, 422)

# --------------------------- Tests JWT ----------------------------------------
def test_jwt_token_missing(client):
	resp = client.get("/data/weight")
	assert resp.status_code in (401, 422)

def test_jwt_token_invalid(client):
	resp = client.get("/data/weight", headers={"Cookie": "access_token_cookie=invalid"})
	assert resp.status_code in (401, 422)

# --------------------------- Tests Rôles --------------------------------------
def test_role_user_access(login_user, client):
	resp_login = login_user(email="roleweight@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/data/weight", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code == 200

# --------------------------- Cas Limites --------------------------------------
def test_create_weight_invalid_value(login_user, client):
	resp_login = login_user(email="weightbadval@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _weight_payload(value=-10, time="12:00")
	resp = client.post("/data/weight", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

# --------------------------- Test Statistiques --------------------------------
def test_weight_bmi_calculation(login_user, client):
	resp_login = login_user(email="weightstats@example.com")
	cookie = _extract_access_cookie(resp_login)
	# Ajout de plusieurs mesures
	client.post("/data/weight", json=_weight_payload(value=70.0, time="08:00"), headers={"Cookie": f"access_token_cookie={cookie}"})
	client.post("/data/weight", json=_weight_payload(value=80.0, time="12:00"), headers={"Cookie": f"access_token_cookie={cookie}"})
	resp = client.get("/data/weight/stats", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert "average" in body or "moyenne" in str(body).lower()
