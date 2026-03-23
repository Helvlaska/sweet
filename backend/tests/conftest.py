"""
[BACK][tests/conftest.py]

Shared test configuration and fixtures for the SWEET test suite.

Fixtures:
  app                           — application instance configured for testing (session scope)
  client                        — Flask test client
  clean_db                      — resets database state between each test (autouse)
  register_user                 — registers a user via POST /auth/register
  login_user                    — registers and logs in a user, returns login response
  auth_client                   — authenticated test client with JWT cookie pre-set
  create_admin_via_api          — creates an admin user via API and elevates role in DB
  create_admin_instance         — creates an admin user directly in DB
  create_health_professional    — creates a health professional, returns (pro_id, cookie)
"""

import time
import logging
import pytest
from app import create_app, db
from app.models.user import User


# ----------------------------- App & client -----------------------------------
@pytest.fixture(scope="session")
def app():
    """Create application instance configured for testing."""
    test_app = create_app("testing")
    test_app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    })
    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Return a Flask test client."""
    return app.test_client()


# ----------------------------- Database cleanup --------------------------------
@pytest.fixture(autouse=True)
def clean_db():
    """Reset database state between tests."""
    yield
    db.session.rollback()
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


# ----------------------------- Helpers ----------------------------------------
def _extract_cookie(response, name="access_token_cookie"):
    """Extract a named cookie value from a Flask response."""
    cookies = response.headers.getlist("Set-Cookie")
    for c in cookies:
        if c.startswith(f"{name}="):
            return c.split(";", 1)[0].split("=", 1)[1]
    return None


def _user_payload(email="user@trucmuche.com", username="user1", password="Password1!", **overrides):
    """Return a base user registration payload with optional overrides."""
    base = {
        "email": email,
        "username": username,
        "password": password,
        "first_name": "Jean",
        "last_name": "Dupont",
        "gender": "prefer_not_say",
        "height": 170,
        "city": "Paris",
    }
    base.update(overrides)
    return base


# ----------------------------- User fixtures ----------------------------------
@pytest.fixture()
def register_user(client):
    """Register a user via POST /auth/register."""
    def _create(**kwargs):
        payload = _user_payload(**kwargs)
        return client.post("/auth/register", json=payload)
    return _create


@pytest.fixture()
def login_user(client, register_user):
    """Register and log in a user. Returns the login response."""
    def _login(email="user@trucmuche.com", password="Password1!", remember_me=False, ensure_registered=True):
        if ensure_registered:
            register_user(email=email, username=email.split("@")[0], password=password)
        return client.post("/auth/login", json={
            "email": email,
            "password": password,
            "remember_me": remember_me
        })
    return _login


@pytest.fixture()
def auth_client(client, login_user):
    """Authenticated test client with JWT cookie pre-set."""
    class AuthClient:
        def __init__(self):
            self.base = client
            resp = login_user()
            self.access_cookie = _extract_cookie(resp)

        def _headers(self):
            if self.access_cookie:
                return {"Cookie": f"access_token_cookie={self.access_cookie}"}
            return {}

        def get(self, url, **kwargs):
            return self.base.get(url, headers=self._headers(), **kwargs)

        def post(self, url, **kwargs):
            return self.base.post(url, headers=self._headers(), **kwargs)

        def put(self, url, **kwargs):
            return self.base.put(url, headers=self._headers(), **kwargs)

        def delete(self, url, **kwargs):
            return self.base.delete(url, headers=self._headers(), **kwargs)

    return AuthClient()


# ----------------------------- Admin fixtures ---------------------------------
@pytest.fixture()
def create_admin_via_api(client):
    """Create an admin user via API then elevate role in DB. Returns (admin_user, cookie)."""
    def _create(email="admin@example.com", username="admin", password="Password1!", **overrides):
        payload = {
            "email": email,
            "username": username,
            "password": password,
            "first_name": "Admin",
            "last_name": "Tester",
            "gender": "prefer_not_say",
            "height": 180,
            "city": "Paris",
            **overrides,
        }
        resp = client.post("/auth/register", json=payload)
        assert resp.status_code == 201, resp.get_json()
        with client.application.app_context():
            admin = User.query.filter_by(_email=email).first()
            assert admin is not None
            admin.role = "admin"
            db.session.commit()
        resp_login = client.post("/auth/login", json={"email": email, "password": password})
        assert resp_login.status_code == 200, resp_login.get_data(as_text=True)
        cookie = _extract_cookie(resp_login)
        return admin, cookie
    return _create


@pytest.fixture()
def create_admin_instance(app):
    """Create an admin user directly in DB. Returns the User instance."""
    def _create(email="admin_instance@example.com", username="admin_instance", **kwargs):
        with app.app_context():
            user = User(
                email=email, # type: ignore
                username=username, # type: ignore
                first_name="Admin", # type: ignore
                last_name="Instance", # type: ignore
                gender="prefer_not_say", # type: ignore
                height=175, # type: ignore
                city="Paris", # type: ignore
            )
            user.password_hash = "Password1!"
            user.role = "admin"
            db.session.add(user)
            db.session.commit()
            return User.query.filter_by(_email=email).first()
    return _create


# ----------------------------- Health professional fixture --------------------
@pytest.fixture()
def create_health_professional(client, login_user):
    """Register a user, log in, and create a health professional. Returns (pro_id, cookie)."""
    def _create(email="prouser@trucmuche.com", **overrides):
        resp_login = login_user(email=email)
        cookie = _extract_cookie(resp_login)
        payload = {
            "fullname": "Dr. Test",
            "speciality": "general_practitioner",
            **overrides
        }
        resp = client.post(
            "/data/health_professionals/",
            json=payload,
            headers={"Cookie": f"access_token_cookie={cookie}"}
        )
        assert resp.status_code == 201, resp.get_json()
        pro_id = resp.get_json()["id"]
        return pro_id, cookie
    return _create


# ----------------------------- Session hooks ----------------------------------
@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Log test session start."""
    session.start_time = time.time()
    logging.getLogger().info("Début de la session de tests SWEET")


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Log test session summary."""
    duration = time.time() - session.start_time
    minutes, seconds = divmod(duration, 60)
    summary = f"Durée totale : {int(minutes)}min {int(seconds)}s"

    if exitstatus == 0:
        result = "✅ Tous les tests ont réussi !"
    elif exitstatus == 1:
        result = "❌ Certains tests ont échoué."
    elif exitstatus == 2:
        result = "⚠️ Les tests ont été interrompus."
    else:
        result = f"❓ Code de sortie inattendu ({exitstatus})"

    logging.getLogger().info(f"\n--- Résumé session Pytest SWEET ---\n{result}\n{summary}\n")
