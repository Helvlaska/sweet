# tests/test_auth.py

import json
from app import db
from app.models.user import User


# --------------------------- Helpers internes ---------------------------------
def _std(resp):
    """Récupère le corps JSON d'une réponse Flask, ou un dict vide."""
    return resp.get_json() if resp.is_json else {}


def _extract_access_cookie(resp):
    """Extrait le cookie JWT access_token_cookie d'une réponse Flask."""
    cookies = resp.headers.getlist("Set-Cookie")
    for c in cookies:
        if c.startswith("access_token_cookie="):
            return c.split(";", 1)[0].split("=", 1)[1]
    return None


# --------------------------- Tests Register -----------------------------------
def test_create_user_success(client):
    """Vérifie qu'un utilisateur peut être créé avec succès."""
    payload = {
        "email": "alice@example.com",
        "username": "alice01",
        "password": "Password1!",
        "first_name": "Alice",
        "last_name": "Wonder",
        "gender": "prefer_not_say",
        "height": 170,
        "city": "Paris"
    }
    resp = client.post("/auth/register", json=payload)
    body = _std(resp)
    assert resp.status_code == 201
    assert "email" in body
    assert body["email"] == "alice@example.com"


def test_create_user_duplicate_email(client):
    """Vérifie qu'une tentative de création avec un email déjà utilisé échoue."""
    base_payload = {
        "email": "dup@example.com",
        "username": "dupuser",
        "password": "Password1!",
        "first_name": "Dup",
        "last_name": "User",
        "gender": "prefer_not_say",
        "height": 180,
        "city": "Paris",
    }
    client.post("/auth/register", json=base_payload)
    payload2 = {**base_payload, "username": "dupuser2"}
    resp = client.post("/auth/register", json=payload2)
    assert resp.status_code in (400, 409)


def test_create_user_invalid_password(client):
    """Vérifie qu'une création échoue avec un mot de passe trop faible."""
    payload = {
        "email": "bob@example.com",
        "username": "bob01",
        "password": "weak",
        "first_name": "Bob",
        "last_name": "Test",
        "gender": "prefer_not_say",
        "height": 175,
        "city": "Paris",
    }
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code in (400, 500)
    body = _std(resp)
    assert "error" in body or resp.status_code == 400


# --------------------------- Tests Login --------------------------------------
def test_login_user_success(client):
    """Vérifie qu'un utilisateur peut se connecter avec succès."""
    payload = {
        "email": "login@example.com",
        "username": "login01",
        "password": "Password1!",
        "first_name": "Login",
        "last_name": "Tester",
        "gender": "prefer_not_say",
        "height": 175,
        "city": "Paris",
    }
    client.post("/auth/register", json=payload)
    resp = client.post("/auth/login", json={"email": "login@example.com", "password": "Password1!"})
    body = _std(resp)
    assert resp.status_code == 200
    assert "message" in body
    assert "Authentification réussie" in body["message"]
    assert "Set-Cookie" in resp.headers


def test_login_user_invalid_password(client):
    """Vérifie qu'une tentative avec un mauvais mot de passe renvoie 401."""
    payload = {
        "email": "wrongpass@example.com",
        "username": "wronguser",
        "password": "Password1!",
        "first_name": "Wrong",
        "last_name": "Pass",
        "gender": "prefer_not_say",
        "height": 175,
        "city": "Paris",
    }
    client.post("/auth/register", json=payload)
    resp = client.post("/auth/login", json={"email": "wrongpass@example.com", "password": "BadPass1!"})
    assert resp.status_code == 401
    body = _std(resp)
    assert "error" in body


def test_login_user_missing_fields(client):
    """Vérifie qu'une requête sans mot de passe renvoie 400."""
    resp = client.post("/auth/login", json={"email": "nofield@example.com"})
    assert resp.status_code == 400


# --------------------------- Tests JWT / Cookies ------------------------------
def test_jwt_token_missing_access_profile(client):
    """Vérifie qu'une requête sans JWT renvoie 401 ou 422."""
    resp = client.get("/auth/profile")
    assert resp.status_code in (401, 422)


def test_jwt_token_invalid_access_profile(client):
    """Vérifie qu'un token JWT invalide renvoie 401 ou 422."""
    resp = client.get("/auth/profile", headers={"Cookie": "access_token_cookie=invalid"})
    assert resp.status_code in (401, 422)


