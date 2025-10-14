import json
from app import db
from app.models.user import User


# --------------------------- Helpers internes ---------------------------------
def _std(resp):
	return resp.get_json() if resp.is_json else {}


# --------------------------- Tests Register -----------------------------------
def test_create_user_success(register_user):
	resp = register_user(email="alice@example.com", username="alice01")
	body = _std(resp)
	assert resp.status_code == 201
	assert body["status"] == "success"
	assert body["data"]["email"] == "alice@example.com"


def test_create_user_duplicate_email(register_user):
	register_user(email="dup@example.com", username="dup1")
	resp = register_user(email="dup@example.com", username="dup2")
	assert resp.status_code == 400
	body = _std(resp)
	assert body["status"] == "error"
	assert "déjà utilisé" in body["message"].lower()


def test_create_user_invalid_password(client):
	payload = {
		"email": "bob@example.com",
		"username": "bob01",
		"password": "weak",  # Ne respecte pas PASSWORD_PATTERN
		"first_name": "Bob",
		"last_name": "Test",
		"gender": "prefer_not_say",
		"height": 175,
		"city": "Paris",
	}
	resp = client.post("/auth/register", json=payload)
	# Validation échoue côté setter -> 500 ou 400 selon gestion; on vérifie que ce n'est pas success
	body = _std(resp)
	assert body.get("status") == "error" or resp.status_code in (400, 500)


# --------------------------- Tests Login --------------------------------------
def test_login_user_success(login_user):
	resp = login_user(email="login@example.com", password="Password1!")
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"
	assert "Set-Cookie" in resp.headers


def test_login_user_invalid_password(login_user, client):
	# Création user
	login_user(email="wrongpass@example.com", password="Password1!", ensure_registered=True)
	# Tentative avec mauvais mdp
	resp = client.post("/auth/login", json={"email": "wrongpass@example.com", "password": "BadPass1!"})
	body = _std(resp)
	assert resp.status_code == 401
	assert body["status"] == "error"


def test_login_user_missing_fields(client):
	resp = client.post("/auth/login", json={"email": "nofield@example.com"})
	body = _std(resp)
	assert resp.status_code == 400
	assert body["status"] == "error"


# --------------------------- Tests JWT / Cookies ------------------------------
def test_jwt_token_missing_access_profile(client):
	resp = client.get("/auth/profile")
	# flask_jwt_extended renverra typiquement 401 JSON
	assert resp.status_code in (401, 422)


def test_jwt_token_invalid_access_profile(client):
	resp = client.get("/auth/profile", headers={"Cookie": "access_token_cookie=invalid"})
	assert resp.status_code in (401, 422)


# --------------------------- Tests Profile GET/PUT ----------------------------
def test_read_profile_success(login_user, client):
	resp_login = login_user(email="profile@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/auth/profile", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"
	assert body["data"]["email"].endswith("profile@example.com")


def test_update_profile_success(login_user, client):
	resp_login = login_user(email="editprofile@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.put("/auth/profile", json={"city": "Lyon"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"
	assert body["data"]["city"] == "Lyon"


# --------------------------- Tests Password Update ----------------------------
def test_update_password_success(login_user, client):
	resp_login = login_user(email="pwdchange@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.put("/auth/password", json={"new_password": "NewPassword1!"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"


def test_update_password_missing_jwt(client):
	resp = client.put("/auth/password", json={"new_password": "NewPassword1!"})
	assert resp.status_code in (401, 422)


# --------------------------- Tests Logout -------------------------------------
def test_logout_success(login_user, client):
	resp_login = login_user(email="logout@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.post("/auth/logout", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"


def test_logout_missing_token(client):
	resp = client.post("/auth/logout")
	assert resp.status_code in (401, 422)


# --------------------------- Tests Reset Password -----------------------------
def test_reset_password_request_success(login_user, client):
	# user already created by login_user
	login_user(email="reset@example.com")
	resp = client.post("/auth/reset", json={"email": "reset@example.com"})
	# Selon implémentation validate_reset_request -> 201 puis find_user -> 201 etc.
	assert resp.status_code in (200, 201)


def test_reset_password_request_invalid_email(client):
	resp = client.post("/auth/reset", json={"email": "invalid"})
	assert resp.status_code == 400


def test_reset_password_confirm_invalid_token(client):
	resp = client.put("/auth/reset/invalidtoken", json={"new_password": "Password2!"})
	assert resp.status_code in (400, 401)


# --------------------------- Tests Rôles (placeholder) ------------------------
def test_access_protected_route_as_user(login_user, client):
	resp_login = login_user(email="roleuser@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/auth/profile", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code == 200


def test_access_protected_route_as_admin(create_admin_instance, client):
	admin = create_admin_instance(email="admin@example.com", username="adminuser")
	# login manually (simulate) -> need a token: easiest generate by hitting login endpoint
	from flask_jwt_extended import create_access_token
	token = create_access_token(identity=admin.id)
	resp = client.get("/auth/profile", headers={"Cookie": f"access_token_cookie={token}"})
	# Même endpoint accessible
	assert resp.status_code == 200


def test_access_protected_route_unauthorized(client):
	resp = client.get("/auth/profile")
	assert resp.status_code in (401, 422)


# --------------------------- Utilitaires tests --------------------------------
def _extract_access_cookie(resp):
	cookies = resp.headers.getlist("Set-Cookie")
	for c in cookies:
		if c.startswith("access_token_cookie="):
			return c.split(";", 1)[0].split("=", 1)[1]
	return None

