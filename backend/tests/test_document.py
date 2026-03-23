"""
[BACK][tests/test_health_document.py]

Test suite — document_bp blueprint
(/data/health_professionals/<health_professional_id>/documents)

Covers:
  - Nominal flow (upload, read, update, delete)
  - Validation errors (missing body, invalid file, limit reached)
  - Authentication errors (missing token)
  - Edge cases (document not found, 10-document limit)

Fixtures: client, login_user, create_health_professional (defined in conftest.py)
"""

import base64
from app import db
from app.models.health_document import HealthDocument


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


def _make_base64_file(content=b"fake pdf content"):
    """Return a base64-encoded string simulating a file."""
    return base64.b64encode(content).decode("utf-8")


def _document_payload(filename="test.pdf", **overrides):
    """Return a single document dict for use inside a documents list."""
    base = {
        "filename": filename,
        "file": _make_base64_file()
    }
    base.update(overrides)
    return base


def _upload_payload(*docs):
    """Wrap one or more document dicts into the expected request format."""
    return {"documents": list(docs)}


# ----------------------------- Create -----------------------------------------
def test_create_document_success(client, create_health_professional):
    """POST /documents/ — valid upload returns 201 and document data."""
    pro_id, cookie = create_health_professional(email="docupload@trucmuche.com")
    payload = _upload_payload(_document_payload("rapport.pdf"))
    resp = client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        json=payload,
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    body = _std(resp)
    assert resp.status_code == 201
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["filename"] == "rapport.pdf"


def test_create_multiple_documents_success(client, create_health_professional):
    """POST /documents/ — uploading multiple documents returns 201."""
    pro_id, cookie = create_health_professional(email="docmulti@trucmuche.com")
    payload = _upload_payload(
        _document_payload("doc1.pdf"),
        _document_payload("doc2.jpg")
    )
    resp = client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        json=payload,
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    body = _std(resp)
    assert resp.status_code == 201
    assert len(body) == 2


def test_create_document_missing_body(client, create_health_professional):
    """POST /documents/ — missing body returns 400."""
    pro_id, cookie = create_health_professional(email="docmissingbody@trucmuche.com")
    resp = client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    assert resp.status_code == 400


def test_create_document_empty_list(client, create_health_professional):
    """POST /documents/ — empty documents list returns 400."""
    pro_id, cookie = create_health_professional(email="docempty@trucmuche.com")
    resp = client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        json={"documents": []},
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    assert resp.status_code == 400


def test_create_document_missing_filename(client, create_health_professional):
    """POST /documents/ — document without filename returns 400."""
    pro_id, cookie = create_health_professional(email="docnofilename@trucmuche.com")
    payload = _upload_payload({"file": _make_base64_file()})
    resp = client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        json=payload,
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    assert resp.status_code == 400


def test_create_document_invalid_extension(client, create_health_professional):
    """POST /documents/ — forbidden extension returns 422."""
    pro_id, cookie = create_health_professional(email="docbadext@trucmuche.com")
    payload = _upload_payload(_document_payload("malware.exe"))
    resp = client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        json=payload,
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_document_limit_reached(client, create_health_professional):
    """POST /documents/ — uploading more than 10 documents returns 422."""
    pro_id, cookie = create_health_professional(email="doclimit@trucmuche.com")
    for i in range(10):
        client.post(
            f"/data/health_professionals/{pro_id}/documents/",
            json=_upload_payload(_document_payload(f"doc{i}.pdf")),
            headers={"Cookie": f"access_token_cookie={cookie}"}
        )
    resp = client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        json=_upload_payload(_document_payload("doc11.pdf")),
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_create_document_missing_token(client, create_health_professional):
    """POST /documents/ — missing JWT returns 401."""
    pro_id, _ = create_health_professional(email="doctokenless@trucmuche.com")
    payload = _upload_payload(_document_payload("test.pdf"))
    fresh_client = client.application.test_client()
    resp = fresh_client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        json=payload
    )
    assert resp.status_code == 401


