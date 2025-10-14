import json
from app import db
from app.models.health_professional import HealthProfessional
from app.models.user import User

def _std(resp):
	return resp.get_json() if resp.is_json else {}

def _extract_access_cookie(resp):
	cookies = resp.headers.getlist("Set-Cookie")
	for c in cookies:
		if c.startswith("access_token_cookie="):
			return c.split(";", 1)[0].split("=", 1)[1]
	return None

def _pro_payload(name="Dr. Test", specialty="généraliste", phone="0601020304", **overrides):
	base = {
		"name": name,
		"specialty": specialty,
		"phone": phone,
	}
	base.update(overrides)
	return base

# --------------------------- Tests CREATE -------------------------------------
def test_create_health_professional_success(login_user, client):
	resp_login = login_user(email="prouser@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _pro_payload(name="Dr. House", specialty="diagnostic", phone="0600000000")
	resp = client.post("/data/healthprofessional", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 201
	assert body["name"] == "Dr. House"
	assert body["specialty"] == "diagnostic"

def test_create_health_professional_missing_fields(login_user, client):
	resp_login = login_user(email="promissing@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = {"name": "Dr. Missing"}  # specialty/phone manquants
	resp = client.post("/data/healthprofessional", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

# --------------------------- Tests READ ---------------------------------------
def test_read_health_professional_success(login_user, client):
	resp_login = login_user(email="proread@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _pro_payload(name="Dr. Read", specialty="cardio", phone="0600000001")
	client.post("/data/healthprofessional", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	resp = client.get("/data/healthprofessional", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert any(e.get("name") == "Dr. Read" for e in body)

def test_read_health_professional_not_found(login_user, client):
	resp_login = login_user(email="pronotfound@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/data/healthprofessional", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert isinstance(body, list)

# --------------------------- Tests UPDATE -------------------------------------
def test_update_health_professional_success(login_user, client):
	resp_login = login_user(email="proupdate@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _pro_payload(name="Dr. Update", specialty="neuro", phone="0600000002")
	resp_create = client.post("/data/healthprofessional", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	entry_id = _std(resp_create)["id"]
	resp = client.put(f"/data/healthprofessional/{entry_id}", json={"specialty": "psy"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["specialty"] == "psy"

def test_update_health_professional_unauthorized(client):
	resp = client.put("/data/healthprofessional/1", json={"specialty": "dermato"})
	assert resp.status_code in (401, 422)

# --------------------------- Tests DELETE -------------------------------------
def test_delete_health_professional_success(login_user, client):
	resp_login = login_user(email="prodelete@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _pro_payload(name="Dr. Delete", specialty="pédiatre", phone="0600000003")
	resp_create = client.post("/data/healthprofessional", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	entry_id = _std(resp_create)["id"]
	resp = client.delete(f"/data/healthprofessional/{entry_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert "success" in str(body).lower() or "deleted" in str(body).lower()

def test_delete_health_professional_unauthorized(client):
	resp = client.delete("/data/healthprofessional/1")
	assert resp.status_code in (401, 422)

# --------------------------- Tests JWT ----------------------------------------
def test_jwt_token_missing(client):
	resp = client.get("/data/healthprofessional")
	assert resp.status_code in (401, 422)

def test_jwt_token_invalid(client):
	resp = client.get("/data/healthprofessional", headers={"Cookie": "access_token_cookie=invalid"})
	assert resp.status_code in (401, 422)

# --------------------------- Tests Rôles --------------------------------------
def test_role_admin_access(create_admin_instance, client):
	admin = create_admin_instance(email="adminpro@example.com", username="adminpro")
	from flask_jwt_extended import create_access_token
	token = create_access_token(identity=admin.id)
	resp = client.get("/data/healthprofessional", headers={"Cookie": f"access_token_cookie={token}"})
	assert resp.status_code == 200

def test_role_user_access(login_user, client):
	resp_login = login_user(email="rolepro@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/data/healthprofessional", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code == 200

# --------------------------- Cas Limites --------------------------------------
def test_create_health_professional_invalid_phone(login_user, client):
	resp_login = login_user(email="probadphone@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _pro_payload(name="Dr. Bad", specialty="généraliste", phone="notaphone")
	resp = client.post("/data/healthprofessional", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

def test_create_health_professional_invalid_specialty(login_user, client):
	resp_login = login_user(email="probadsp@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _pro_payload(name="Dr. BadSp", specialty="invalid", phone="0600000004")
	resp = client.post("/data/healthprofessional", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body
