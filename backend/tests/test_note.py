"""
[BACK][tests/test_note.py]

Test suite — note_bp blueprint
(/data/health_professionals/<health_professional_id>/notes)

Covers:
  - Nominal flow (create, read, update, delete)
  - Validation errors (missing body, invalid title, invalid content)
  - Authentication errors (missing token)
  - Edge cases (not found, empty list)

Fixtures: client, login_user, create_health_professional (defined in conftest.py)
"""

from app import db
from app.models.note import Note


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


def _note_payload(title="Consultation", content="Compte rendu détaillé de la consultation.", **overrides):
    """Return a base note payload with optional overrides."""
    base = {"title": title, "content": content}
    base.update(overrides)
    return base


# ----------------------------- Create -----------------------------------------
def test_create_note_success(client, create_health_professional):
    """POST /notes/ — valid payload returns 201."""
    pro_id, cookie = create_health_professional(email="noteuser@example.com")
    resp = client.post(f"/data/health_professionals/{pro_id}/notes/", json=_note_payload(title="Suivi"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body["title"] == "Suivi"


def test_create_note_missing_body(client, create_health_professional):
    """POST /notes/ — missing body returns 400."""
    pro_id, cookie = create_health_professional(email="notemissingbody@example.com")
    resp = client.post(f"/data/health_professionals/{pro_id}/notes/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_create_note_missing_fields(client, create_health_professional):
    """POST /notes/ — missing content returns 422."""
    pro_id, cookie = create_health_professional(email="noteuser2@example.com")
    resp = client.post(f"/data/health_professionals/{pro_id}/notes/", json={"title": "Sans contenu"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_note_invalid_title(client, create_health_professional):
    """POST /notes/ — title too short returns 422."""
    pro_id, cookie = create_health_professional(email="noteuser3@example.com")
    resp = client.post(f"/data/health_professionals/{pro_id}/notes/", json=_note_payload(title="A"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_note_invalid_content(client, create_health_professional):
    """POST /notes/ — content too short returns 422."""
    pro_id, cookie = create_health_professional(email="noteuser4@example.com")
    resp = client.post(f"/data/health_professionals/{pro_id}/notes/", json=_note_payload(content="Court"), headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_note_missing_token(client, create_health_professional):
    """POST /notes/ — missing JWT returns 401."""
    pro_id, cookie = create_health_professional(email="notetokenless@example.com")
    fresh_client = client.application.test_client()
    resp = fresh_client.post(f"/data/health_professionals/{pro_id}/notes/", json=_note_payload())
    assert resp.status_code == 401


# ----------------------------- Read -------------------------------------------
def test_read_notes_success(client, create_health_professional):
    """GET /notes/ — returns list of notes."""
    pro_id, cookie = create_health_professional(email="noteuser5@example.com")
    client.post(f"/data/health_professionals/{pro_id}/notes/", json=_note_payload(title="Consult 1"), headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get(f"/data/health_professionals/{pro_id}/notes/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert any(n.get("title") == "Consult 1" for n in body)


def test_read_notes_empty(client, create_health_professional):
    """GET /notes/ — returns empty list when no notes exist."""
    pro_id, cookie = create_health_professional(email="noteuser6@example.com")
    resp = client.get(f"/data/health_professionals/{pro_id}/notes/", headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert len(body) == 0


def test_read_notes_missing_token(client, create_health_professional):
    """GET /notes/ — missing JWT returns 401."""
    pro_id, cookie = create_health_professional(email="notereadtoken@example.com")
    fresh_client = client.application.test_client()
    resp = fresh_client.get(f"/data/health_professionals/{pro_id}/notes/")
    assert resp.status_code == 401


# ----------------------------- Update -----------------------------------------
def test_update_note_success(client, create_health_professional):
    """PUT /notes/<id> — valid update returns 200."""
    pro_id, cookie = create_health_professional(email="noteuser7@example.com")
    resp_create = client.post(f"/data/health_professionals/{pro_id}/notes/", json=_note_payload(title="Initial"), headers={"Cookie": f"access_token_cookie={cookie}"})
    note_id = _std(resp_create)["id"]
    resp = client.put(f"/data/health_professionals/{pro_id}/notes/{note_id}", json={"title": "Modifié"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["title"] == "Modifié"


def test_update_note_not_found(client, create_health_professional):
    """PUT /notes/<id> — unknown id returns 404."""
    pro_id, cookie = create_health_professional(email="noteupdatenotfound@example.com")
    resp = client.put(f"/data/health_professionals/{pro_id}/notes/id-inexistant", json=_note_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_update_note_missing_body(client, create_health_professional):
    """PUT /notes/<id> — missing body returns 400."""
    pro_id, cookie = create_health_professional(email="noteupdatebody@example.com")
    resp_create = client.post(f"/data/health_professionals/{pro_id}/notes/", json=_note_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    note_id = _std(resp_create)["id"]
    resp = client.put(f"/data/health_professionals/{pro_id}/notes/{note_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 400


def test_update_note_invalid_title(client, create_health_professional):
    """PUT /notes/<id> — invalid title returns 422."""
    pro_id, cookie = create_health_professional(email="noteuser10@example.com")
    resp_create = client.post(f"/data/health_professionals/{pro_id}/notes/", json=_note_payload(title="Valid"), headers={"Cookie": f"access_token_cookie={cookie}"})
    note_id = _std(resp_create)["id"]
    resp = client.put(f"/data/health_professionals/{pro_id}/notes/{note_id}", json={"title": "A"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_note_invalid_content(client, create_health_professional):
    """PUT /notes/<id> — invalid content returns 422."""
    pro_id, cookie = create_health_professional(email="noteuser11@example.com")
    resp_create = client.post(f"/data/health_professionals/{pro_id}/notes/", json=_note_payload(title="Valid2"), headers={"Cookie": f"access_token_cookie={cookie}"})
    note_id = _std(resp_create)["id"]
    resp = client.put(f"/data/health_professionals/{pro_id}/notes/{note_id}", json={"content": "Court"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_note_missing_token(client, create_health_professional):
    """PUT /notes/<id> — missing JWT returns 401."""
    pro_id, cookie = create_health_professional(email="notetokenmissupd@example.com")
    resp_create = client.post(f"/data/health_professionals/{pro_id}/notes/", json=_note_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    note_id = _std(resp_create)["id"]
    fresh_client = client.application.test_client()
    resp = fresh_client.put(f"/data/health_professionals/{pro_id}/notes/{note_id}", json=_note_payload())
    assert resp.status_code == 401


# ----------------------------- Delete -----------------------------------------
def test_delete_note_success(client, create_health_professional):
    """DELETE /notes/<id> — valid delete returns 204."""
    pro_id, cookie = create_health_professional(email="noteuser8@example.com")
    resp_create = client.post(f"/data/health_professionals/{pro_id}/notes/", json=_note_payload(title="A supprimer"), headers={"Cookie": f"access_token_cookie={cookie}"})
    note_id = _std(resp_create)["id"]
    resp = client.delete(f"/data/health_professionals/{pro_id}/notes/{note_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 204


def test_delete_note_not_found(client, create_health_professional):
    """DELETE /notes/<id> — unknown id returns 404."""
    pro_id, cookie = create_health_professional(email="noteuser12@example.com")
    resp = client.delete(f"/data/health_professionals/{pro_id}/notes/00000000-0000-0000-0000-000000000000", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 404


def test_delete_note_missing_token(client, create_health_professional):
    """DELETE /notes/<id> — missing JWT returns 401."""
    pro_id, cookie = create_health_professional(email="notetokenmissdel@example.com")
    resp_create = client.post(f"/data/health_professionals/{pro_id}/notes/", json=_note_payload(), headers={"Cookie": f"access_token_cookie={cookie}"})
    note_id = _std(resp_create)["id"]
    fresh_client = client.application.test_client()
    resp = fresh_client.delete(f"/data/health_professionals/{pro_id}/notes/{note_id}")
    assert resp.status_code == 401


# ----------------------------- Role access ------------------------------------
def test_role_user_access(client, create_health_professional):
    """GET /notes/ — standard user can access their notes."""
    pro_id, cookie = create_health_professional(email="noteuser9@example.com")
    resp = client.get(f"/data/health_professionals/{pro_id}/notes/", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200