# ----------------------------- Read -------------------------------------------
def test_get_documents_success(client, create_health_professional):
    """GET /documents/ — returns list of documents for a professional."""
    pro_id, cookie = create_health_professional(email="docread@trucmuche.com")
    client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        json=_upload_payload(_document_payload("bilan.pdf")),
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    resp = client.get(
        f"/data/health_professionals/{pro_id}/documents/",
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert len(body) == 1


def test_get_documents_empty(client, create_health_professional):
    """GET /documents/ — returns empty list when no documents exist."""
    pro_id, cookie = create_health_professional(email="docreadempty@trucmuche.com")
    resp = client.get(
        f"/data/health_professionals/{pro_id}/documents/",
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    body = _std(resp)
    assert resp.status_code == 200
    assert isinstance(body, list)
    assert len(body) == 0


def test_get_documents_missing_token(client, create_health_professional):
    """GET /documents/ — missing JWT returns 401."""
    pro_id, _ = create_health_professional(email="docreadtoken@trucmuche.com")
    fresh_client = client.application.test_client()
    resp = fresh_client.get(
        f"/data/health_professionals/{pro_id}/documents/"
    )
    assert resp.status_code == 401


# ----------------------------- Update -----------------------------------------
def test_update_document_success(client, create_health_professional):
    """PUT /documents/<id> — valid update returns 200."""
    pro_id, cookie = create_health_professional(email="docupdate@trucmuche.com")
    resp_create = client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        json=_upload_payload(_document_payload("avant.pdf")),
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    doc_id = _std(resp_create)[0]["id"]
    resp = client.put(
        f"/data/health_professionals/{pro_id}/documents/{doc_id}",
        json={"filename": "apres.pdf"},
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    body = _std(resp)
    assert resp.status_code == 200
    assert body["filename"] == "apres.pdf"


def test_update_document_not_found(client, create_health_professional):
    """PUT /documents/<id> — unknown document id returns 404."""
    pro_id, cookie = create_health_professional(email="docupdatenotfound@trucmuche.com")
    resp = client.put(
        f"/data/health_professionals/{pro_id}/documents/id-inexistant",
        json={"filename": "nouveau.pdf"},
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    assert resp.status_code == 404


def test_update_document_missing_body(client, create_health_professional):
    """PUT /documents/<id> — missing body returns 400."""
    pro_id, cookie = create_health_professional(email="docupdatebody@trucmuche.com")
    resp_create = client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        json=_upload_payload(_document_payload("test.pdf")),
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    doc_id = _std(resp_create)[0]["id"]
    resp = client.put(
        f"/data/health_professionals/{pro_id}/documents/{doc_id}",
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    assert resp.status_code == 400


def test_update_document_invalid_extension(client, create_health_professional):
    """PUT /documents/<id> — invalid filename extension returns 422."""
    pro_id, cookie = create_health_professional(email="docupdatebadext@trucmuche.com")
    resp_create = client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        json=_upload_payload(_document_payload("test.pdf")),
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    doc_id = _std(resp_create)[0]["id"]
    resp = client.put(
        f"/data/health_professionals/{pro_id}/documents/{doc_id}",
        json={"filename": "virus.exe"},
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    body = _std(resp)
    assert resp.status_code == 422
    assert "error" in body


def test_update_document_missing_token(client):
    """PUT /documents/<id> — missing JWT returns 401."""
    resp = client.put(
        "/data/health_professionals/some-pro/documents/some-doc",
        json={"filename": "test.pdf"}
    )
    assert resp.status_code == 401


# ----------------------------- Delete -----------------------------------------
def test_delete_document_success(client, create_health_professional):
    """DELETE /documents/<id> — valid delete returns 204."""
    pro_id, cookie = create_health_professional(email="docdelete@trucmuche.com")
    resp_create = client.post(
        f"/data/health_professionals/{pro_id}/documents/",
        json=_upload_payload(_document_payload("asupprimer.pdf")),
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    doc_id = _std(resp_create)[0]["id"]
    resp = client.delete(
        f"/data/health_professionals/{pro_id}/documents/{doc_id}",
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    assert resp.status_code == 204


def test_delete_document_not_found(client, create_health_professional):
    """DELETE /documents/<id> — unknown document id returns 404."""
    pro_id, cookie = create_health_professional(email="docdeletenotfound@trucmuche.com")
    resp = client.delete(
        f"/data/health_professionals/{pro_id}/documents/id-inexistant",
        headers={"Cookie": f"access_token_cookie={cookie}"}
    )
    assert resp.status_code == 404


def test_delete_document_missing_token(client):
    """DELETE /documents/<id> — missing JWT returns 401."""
    resp = client.delete(
        "/data/health_professionals/some-pro/documents/some-doc"
    )
    assert resp.status_code == 401
