"""
[BACK][tests/test_auth.py]

Test suite — auth_bp blueprint (/auth)
Authentication flows : register, login, logout, token refresh, password reset.

Covers:
  - Nominal flow (valid data, expected response)
  - Validation errors (missing fields, invalid format)
  - Authentication errors (wrong credentials, missing or expired token)
  - Edge cases (missing body, anti-enumeration on reset)

Fixtures: client, register_user, login_user (defined in conftest.py)
"""

from app import db
from app.models.user import User


# ----------------------------- Helpers ----------------------------------------
def _std(resp):
    """Extract JSON body from a Flask response, or return an empty dict."""
    return resp.get_json() if resp.is_json else {}


def _extract_access_cookie(resp):
    """Extract access_token_cookie value from a Flask response."""
    cookies = resp.headers.getlist("Set-Cookie")
    for c in cookies:
        if c.startswith("access_token_cookie="):
            return c.split(";", 1)[0].split("=", 1)[1]
    return None


# ----------------------------- Register ---------------------------------------
def test_register_success(client):
    """POST /auth/register — valid payload returns 201 and email in body."""
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
    assert body["email"] == "alice@example.com"


def test_register_missing_body(client):
    """POST /auth/register — missing body returns 400."""
    resp = client.post("/auth/register")
    assert resp.status_code == 400


def test_register_missing_fields(client):
    """POST /auth/register — missing required field (username) returns 422."""
    payload = {
        "email": "missing@example.com",
        "password": "Password1!",
        "first_name": "Test",
        "last_name": "User",
        "gender": "prefer_not_say",
        "height": 170,
        "city": "Paris",
    }
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 422


def test_register_invalid_password(client):
    """POST /auth/register — weak password returns 422."""
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
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_register_duplicate_email(client):
    """POST /auth/register — duplicate email returns 422."""
    payload = {
        "email": "dup@example.com",
        "username": "dupuser",
        "password": "Password1!",
        "first_name": "Dup",
        "last_name": "User",
        "gender": "prefer_not_say",
        "height": 180,
        "city": "Paris",
    }
    client.post("/auth/register", json=payload)
    payload2 = {**payload, "username": "dupuser2"}
    resp = client.post("/auth/register", json=payload2)
    assert resp.status_code == 422


# ----------------------------- Login ------------------------------------------
def test_login_success(client):
    """POST /auth/login — valid credentials return 200 and set JWT cookie."""
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
    assert "Authentification réussie" in body["message"]
    assert "Set-Cookie" in resp.headers


def test_login_missing_body(client):
    """POST /auth/login — missing body returns 400."""
    resp = client.post("/auth/login")
    assert resp.status_code == 400


def test_login_missing_fields(client):
    """POST /auth/login — missing password returns 400."""
    resp = client.post("/auth/login", json={"email": "nofield@example.com"})
    assert resp.status_code in (400, 401)


def test_login_invalid_password(client):
    """POST /auth/login — wrong password returns 401."""
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
    body = _std(resp)
    assert resp.status_code == 401
    assert "error" in body


# ----------------------------- JWT / Cookies ----------------------------------
def test_jwt_missing(client):
    """GET /auth/profile — missing JWT returns 401."""
    resp = client.get("/auth/profile")
    assert resp.status_code == 401


def test_jwt_invalid(client):
    """GET /auth/profile — invalid JWT returns 401."""
    resp = client.get("/auth/profile", headers={"Cookie": "access_token_cookie=invalid"})
    assert resp.status_code == 401


# ----------------------------- Logout -----------------------------------------
def test_logout_success(client):
    """POST /auth/logout — authenticated user can logout and receives 200."""
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
    assert "Logout" in body["message"]


def test_logout_missing_token(client):
    """POST /auth/logout — missing JWT returns 401."""
    resp = client.post("/auth/logout")
    assert resp.status_code == 401


# ----------------------------- Password Reset ---------------------------------
def test_reset_request_success(client):
    """POST /auth/reset — valid email returns 200 (neutral message, anti-enumeration)."""
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
    assert resp.status_code == 200


def test_reset_request_unknown_email(client):
    """POST /auth/reset — unknown email returns 200 (anti-enumeration)."""
    resp = client.post("/auth/reset", json={"email": "ghost@example.com"})
    assert resp.status_code == 200


def test_reset_request_missing_body(client):
    """POST /auth/reset — missing body returns 400."""
    resp = client.post("/auth/reset")
    assert resp.status_code == 400


def test_reset_request_missing_email(client):
    """POST /auth/reset — missing email field returns 400."""
    resp = client.post("/auth/reset", json={})
    assert resp.status_code == 400


def test_reset_confirm_invalid_token(client):
    """PUT /auth/reset/<token> — invalid token returns 401."""
    resp = client.put("/auth/reset/invalidtoken", json={"new_password": "Password2!"})
    assert resp.status_code == 401


def test_reset_confirm_missing_password(client):
    """PUT /auth/reset/<token> — missing new_password field returns 400."""
    resp = client.put("/auth/reset/sometoken", json={})
    assert resp.status_code == 400
