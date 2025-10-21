import json
from app import db
from app.models.article import Article
from app.models.user import User

def _std(resp):
    """Récupère le corps JSON d’une réponse Flask."""
    return resp.get_json() if resp.is_json else {}

def _extract_access_cookie(resp):
    """Extrait le cookie JWT access_token_cookie de la réponse de login."""
    cookies = resp.headers.getlist("Set-Cookie")
    for c in cookies:
        if c.startswith("access_token_cookie="):
            return c.split(";", 1)[0].split("=", 1)[1]
    return None

def _article_payload(title="Un article", content="Contenu valide d’article", **overrides):
    base = {"title": title, "content": content}
    base.update(overrides)
    return base


# --------------------------- CREATE ------------------------------------------
def test_create_article_success(client, create_admin_via_api):
    # 1️⃣ Création d’un admin via la fixture
    admin, cookie = create_admin_via_api(email="adminart@example.com", username="adminart")
    payload = {"title": "Article Test", "content": "Ceci est un contenu de test suffisamment long pour passer la validation."}
    resp = client.post("/data/article/", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = resp.get_json()
    assert resp.status_code == 201, f"Erreur inattendue: {body}"
    assert body.get("status") == "success"
    assert "data" in body
    assert body["data"]["title"] == "Article Test"
    assert body["data"]["content"].startswith("Ceci est un contenu de test")
    assert body["data"]["id"] is not None


def test_create_article_missing_fields(create_admin_instance, client):
    admin = create_admin_instance()
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=admin.id)

    payload = {"title": "Sans contenu"}  # content manquant
    resp = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={token}"})
    body = _std(resp)
    assert resp.status_code == 400
    assert "error" in body

def test_create_article_invalid_title(create_admin_instance, client):
    admin = create_admin_instance()
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=admin.id)

    payload = _article_payload(title="", content="Contenu suffisant")
    resp = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={token}"})
    body = _std(resp)
    assert resp.status_code in (400, 422)
    assert "error" in body

# --------------------------- READ -------------------------------------------
def test_read_article_success(create_admin_instance, client):
    admin = create_admin_instance()
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=admin.id)

    payload = _article_payload(title="Lire", content="Contenu à lire")
    resp_create = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={token}"})
    article_id = _std(resp_create)["data"]["id"]

    resp = client.get(f"/articles/{article_id}", headers={"Cookie": f"access_token_cookie={token}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["data"]["title"] == "Lire"

def test_read_article_not_found(create_admin_instance, client):
    admin = create_admin_instance()
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=admin.id)

    resp = client.get("/articles/999999", headers={"Cookie": f"access_token_cookie={token}"})
    assert resp.status_code == 404

# --------------------------- UPDATE -----------------------------------------
def test_update_article_success(create_admin_instance, client):
    admin = create_admin_instance()
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=admin.id)

    payload = _article_payload(title="Avant", content="Contenu initial")
    resp_create = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={token}"})
    article_id = _std(resp_create)["data"]["id"]

    resp = client.put(f"/articles/{article_id}", json={"title": "Après"}, headers={"Cookie": f"access_token_cookie={token}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["data"]["title"] == "Après"

def test_update_article_invalid_field(create_admin_instance, client):
    admin = create_admin_instance()
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=admin.id)

    payload = _article_payload(title="BadField", content="Contenu correct")
    resp_create = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={token}"})
    article_id = _std(resp_create)["data"]["id"]

    resp = client.put(f"/articles/{article_id}", json={"not_a_field": "value"}, headers={"Cookie": f"access_token_cookie={token}"})
    body = _std(resp)
    assert resp.status_code == 400

# --------------------------- DELETE ------------------------------------------
def test_delete_article_success(create_admin_instance, client):
    admin = create_admin_instance()
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=admin.id)

    payload = _article_payload(title="A supprimer", content="Contenu temporaire")
    resp_create = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={token}"})
    article_id = _std(resp_create)["data"]["id"]

    resp = client.delete(f"/articles/{article_id}", headers={"Cookie": f"access_token_cookie={token}"})
    body = _std(resp)
    assert resp.status_code in (200, 204)
    assert "success" in str(body).lower() or body == {}

def test_delete_article_not_found(create_admin_instance, client):
    admin = create_admin_instance()
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=admin.id)
    resp = client.delete("/articles/999999", headers={"Cookie": f"access_token_cookie={token}"})
    assert resp.status_code == 404

# --------------------------- LIKE -------------------------------------------
def test_like_article_toggle(create_admin_instance, client):
    admin = create_admin_instance()
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=admin.id)

    payload = _article_payload(title="Like", content="Contenu test like")
    resp_create = client.post("/articles/", json=payload, headers={"Cookie": f"access_token_cookie={token}"})
    article_id = _std(resp_create)["data"]["id"]

    # Like
    resp_like = client.post(f"/articles/{article_id}/like", headers={"Cookie": f"access_token_cookie={token}"})
    assert resp_like.status_code == 200

    # Unlike
    resp_unlike = client.post(f"/articles/{article_id}/like", headers={"Cookie": f"access_token_cookie={token}"})
    assert resp_unlike.status_code == 200
