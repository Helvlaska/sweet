import json
from app import db
from app.models.comment import Comment
from app.models.user import User

def _std(resp):
	return resp.get_json() if resp.is_json else {}

# --------------------------- Helpers ------------------------------------------
def _extract_access_cookie(resp):
	cookies = resp.headers.getlist("Set-Cookie")
	for c in cookies:
		if c.startswith("access_token_cookie="):
			return c.split(";", 1)[0].split("=", 1)[1]
	return None

def _comment_payload(content="Un commentaire", **overrides):
	base = {
		"content": content,
	}
	base.update(overrides)
	return base

# --------------------------- Tests CREATE -------------------------------------
def test_create_comment_success(login_user, client):
	resp_login = login_user(email="comuser@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _comment_payload(content="Commentaire Test")
	resp = client.post("/comments/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 201
	assert body["status"] == "success"
	assert body["data"]["content"] == "Commentaire Test"

def test_create_comment_missing_fields(login_user, client):
	resp_login = login_user(email="commissing@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = {}  # content manquant
	resp = client.post("/comments/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert body.get("status") == "error" or resp.status_code in (400, 500)

# --------------------------- Tests READ ---------------------------------------
def test_read_comment_success(login_user, client):
	resp_login = login_user(email="comread@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _comment_payload(content="Lire")
	resp_create = client.post("/comments/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	comment_id = _std(resp_create)["data"]["id"]
	resp = client.get(f"/comments/{comment_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"
	assert body["data"]["content"] == "Lire"

def test_read_comment_not_found(login_user, client):
	resp_login = login_user(email="comnotfound@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/comments/999999", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 404 or body.get("status") == "error"

# --------------------------- Tests UPDATE -------------------------------------
def test_update_comment_success(login_user, client):
	resp_login = login_user(email="comupdate@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _comment_payload(content="Avant")
	resp_create = client.post("/comments/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	comment_id = _std(resp_create)["data"]["id"]
	resp = client.put(f"/comments/{comment_id}", json={"content": "Après"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"
	assert body["data"]["content"] == "Après"

def test_update_comment_unauthorized(client):
	resp = client.put("/comments/1", json={"content": "NoJWT"})
	assert resp.status_code in (401, 422)

# --------------------------- Tests DELETE -------------------------------------
def test_delete_comment_success(login_user, client):
	resp_login = login_user(email="comdelete@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _comment_payload(content="A supprimer")
	resp_create = client.post("/comments/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	comment_id = _std(resp_create)["data"]["id"]
	resp = client.delete(f"/comments/{comment_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"

def test_delete_comment_unauthorized(client):
	resp = client.delete("/comments/1")
	assert resp.status_code in (401, 422)

# --------------------------- Tests JWT ----------------------------------------
def test_jwt_token_missing(client):
	resp = client.get("/comments/1")
	assert resp.status_code in (401, 422)

def test_jwt_token_invalid(client):
	resp = client.get("/comments/1", headers={"Cookie": "access_token_cookie=invalid"})
	assert resp.status_code in (401, 422)

# --------------------------- Tests Rôles --------------------------------------
def test_role_admin_access(create_admin_instance, client):
	admin = create_admin_instance(email="admincom@example.com", username="admincom")
	from flask_jwt_extended import create_access_token
	token = create_access_token(identity=admin.id)
	resp = client.get("/comments/", headers={"Cookie": f"access_token_cookie={token}"})
	assert resp.status_code == 200

def test_role_user_access(login_user, client):
	resp_login = login_user(email="rolecom@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/comments/", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code == 200

# --------------------------- Cas Limites --------------------------------------
def test_create_comment_invalid_content(login_user, client):
	resp_login = login_user(email="combadcontent@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _comment_payload(content="")
	resp = client.post("/comments/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert body.get("status") == "error" or resp.status_code in (400, 500)

def test_update_comment_invalid_field(login_user, client):
	resp_login = login_user(email="combadfield@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _comment_payload(content="BadField")
	resp_create = client.post("/comments/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	comment_id = _std(resp_create)["data"]["id"]
	resp = client.put(f"/comments/{comment_id}", json={"not_a_field": "value"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert body.get("status") == "error" or resp.status_code in (400, 500)
