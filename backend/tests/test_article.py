import json
from app import db
from app.models.article import Article
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

def _article_payload(title="Un article", content="Contenu d'article", **overrides):
	base = {
		"title": title,
		"content": content,
	}
	base.update(overrides)
	return base

# --------------------------- Tests CREATE -------------------------------------
def test_create_article_success(login_user, client):
	resp_login = login_user(email="artuser@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _article_payload(title="Article Test", content="Contenu test")
	resp = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 201
	assert body["status"] == "success"
	assert body["data"]["title"] == "Article Test"

def test_create_article_missing_fields(login_user, client):
	resp_login = login_user(email="artmissing@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = {"title": "Sans contenu"}  # content manquant
	resp = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert body.get("status") == "error" or resp.status_code in (400, 500)

# --------------------------- Tests READ ---------------------------------------
def test_read_article_success(login_user, client):
	resp_login = login_user(email="artread@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _article_payload(title="Lire", content="Contenu")
	resp_create = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	article_id = _std(resp_create)["data"]["id"]
	resp = client.get(f"/articles/{article_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"
	assert body["data"]["title"] == "Lire"

def test_read_article_not_found(login_user, client):
	resp_login = login_user(email="artnotfound@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/articles/999999", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 404 or body.get("status") == "error"

# --------------------------- Tests UPDATE -------------------------------------
def test_update_article_success(login_user, client):
	resp_login = login_user(email="artupdate@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _article_payload(title="Avant", content="Avant")
	resp_create = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	article_id = _std(resp_create)["data"]["id"]
	resp = client.put(f"/articles/{article_id}", json={"title": "Après"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"
	assert body["data"]["title"] == "Après"

def test_update_article_unauthorized(client):
	resp = client.put("/articles/1", json={"title": "NoJWT"})
	assert resp.status_code in (401, 422)

# --------------------------- Tests DELETE -------------------------------------
def test_delete_article_success(login_user, client):
	resp_login = login_user(email="artdelete@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _article_payload(title="A supprimer", content="Contenu")
	resp_create = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	article_id = _std(resp_create)["data"]["id"]
	resp = client.delete(f"/articles/{article_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["status"] == "success"

def test_delete_article_unauthorized(client):
	resp = client.delete("/articles/1")
	assert resp.status_code in (401, 422)

# --------------------------- Tests LIKE ---------------------------------------
def test_like_article_toggle(login_user, client):
	resp_login = login_user(email="artlike@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _article_payload(title="Like", content="Contenu")
	resp_create = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	article_id = _std(resp_create)["data"]["id"]
	# Like
	resp_like = client.post(f"/articles/{article_id}/like", headers={"Cookie": f"access_token_cookie={cookie}"})
	body_like = _std(resp_like)
	assert resp_like.status_code == 200
	assert body_like["status"] == "success"
	# Unlike
	resp_unlike = client.post(f"/articles/{article_id}/like", headers={"Cookie": f"access_token_cookie={cookie}"})
	body_unlike = _std(resp_unlike)
	assert resp_unlike.status_code == 200
	assert body_unlike["status"] == "success"

# --------------------------- Tests JWT ----------------------------------------
def test_jwt_token_missing(client):
	resp = client.get("/articles/1")
	assert resp.status_code in (401, 422)

def test_jwt_token_invalid(client):
	resp = client.get("/articles/1", headers={"Cookie": "access_token_cookie=invalid"})
	assert resp.status_code in (401, 422)

# --------------------------- Tests Rôles --------------------------------------
def test_role_admin_access(create_admin_instance, client):
	admin = create_admin_instance(email="adminart@example.com", username="adminart")
	from flask_jwt_extended import create_access_token
	token = create_access_token(identity=admin.id)
	resp = client.get("/articles/", headers={"Cookie": f"access_token_cookie={token}"})
	assert resp.status_code == 200

def test_role_user_access(login_user, client):
	resp_login = login_user(email="roleart@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.get("/articles/", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code == 200

# --------------------------- Cas Limites --------------------------------------
def test_create_article_invalid_title(login_user, client):
	resp_login = login_user(email="artbadtitle@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _article_payload(title="", content="Contenu")
	resp = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert body.get("status") == "error" or resp.status_code in (400, 500)

def test_update_article_invalid_field(login_user, client):
	resp_login = login_user(email="artbadfield@example.com")
	cookie = _extract_access_cookie(resp_login)
	payload = _article_payload(title="BadField", content="Contenu")
	resp_create = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	article_id = _std(resp_create)["data"]["id"]
	resp = client.put(f"/articles/{article_id}", json={"not_a_field": "value"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert body.get("status") == "error" or resp.status_code in (400, 500)
