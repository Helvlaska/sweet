import pytest

# Helpers locaux
def _std(resp):
	return resp.get_json() if resp.is_json else {}

def _extract_access_cookie(resp):
	cookies = resp.headers.getlist("Set-Cookie")
	for c in cookies:
		if c.startswith("access_token_cookie="):
			return c.split(";", 1)[0].split("=", 1)[1]
	return None

def _pro_payload(fullname="Dr. Note", speciality="diabetologist", phone="0601112233", **overrides):
	base = {"fullname": fullname, "speciality": speciality, "phone": phone}
	base.update(overrides)
	return base

def _note_payload(title="Consultation", content="Compte rendu de la consultation avec recommandations.", **overrides):
	base = {"title": title, "content": content}
	base.update(overrides)
	return base

# --------------------------- SETUP ENTITY -----------------------------------
def _create_professional(client, cookie, fullname="Dr. Note", speciality="general_practitioner"):
	payload = _pro_payload(fullname=fullname, speciality=speciality)
	resp = client.post("/data/healthprofessional", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	return _std(resp)

def _create_note(client, cookie, professional_id, title="Consultation", content="Compte rendu de la consultation avec recommandations."):
	payload = _note_payload(title=title, content=content)
	resp = client.post(f"/data/note/{professional_id}", json=payload, headers={"Cookie": f"access_token_cookie={cookie}"})
	return resp

# --------------------------- CREATE -----------------------------------------
def test_create_note_success(login_user, client):
	resp_login = login_user(email="noteuser@example.com")
	cookie = _extract_access_cookie(resp_login)
	pro = _create_professional(client, cookie)
	resp = _create_note(client, cookie, pro["id"], title="Suivi", content="Recommandations détaillées sur le traitement.")
	body = _std(resp)
	assert resp.status_code == 201
	assert body["title"] == "Suivi"

def test_create_note_missing_fields(login_user, client):
	resp_login = login_user(email="noteuser2@example.com")
	cookie = _extract_access_cookie(resp_login)
	pro = _create_professional(client, cookie)
	resp = client.post(f"/data/note/{pro['id']}", json={"title": "Sans contenu"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

def test_create_note_invalid_title(login_user, client):
	resp_login = login_user(email="noteuser3@example.com")
	cookie = _extract_access_cookie(resp_login)
	pro = _create_professional(client, cookie)
	resp = _create_note(client, cookie, pro["id"], title="A", content="Valid content with enough length.")
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

def test_create_note_invalid_content(login_user, client):
	resp_login = login_user(email="noteuser4@example.com")
	cookie = _extract_access_cookie(resp_login)
	pro = _create_professional(client, cookie)
	resp = _create_note(client, cookie, pro["id"], title="Titre valide", content="Court")
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

# --------------------------- READ -------------------------------------------
def test_read_note_success(login_user, client):
	resp_login = login_user(email="noteuser5@example.com")
	cookie = _extract_access_cookie(resp_login)
	pro = _create_professional(client, cookie)
	_create_note(client, cookie, pro["id"], title="Consult 1", content="Un contenu adéquat et suffisamment long.")
	resp = client.get(f"/data/note/{pro['id']}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert isinstance(body, list) and any(n.get("title") == "Consult 1" for n in body)

def test_read_note_not_found(login_user, client):
	resp_login = login_user(email="noteuser6@example.com")
	cookie = _extract_access_cookie(resp_login)
	# Aucun pro créé => accès à un ID inexistant
	resp = client.get(f"/data/note/00000000-0000-0000-0000-000000000000", headers={"Cookie": f"access_token_cookie={cookie}"})
	# Peut retourner 200 liste vide ou 404 selon implémentation service
	assert resp.status_code in (200, 404)

# --------------------------- UPDATE -----------------------------------------
def test_update_note_success(login_user, client):
	resp_login = login_user(email="noteuser7@example.com")
	cookie = _extract_access_cookie(resp_login)
	pro = _create_professional(client, cookie)
	create_resp = _create_note(client, cookie, pro["id"], title="Initial", content="Un contenu adéquat et suffisamment long.")
	note_id = _std(create_resp)["id"]
	resp = client.put(f"/data/note/{note_id}", json={"title": "Modifié"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert body["title"] == "Modifié"

def test_update_note_unauthorized(client):
	resp = client.put("/data/note/1", json={"title": "Modif"})
	assert resp.status_code in (401, 422)

# --------------------------- DELETE -----------------------------------------
def test_delete_note_success(login_user, client):
	resp_login = login_user(email="noteuser8@example.com")
	cookie = _extract_access_cookie(resp_login)
	pro = _create_professional(client, cookie)
	create_resp = _create_note(client, cookie, pro["id"], title="A supprimer", content="Contenu suffisant pour suppression.")
	note_id = _std(create_resp)["id"]
	resp = client.delete(f"/data/note/{note_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code == 200
	assert "success" in str(body).lower() or "deleted" in str(body).lower()

def test_delete_note_unauthorized(client):
	resp = client.delete("/data/note/1")
	assert resp.status_code in (401, 422)

# --------------------------- JWT --------------------------------------------
def test_jwt_token_missing(client):
	resp = client.get("/data/note/123")
	assert resp.status_code in (401, 422)

def test_jwt_token_invalid(client):
	resp = client.get("/data/note/123", headers={"Cookie": "access_token_cookie=invalid"})
	assert resp.status_code in (401, 422)

# --------------------------- RÔLES ------------------------------------------
def test_role_user_access(login_user, client):
	resp_login = login_user(email="noteuser9@example.com")
	cookie = _extract_access_cookie(resp_login)
	pro = _create_professional(client, cookie)
	resp = client.get(f"/data/note/{pro['id']}", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code in (200, 204)

# --------------------------- Cas Limites ------------------------------------
def test_update_note_invalid_title(login_user, client):
	resp_login = login_user(email="noteuser10@example.com")
	cookie = _extract_access_cookie(resp_login)
	pro = _create_professional(client, cookie)
	create_resp = _create_note(client, cookie, pro["id"], title="Valid", content="Contenu valide suffisant.")
	note_id = _std(create_resp)["id"]
	resp = client.put(f"/data/note/{note_id}", json={"title": "A"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

def test_update_note_invalid_content(login_user, client):
	resp_login = login_user(email="noteuser11@example.com")
	cookie = _extract_access_cookie(resp_login)
	pro = _create_professional(client, cookie)
	create_resp = _create_note(client, cookie, pro["id"], title="Valid2", content="Contenu valide suffisant.")
	note_id = _std(create_resp)["id"]
	resp = client.put(f"/data/note/{note_id}", json={"content": "Court"}, headers={"Cookie": f"access_token_cookie={cookie}"})
	body = _std(resp)
	assert resp.status_code in (400, 500) or "error" in body

def test_delete_note_not_found(login_user, client):
	resp_login = login_user(email="noteuser12@example.com")
	cookie = _extract_access_cookie(resp_login)
	resp = client.delete(f"/data/note/00000000-0000-0000-0000-000000000000", headers={"Cookie": f"access_token_cookie={cookie}"})
	assert resp.status_code in (404, 400, 200)  # selon implémentation (idempotent)

