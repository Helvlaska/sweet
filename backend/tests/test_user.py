import json
from app import db
from app.models.user import User

def _std(resp):
	return resp.get_json() if resp.is_json else {}

# --------------------------- Tests CREATE -------------------------------------
def test_create_user_success(register_user):
	resp = register_user(email="usertest@example.com", username="usertest")
	body = _std(resp)
	assert resp.status_code == 201
	assert body["status"] == "success"
	assert body["data"]["email"] == "usertest@example.com"

def test_create_user_missing_fields(client):
	payload = {
		"email": "missing@example.com",
		# username manquant
		"password": "Password1!",
		"first_name": "Test",
		"last_name": "User",
		"gender": "prefer_not_say",
		"height": 170,
		"city": "Paris",
	}
	resp = client.post("/auth/register", json=payload)
	body = _std(resp)
	assert body.get("status") == "error" or resp.status_code in (400, 500)

# --------------------------- Tests READ ---------------------------------------
def test_read_user_success(login_user, client):
	resp_login = login_user(email="readuser@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/auth/profile", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"
	assert body["data"]["email"] == "readuser@example.com"

def test_read_user_not_found(client):
	# Accès profil sans JWT
	resp = client.get("/auth/profile")
	assert resp.status_code in (401, 422)

# --------------------------- Tests UPDATE -------------------------------------
def test_update_user_success(login_user, client):
	resp_login = login_user(email="updateuser@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.put("/auth/profile", json={"city": "Marseille"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"
	assert body["data"]["city"] == "Marseille"

def test_update_user_unauthorized(client):
	resp = client.put("/auth/profile", json={"city": "Nice"})
	assert resp.status_code in (401, 422)

# --------------------------- Tests DELETE -------------------------------------
def test_delete_user_success(create_user_instance, app):
	user = create_user_instance(email="deleteuser@example.com", username="deleteuser")
	user_id = user.id
	user.delete()
	found = User.query.filter_by(id=user_id).first()
	assert found is None

def test_delete_user_unauthorized(client):
	# Suppression via API non exposée, mais on vérifie que l'accès direct sans JWT échoue
	resp = client.delete("/auth/profile")
	assert resp.status_code in (401, 404, 405)

# --------------------------- Tests JWT ----------------------------------------
def test_jwt_token_missing(client):
	resp = client.get("/auth/profile")
	assert resp.status_code in (401, 422)

def test_jwt_token_invalid(client):
	resp = client.get("/auth/profile", headers={"Cookie": "access_token_cookie=invalid"})
	assert resp.status_code in (401, 422)

# --------------------------- Tests Rôles --------------------------------------
def test_role_admin_access(create_admin_instance, client):
	admin = create_admin_instance(email="adminuser@example.com", username="adminuser")
	from flask_jwt_extended import create_access_token
	token = create_access_token(identity=admin.id)
	resp = client.get("/auth/profile", headers={"Cookie": f"access_token_cookie={token}"})
	assert resp.status_code == 200

def test_role_user_access(login_user, client):
	resp_login = login_user(email="roleuser@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/auth/profile", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code == 200

# --------------------------- Cas Limites --------------------------------------
def test_update_user_invalid_field(login_user, client):
	resp_login = login_user(email="invalidfield@example.com")
	cookie = _extract_access_cookie(resp_login)
	# Champ non existant
	resp = client.put("/auth/profile", json={"not_a_field": "value"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert body["status"] == "error" or resp.status_code in (400, 500)

def test_create_user_invalid_email(client):
	payload = {
		"email": "notanemail",
		"username": "bademail",
		"password": "Password1!",
		"first_name": "Test",
		"last_name": "User",
		"gender": "prefer_not_say",
		"height": 170,
		"city": "Paris",
	}
	resp = client.post("/auth/register", json=payload)
	body = _std(resp)
	assert body.get("status") == "error" or resp.status_code in (400, 500)

# --------------------------- Utilitaires tests --------------------------------
def _extract_access_cookie(resp):
	cookies = resp.headers.getlist("Set-Cookie")
	for c in cookies:
		if c.startswith("access_token_cookie="):
			return c.split(";", 1)[0].split("=", 1)[1]
	return None