# --------------------------- Tests Profile GET/PUT ----------------------------
def test_read_profile_success(client):
    """Vérifie qu'un utilisateur connecté peut lire son profil."""
    payload = {
        "email": "profile@example.com",
        "username": "profileuser",
        "password": "Password1!",
        "first_name": "Profile",
        "last_name": "User",
        "gender": "prefer_not_say",
        "height": 175,
        "city": "Paris",
    }
    client.post("/auth/register", json=payload)
    resp_login = client.post("/auth/login", json={"email": "profile@example.com", "password": "Password1!"})
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/auth/profile", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert "email" in body
    assert body["email"] == "profile@example.com"


def test_update_profile_success(client):
    """Vérifie qu'un utilisateur connecté peut mettre à jour son profil."""
    payload = {
        "email": "editprofile@example.com",
        "username": "edituser",
        "password": "Password1!",
        "first_name": "Edit",
        "last_name": "Profile",
        "gender": "prefer_not_say",
        "height": 170,
        "city": "Paris",
    }
    client.post("/auth/register", json=payload)
    resp_login = client.post("/auth/login", json={"email": "editprofile@example.com", "password": "Password1!"})
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/auth/profile", json={"city": "Lyon"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert "city" in body
    assert body["city"] == "Lyon"


# --------------------------- Tests Password Update ----------------------------
def test_update_password_success(client):
    """Vérifie qu'un utilisateur peut changer son mot de passe s'il est connecté."""
    payload = {
        "email": "pwdchange@example.com",
        "username": "pwduser",
        "password": "Password1!",
        "first_name": "Pwd",
        "last_name": "Change",
        "gender": "prefer_not_say",
        "height": 170,
        "city": "Paris",
    }
    client.post("/auth/register", json=payload)
    resp_login = client.post("/auth/login", json={"email": "pwdchange@example.com", "password": "Password1!"})
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/auth/password", json={"new_password": "NewPassword1!"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200
    body = _std(resp)
    assert "message" in body
    assert "Password updated" in body["message"]


def test_update_password_missing_jwt(client):
    """Vérifie qu'une mise à jour de mot de passe sans JWT échoue."""
    resp = client.put("/auth/password", json={"new_password": "NewPassword1!"})
    assert resp.status_code in (401, 422)


# --------------------------- Tests Logout -------------------------------------
def test_logout_success(client):
    """Vérifie qu'un utilisateur peut se déconnecter avec succès."""
    payload = {
        "email": "logout@example.com",
        "username": "logoutuser",
        "password": "Password1!",
        "first_name": "Logout",
        "last_name": "User",
        "gender": "prefer_not_say",
        "height": 170,
        "city": "Paris",
    }
    client.post("/auth/register", json=payload)
    resp_login = client.post("/auth/login", json={"email": "logout@example.com", "password": "Password1!"})
    cookie = _extract_access_cookie(resp_login)
    resp = client.post("/auth/logout", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert "message" in body
    assert "Logout" in body["message"]


def test_logout_missing_token(client):
    """Vérifie qu'une déconnexion sans JWT échoue."""
    resp = client.post("/auth/logout")
    assert resp.status_code in (401, 422)


# --------------------------- Tests Reset Password -----------------------------
def test_reset_password_request_success(client):
    """Vérifie qu'une demande de reset password fonctionne."""
    payload = {
        "email": "reset@example.com",
        "username": "resetuser",
        "password": "Password1!",
        "first_name": "Reset",
        "last_name": "Test",
        "gender": "prefer_not_say",
        "height": 175,
        "city": "Paris",
    }
    client.post("/auth/register", json=payload)
    resp = client.post("/auth/reset", json={"email": "reset@example.com"})
    assert resp.status_code in (200, 201)


def test_reset_password_request_invalid_email(client):
    """Vérifie qu'un email invalide renvoie 400."""
    resp = client.post("/auth/reset", json={"email": "invalid"})
    assert resp.status_code == 400


def test_reset_password_confirm_invalid_token(client):
    """Vérifie qu'un token invalide est refusé."""
    resp = client.put("/auth/reset/invalidtoken", json={"new_password": "Password2!"})
    assert resp.status_code in (400, 401)
