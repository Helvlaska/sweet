import pytest
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash
import time
import logging


@pytest.fixture(scope="session")
def app():
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
	return app.test_client()


def _user_payload(email="user@trucmuche.com", username="user1", password="Password1!", **overrides):
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


@pytest.fixture()
def register_user(client):
	created = {}
	def _create(**kwargs):
		payload = _user_payload(**kwargs)
		resp = client.post("/auth/register", json=payload)
		created["last_response"] = resp
		return resp
	return _create


#@pytest.fixture()
#def create_user_instance(app):
	#def _create(**kwargs):
		#payload = _user_payload(**kwargs)
		#user = User(**payload)
		#user.password_hash = payload["password"]
		#db.session.add(user)
		#db.session.commit()
		#return payload
	#return _create
def _extract_cookie(resp, name="access_token_cookie"):
	cookies = resp.headers.getlist("Set-Cookie")
	for c in cookies:
		if c.startswith(f"{name}="):
			return c.split(";", 1)[0].split("=", 1)[1]
	return None

@pytest.fixture()
def create_admin_via_api(client):
	"""
	Crée un admin en utilisant /auth/register puis élève son rôle en DB.
	Retourne (admin_user, access_cookie)
	"""
	def _create_admin(email="admin@example.com", username="admin", password="Password1!", **overrides):
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
		# 1) créer le compte via l’API
		resp = client.post("/auth/register", json=payload)
		assert resp.status_code == 201, resp.get_json()

		# 2) promouvoir en admin (même DB que le client)
		with client.application.app_context():
			admin = User.query.filter_by(_email=email).first()
			assert admin is not None
			admin.role = "admin"
			db.session.commit()

		# 3) login pour récupérer le cookie JWT si besoin
		resp_login = client.post("/auth/login", json={"email": email, "password": password})
		assert resp_login.status_code == 200, resp_login.get_data(as_text=True)
		cookie = _extract_cookie(resp_login, "access_token_cookie")
		return admin, cookie

	return _create_admin


@pytest.fixture()
def login_user(client, register_user):
	def _login(email="user@trucmuche.com", password="Password1!", remember_me=False, ensure_registered=True):
		if ensure_registered:
			register_user(email=email, username=email.split('@')[0], password=password)
		resp = client.post("/auth/login", json={"email": email, "password": password, "remember_me": remember_me})
		return resp
	return _login


def extract_cookie(response, name):
	cookies = response.headers.getlist('Set-Cookie')
	for c in cookies:
		if c.startswith(name + "="):
			return c.split(';', 1)[0].split('=', 1)[1]
	return None

@pytest.fixture(autouse=True)
def clean_db():
	"""Reset database between tests."""
	yield
	db.session.rollback()
	for table in reversed(db.metadata.sorted_tables):
		db.session.execute(table.delete())
	db.session.commit()

@pytest.fixture()
def auth_client(client, login_user):
	class AuthClient:
		def __init__(self):
			self.base = client
			resp = login_user()
			self.access_cookie = extract_cookie(resp, 'access_token_cookie')

		def get(self, url, **kwargs):
			return self.base.get(url, headers=self._headers(), **kwargs)

		def post(self, url, **kwargs):
			return self.base.post(url, headers=self._headers(), **kwargs)

		def put(self, url, **kwargs):
			return self.base.put(url, headers=self._headers(), **kwargs)

		def _headers(self):
			headers = kwargs = {}
			if self.access_cookie:
				headers['Cookie'] = f"access_token_cookie={self.access_cookie}"
			return headers
	return AuthClient()

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
	"""Appelé au démarrage des tests"""
	session.start_time = time.time()
	logging.getLogger().info("🚀 Début de la session de tests SWEET")


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
	"""Appelé à la fin des tests"""
	duration = time.time() - session.start_time
	minutes, seconds = divmod(duration, 60)
	summary = f"⏱️ Durée totale : {int(minutes)}min {int(seconds)}s"

	if exitstatus == 0:
		result = "✅ Tous les tests ont réussi !"
	elif exitstatus == 1:
		result = "❌ Certains tests ont échoué."
	elif exitstatus == 2:
		result = "⚠️ Les tests ont été interrompus."
	else:
		result = f"❓ Code de sortie inattendu ({exitstatus})"

	logging.getLogger().info(f"\n--- Résumé session Pytest SWEET ---\n{result}\n{summary}\n")
