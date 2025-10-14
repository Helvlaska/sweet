import json
from app import db
from app.models.activity import Activity
from app.models.user import User

def _std(resp):
	return resp.get_json() if resp.is_json else {}

def _extract_access_cookie(resp):
	cookies = resp.headers.getlist("Set-Cookie")
	for c in cookies:
		if c.startswith("access_token_cookie="):
			return c.split(";", 1)[0].split("=", 1)[1]
	return None

def _activity_payload(description="marche", duration=30, **overrides):
	base = {
		"description": description,
		"duration": duration,
	}
	base.update(overrides)
	return base

# --------------------------- Tests CREATE -------------------------------------
def test_create_activity_success(login_user, client):
	resp_login = login_user(email="actuser@trucmuche.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _activity_payload(description="marche", duration=45)
	resp = client.post("/data/activity", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 201
	assert body["description"] == "marche"
	assert body["duration"] == 45

def test_create_activity_missing_fields(login_user, client):
	resp_login = login_user(email="actmissing@trucmuche.com")
	cookie = _extract_access_cookie(resp_login)
	payload = {"description": "marche"}  # duration manquant
	resp = client.post("/data/activity", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

# --------------------------- Tests READ ---------------------------------------
def test_read_activity_success(login_user, client):
	resp_login = login_user(email="actread@trucmuche.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _activity_payload(description="yoga", duration=60)
	resp_create = client.post("/data/activity", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	resp = client.get("/data/activity", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert any(e.get("description") == "yoga" for e in body)

def test_read_activity_not_found(login_user, client):
	resp_login = login_user(email="actnotfound@trucmuche.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/data/activity", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert isinstance(body, list)

# --------------------------- Tests UPDATE -------------------------------------
def test_update_activity_success(login_user, client):
	resp_login = login_user(email="actupdate@trucmuche.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _activity_payload(description="vélo", duration=20)
	resp_create = client.post("/data/activity", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	entry_id = _std(resp_create)["id"]
	resp = client.put(f"/data/activity/{entry_id}", json={"duration": 50}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["duration"] == 50

def test_update_activity_unauthorized(client):
	resp = client.put("/data/activity/1", json={"duration": 10})
	assert resp.status_code in (401, 422)

# --------------------------- Tests DELETE -------------------------------------
def test_delete_activity_success(login_user, client):
	resp_login = login_user(email="actdelete@trucmuche.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _activity_payload(description="natation", duration=30)
	resp_create = client.post("/data/activity", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	entry_id = _std(resp_create)["id"]
	resp = client.delete(f"/data/activity/{entry_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert "success" in str(body).lower() or "deleted" in str(body).lower()

def test_delete_activity_unauthorized(client):
	resp = client.delete("/data/activity/1")
	assert resp.status_code in (401, 422)

# --------------------------- Tests JWT ----------------------------------------
def test_jwt_token_missing(client):
	resp = client.get("/data/activity")
	assert resp.status_code in (401, 422)

def test_jwt_token_invalid(client):
	resp = client.get("/data/activity", headers={"Cookie": "access_token_cookie=invalid"})
	assert resp.status_code in (401, 422)

# --------------------------- Tests Rôles --------------------------------------
#def test_role_admin_access(create_admin_instance, client):
	#admin = create_admin_instance(email="adminact@trucmuche.com", username="adminact")
	#from flask_jwt_extended import create_access_token
	#token = create_access_token(identity=admin.id)
	#resp = client.get("/data/activity", headers={"Cookie": f"access_token_cookie={token}"})
	#assert resp.status_code == 200

#def test_role_user_access(login_user, client):
	#resp_login = login_user(email="roleact@trucmuche.com")
	#cookie = _extract_access_cookie(resp_login)
	#resp = client.get("/data/activity", headers={"Cookie": f"access_token_cookie={cookie}"})
	#assert resp.status_code == 200

# --------------------------- Cas Limites --------------------------------------
def test_create_activity_invalid_description(login_user, client):
	resp_login = login_user(email="actbaddesc@trucmuche.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _activity_payload(description="invalid", duration=30)
	resp = client.post("/data/activity", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

def test_create_activity_invalid_duration(login_user, client):
	resp_login = login_user(email="actbaddur@trucmuche.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _activity_payload(description="marche", duration=0)
	resp = client.post("/data/activity", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

# --------------------------- Test Statistiques --------------------------------
def test_activity_stats(login_user, client):
	resp_login = login_user(email="actstats@trucmuche.com")
	cookie = _extract_access_cookie(resp_login)
	# Ajout de plusieurs activités
	client.post("/data/activity", json=_activity_payload(description="marche", duration=30), headers={"Cookie": f"access_token_cookie={cookie}"})
	client.post("/data/activity", json=_activity_payload(description="vélo", duration=60), headers={"Cookie": f"access_token_cookie={cookie}"})
	resp = client.get("/data/activity/stats", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert "average" in body or "moyenne" in str(body).lower()
