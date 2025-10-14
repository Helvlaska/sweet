import pytest
from app.models.forum_post import ForumPost

SKIP_REASON = "Routes forum non implémentées (app/routes/forum.py vide) — tests en attente d'implémentation des endpoints."


@pytest.mark.skip(reason=SKIP_REASON)
def test_create_forum_post_success():
	pass

@pytest.mark.skip(reason=SKIP_REASON)
def test_read_forum_post_success():
	pass

@pytest.mark.skip(reason=SKIP_REASON)
def test_update_forum_post_success():
	pass

@pytest.mark.skip(reason=SKIP_REASON)
def test_delete_forum_post_success():
	pass

@pytest.mark.skip(reason=SKIP_REASON)
def test_create_forum_post_missing_fields():
	pass

@pytest.mark.skip(reason=SKIP_REASON)
def test_read_forum_post_not_found():
	pass

@pytest.mark.skip(reason=SKIP_REASON)
def test_update_forum_post_unauthorized():
	pass

@pytest.mark.skip(reason=SKIP_REASON)
def test_delete_forum_post_unauthorized():
	pass

@pytest.mark.skip(reason=SKIP_REASON)
def test_jwt_token_missing():
	pass

@pytest.mark.skip(reason=SKIP_REASON)
def test_jwt_token_invalid():
	pass

@pytest.mark.skip(reason=SKIP_REASON)
def test_role_admin_access():
	pass

@pytest.mark.skip(reason=SKIP_REASON)
def test_role_user_access():
	pass

