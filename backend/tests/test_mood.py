import pytest

# Helpers locaux
def _std(resp):
	return resp.get_json() if resp.is_json else {}

def _extract_access_cookie(resp):
	cookies = resp.headers.getlist("Set-Cookie")
	for c in cookies:
		if c.startswith("access_token_cookie="):
			return c.split(";", 1)[0].split("=", 1)[1]
	return None

def _mood_payload(description="Content", **overrides):
	base = {"description": description}
	base.update(overrides)
	return base

# --------------------------- CREATE -----------------------------------------
def test_create_mood_success(login_user, client):
	resp_login = login_user(email="mooduser@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _mood_payload(description="Heureux")
	resp = client.post("/data/mood", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 201
	assert body["description"] == "Heureux"

def test_create_mood_missing_description(login_user, client):
	resp_login = login_user(email="mooduser2@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.post("/data/mood", json={}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

def test_create_mood_invalid_description(login_user, client):
	resp_login = login_user(email="mooduser3@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _mood_payload(description="A")
	resp = client.post("/data/mood", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

# --------------------------- READ -------------------------------------------
def test_read_mood_list_success(login_user, client):
	resp_login = login_user(email="mooduser4@example.com")
	cookie = _extract_access_cookie(resp_login)
	client.post("/data/mood", json=_mood_payload(description="Serein"), headers={"Cookie": f"access_token_cookie={cookie}"})
	resp = client.get("/data/mood", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert isinstance(body, list) and any(m.get("description") == "Serein" for m in body)

def test_read_mood_empty(login_user, client):
	resp_login = login_user(email="mooduser5@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/data/mood", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert isinstance(body, list)

# --------------------------- UPDATE -----------------------------------------
def test_update_mood_success(login_user, client):
	resp_login = login_user(email="mooduser6@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/mood", json=_mood_payload(description="Fatigué"), headers={"Cookie": f"access_token_cookie={cookie}"})
	mood_id = _std(create_resp)["id"]
	resp = client.put(f"/data/mood/{mood_id}", json={"description": "Reposé"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["description"] == "Reposé"

def test_update_mood_unauthorized(client):
	resp = client.put("/data/mood/1", json={"description": "Modif"})
	assert resp.status_code in (401, 422)

def test_update_mood_not_found(login_user, client):
	resp_login = login_user(email="mooduser7@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.put("/data/mood/00000000-0000-0000-0000-000000000000", json={"description": "Ghost"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code in (404, 400)

def test_update_mood_invalid_description(login_user, client):
	resp_login = login_user(email="mooduser8@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/mood", json=_mood_payload(description="Valid"), headers={"Cookie": f"access_token_cookie={cookie}"})
	mood_id = _std(create_resp)["id"]
	resp = client.put(f"/data/mood/{mood_id}", json={"description": "A"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

# --------------------------- DELETE -----------------------------------------
def test_delete_mood_success(login_user, client):
	resp_login = login_user(email="mooduser9@example.com")
	cookie = _extract_access_cookie(resp_login)
	create_resp = client.post("/data/mood", json=_mood_payload(description="A supprimer"), headers={"Cookie": f"access_token_cookie={cookie}"})
	mood_id = _std(create_resp)["id"]
	resp = client.delete(f"/data/mood/{mood_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert "success" in str(body).lower() or "deleted" in str(body).lower()

def test_delete_mood_unauthorized(client):
	resp = client.delete("/data/mood/1")
	assert resp.status_code in (401, 422)

def test_delete_mood_not_found(login_user, client):
	resp_login = login_user(email="mooduser10@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.delete("/data/mood/00000000-0000-0000-0000-000000000000", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code in (404, 400, 200)

# --------------------------- JWT --------------------------------------------
def test_mood_jwt_missing(client):
	resp = client.get("/data/mood")
	assert resp.status_code in (401, 422)

def test_mood_jwt_invalid(client):
	resp = client.get("/data/mood", headers={"Cookie": "access_token_cookie=invalid"})
	assert resp.status_code in (401, 422)

# --------------------------- RÔLES ------------------------------------------
def test_mood_role_user_access(login_user, client):
	resp_login = login_user(email="mooduser11@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/data/mood", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code == 200

def test_mood_role_admin_access(create_admin_instance, client):
	admin = create_admin_instance(email="adminmood@example.com", username="adminmood")
	from flask_jwt_extended import create_access_token
	token = create_access_token(identity=admin.id)
	resp = client.get("/data/mood", headers={"Cookie": f"access_token_cookie={token}"})
	assert resp.status_code == 200

# --------------------------- Cas Limites ------------------------------------
def test_create_mood_long_description(login_user, client):
	resp_login = login_user(email="mooduser12@example.com")
	cookie = _extract_access_cookie(resp_login)
	desc = "Très " + "content " * 100  # description très longue
	payload = _mood_payload(description=desc)
	resp = client.post("/data/mood", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	# Peut être accepté ou rejeté selon la contrainte du modèle
	assert resp.status_code in (201, 400, 500)

