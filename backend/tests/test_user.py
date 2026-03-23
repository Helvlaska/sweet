"""
[BACK][tests/test_user.py]

Test suite — user profile CRUD via auth_bp (/auth/profile, /auth/password)

Covers:
  - Nominal flow (read, update profile and password)
  - Validation errors (invalid data, missing fields)
  - Authentication errors (missing or invalid token)
  - Authorization errors (unauthenticated access)
  - Edge cases (unknown field, invalid field value)

Fixtures: client, register_user, login_user, create_admin_via_api,
          create_admin_instance (defined in conftest.py)
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


# ----------------------------- Read Profile -----------------------------------
def test_read_profile_success(login_user, client):
    """GET /auth/profile — authenticated user can read their profile."""
    resp_login = login_user(email="readuser@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/auth/profile", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["email"] == "readuser@example.com"


def test_read_profile_missing_token(client):
    """GET /auth/profile — missing JWT returns 401."""
    resp = client.get("/auth/profile")
    assert resp.status_code == 401


def test_read_profile_invalid_token(client):
    """GET /auth/profile — invalid JWT returns 401."""
    resp = client.get("/auth/profile", headers={"Cookie": "access_token_cookie=invalid"})
    assert resp.status_code == 401


# ----------------------------- Update Profile ---------------------------------
def test_update_profile_success(login_user, client):
    """PUT /auth/profile — authenticated user can update their profile."""
    resp_login = login_user(email="updateuser@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/auth/profile", json={"city": "Marseille"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["city"] == "Marseille"


def test_update_profile_missing_token(client):
    """PUT /auth/profile — missing JWT returns 401."""
    resp = client.put("/auth/profile", json={"city": "Nice"})
    assert resp.status_code == 401


def test_update_profile_missing_body(login_user, client):
    """PUT /auth/profile — missing body returns 400."""
    resp_login = login_user(email="emptybody@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/auth/profile", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_update_profile_invalid_value(login_user, client):
    """PUT /auth/profile — invalid field value (height out of range) returns 422."""
    resp_login = login_user(email="invalidvalue@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/auth/profile", json={"height": -5}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_profile_unknown_field(login_user, client):
    """PUT /auth/profile — unknown field is silently ignored, returns 200."""
    resp_login = login_user(email="unknownfield@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/auth/profile", json={"not_a_field": "value"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200


def test_update_profile_invalid_gender(login_user, client):
    """PUT /auth/profile — invalid gender value returns 422."""
    resp_login = login_user(email="invalidgender@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/auth/profile", json={"gender": "invalid"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


# ----------------------------- Update Password --------------------------------
def test_update_password_success(login_user, client):
    """PUT /auth/password — authenticated user can change their password."""
    resp_login = login_user(email="pwdchange@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/auth/password", json={"new_password": "NewPassword1!"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert "Password updated" in body["message"]


def test_update_password_missing_token(client):
    """PUT /auth/password — missing JWT returns 401."""
    resp = client.put("/auth/password", json={"new_password": "NewPassword1!"})
    assert resp.status_code == 401


def test_update_password_missing_field(login_user, client):
    """PUT /auth/password — missing new_password field returns 400."""
    resp_login = login_user(email="missingpwd@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/auth/password", json={}, headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_update_password_invalid_value(login_user, client):
    """PUT /auth/password — weak new password returns 422."""
    resp_login = login_user(email="weakpwd@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.put("/auth/password", json={"new_password": "weak"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


# ----------------------------- Delete (model level) ---------------------------
def test_delete_user_success(create_admin_instance, app):
    """User.delete() — user is removed from the database."""
    with app.app_context():
        user = create_admin_instance(email="deleteuser@example.com", username="deleteuser")
        user_id = user.id
        user.delete()
        found = User.query.filter_by(id=user_id).first()
        assert found is None


# ----------------------------- Role Access ------------------------------------
def test_role_admin_access(client, create_admin_via_api):
    """GET /auth/profile — admin user can access their profile."""
    admin, cookie = create_admin_via_api(email="adminaccess@example.com", username="adminaccess")
    resp = client.get("/auth/profile", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200


def test_role_user_access(login_user, client):
    """GET /auth/profile — standard user can access their profile."""
    resp_login = login_user(email="roleuser@example.com")
    cookie = _extract_access_cookie(resp_login)
    resp = client.get("/auth/profile", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200
