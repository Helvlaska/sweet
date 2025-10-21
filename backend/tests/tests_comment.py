import json
import pytest
from app import db
from app.models.comment import Comment
from app.models.forum_post import ForumPost
from app.models.user import User


def _std(resp):
    return resp.get_json() if resp.is_json else {}


def _extract_access_cookie(resp):
    cookies = resp.headers.getlist("Set-Cookie")
    for c in cookies:
        if c.startswith("access_token_cookie="):
            return c.split(";", 1)[0].split("=", 1)[1]
    return None


def _forum_post_payload(title="Un post", content="Contenu du post", **overrides):
    base = {
        "title": title,
        "content": content,
    }
    base.update(overrides)
    return base


def _comment_payload(content="Un commentaire", **overrides):
    base = {
        "content": content,
    }
    base.update(overrides)
    return base

# --------------------------- Helpers -----------------------------------------


def _create_forum_post(client, login_user, email="user@trucmuche.com"):
    resp_login = login_user(email=email)
    cookie = _extract_access_cookie(resp_login)
    payload = _forum_post_payload(
        title="Post pour commentaire", content="Contenu")
    resp = client.post("/data/forum/posts", json=payload,
                       headers={"Cookie": f"access_token_cookie={cookie}"})
    post_id = _std(resp)["id"]
    return post_id, cookie

# --------------------------- CREATE ------------------------------------------


def test_create_comment_success(login_user, client):
    post_id, cookie = _create_forum_post(
        client, login_user, email="commentcreate@trucmuche.com")
    payload = _comment_payload(content="Commentaire Test")
    resp = client.post(f"/data/forum/posts/{post_id}/comments", json=payload, headers={
                       "Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 201
    assert body["content"] == "Commentaire Test"

# --------------------------- READ --------------------------------------------


def test_get_comments_by_post(login_user, client):
    post_id, cookie = _create_forum_post(
        client, login_user, email="commentget@trucmuche.com")
    payload = _comment_payload(content="Lecture commentaire")
    client.post(f"/data/forum/posts/{post_id}/comments", json=payload,
                headers={"Cookie": f"access_token_cookie={cookie}"})
    resp = client.get(f"/data/forum/posts/{post_id}/comments")
    assert resp.status_code == 200
    body = _std(resp)
    assert isinstance(body, list)
    assert any(c["content"] == "Lecture commentaire" for c in body)

# --------------------------- UPDATE ------------------------------------------


def test_update_comment_success(login_user, client):
    post_id, cookie = _create_forum_post(
        client, login_user, email="commentupdate@trucmuche.com")
    payload = _comment_payload(content="Avant")
    resp_create = client.post(f"/data/forum/posts/{post_id}/comments", json=payload, headers={
                              "Cookie": f"access_token_cookie={cookie}"})
    comment_id = _std(resp_create)["id"]
    resp = client.put(f"/data/forum/comments/{comment_id}", json={
                      "content": "Après"}, headers={"Cookie": f"access_token_cookie={cookie}"})
    body = _std(resp)
    assert resp.status_code == 200
    assert body["content"] == "Après"


def test_update_comment_not_author(login_user, client):
    post_id, cookie1 = _create_forum_post(
        client, login_user, email="authorcomment@trucmuche.com")
    payload = _comment_payload(content="Auteur")
    resp_create = client.post(f"/data/forum/posts/{post_id}/comments", json=payload, headers={
                              "Cookie": f"access_token_cookie={cookie1}"})
    comment_id = _std(resp_create)["id"]
    resp_login2 = login_user(email="notauthorcomment@trucmuche.com")
    cookie2 = _extract_access_cookie(resp_login2)
    resp = client.put(f"/data/forum/comments/{comment_id}", json={
                      "content": "Fail"}, headers={"Cookie": f"access_token_cookie={cookie2}"})
    assert resp.status_code == 400

# --------------------------- DELETE ------------------------------------------


def test_delete_comment_success(login_user, client):
    post_id, cookie = _create_forum_post(
        client, login_user, email="commentdelete@trucmuche.com")
    payload = _comment_payload(content="A supprimer")
    resp_create = client.post(f"/data/forum/posts/{post_id}/comments", json=payload, headers={
                              "Cookie": f"access_token_cookie={cookie}"})
    comment_id = _std(resp_create)["id"]
    resp = client.delete(
        f"/data/forum/comments/{comment_id}", headers={"Cookie": f"access_token_cookie={cookie}"})
    assert resp.status_code == 200


def test_delete_comment_not_author(login_user, client):
    post_id, cookie1 = _create_forum_post(
        client, login_user, email="authorcomment2@trucmuche.com")
    payload = _comment_payload(content="Auteur2")
    resp_create = client.post(f"/data/forum/posts/{post_id}/comments", json=payload, headers={
                              "Cookie": f"access_token_cookie={cookie1}"})
    comment_id = _std(resp_create)["id"]
    resp_login2 = login_user(email="notauthorcomment2@trucmuche.com")
    cookie2 = _extract_access_cookie(resp_login2)
    resp = client.delete(
        f"/data/forum/comments/{comment_id}", headers={"Cookie": f"access_token_cookie={cookie2}"})
    assert resp.status_code == 400
