import json
from app import db
from app.models.glycemia import Glycemia
from app.models.user import User

def _std(resp):
	return resp.get_json() if resp.is_json else {}

def _extract_access_cookie(resp):
	cookies = resp.headers.getlist("Set-Cookie")
	for c in cookies:
		if c.startswith("access_token_cookie="):
			return c.split(";", 1)[0].split("=", 1)[1]
	return None

def _glycemia_payload(value=1.2, time="08:00", **overrides):
	base = {
		"value": value,
		"time": time,
	}
	base.update(overrides)
	return base

# --------------------------- Tests CREATE -------------------------------------
def test_create_glycemia_success(login_user, client):
	resp_login = login_user(email="glyuser@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _glycemia_payload(glucose_level=120)
	resp = client.post("/data/glycemia", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 201
	assert body["glucose_level"] == 120

def test_create_glycemia_missing_fields(login_user, client):
	resp_login = login_user(email="glymissing@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = {"value": 1.2}  # time manquant
	resp = client.post("/data/glycemia", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

# --------------------------- Tests READ ---------------------------------------
def test_read_glycemia_success(login_user, client):
	resp_login = login_user(email="glyread@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _glycemia_payload(glucose_level=90)
	client.post("/data/glycemia", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	resp = client.get("/data/glycemia", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert any(e.get("glucose_level") == 90 for e in body)

def test_read_glycemia_not_found(login_user, client):
	resp_login = login_user(email="glynotfound@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/data/glycemia", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert isinstance(body, list)

# --------------------------- Tests UPDATE -------------------------------------
def test_update_glycemia_success(login_user, client):
	resp_login = login_user(email="glyupdate@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _glycemia_payload(glucose_level=100)
	resp_create = client.post("/data/glycemia", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	entry_id = _std(resp_create)["id"]
	resp = client.put(f"/data/glycemia/{entry_id}", json={"glucose_level": 90}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["glucose_level"] == 90

def test_update_glycemia_unauthorized(client):
	resp = client.put("/data/glycemia/1", json={"glucose_level": 500})
	assert resp.status_code in (401, 422)

# --------------------------- Tests DELETE -------------------------------------
def test_delete_glycemia_success(login_user, client):
	resp_login = login_user(email="glydelete@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _glycemia_payload(glucose_level=110)
	resp_create = client.post("/data/glycemia", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	entry_id = _std(resp_create)["id"]
	resp = client.delete(f"/data/glycemia/{entry_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert "success" in str(body).lower() or "deleted" in str(body).lower()

def test_delete_glycemia_unauthorized(client):
	resp = client.delete("/data/glycemia/1")
	assert resp.status_code in (401, 422)

# --------------------------- Tests JWT ----------------------------------------
def test_jwt_token_missing(client):
	resp = client.get("/data/glycemia")
	assert resp.status_code in (401, 422)

def test_jwt_token_invalid(client):
	resp = client.get("/data/glycemia", headers={"Cookie": "access_token_cookie=invalid"})
	assert resp.status_code in (401, 422)

# --------------------------- Tests Rôles --------------------------------------
def test_role_user_access(login_user, client):
	resp_login = login_user(email="rolegly@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/data/glycemia", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code == 200

# --------------------------- Cas Limites --------------------------------------
def test_create_glycemia_invalid_value(login_user, client):
	resp_login = login_user(email="glybadval@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _glycemia_payload(glucose_level=20)
	resp = client.post("/data/glycemia", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

# --------------------------- Test Statistiques --------------------------------
def test_glycemia_calculation(login_user, client):
	resp_login = login_user(email="glystats@example.com")
	cookie = _extract_access_cookie(resp_login)
	# Ajout de plusieurs mesures
	client.post("/data/glycemia", json=_glycemia_payload(glucose_level=110), headers={"Cookie": f"access_token_cookie={cookie}"})
	client.post("/data/glycemia", json=_glycemia_payload(vglucose_level=120), headers={"Cookie": f"access_token_cookie={cookie}"})
	client.post("/data/glycemia", json=_glycemia_payload(vglucose_level=99), headers={"Cookie": f"access_token_cookie={cookie}"})
	resp = client.get("/data/glycemia/stats", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert "average" in body or "moyenne" in str(body).lower()
