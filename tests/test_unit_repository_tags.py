import unittest
from unittest.mock import MagicMock, AsyncMock, Mock, patch

from sqlalchemy.orm import Session

from src.database.models import Note, User, Tag
from src.repository.tags import get_tag, get_tags, remove_tag, create_tag, update_tag
from src.schemas import TagModel


class TestTags(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.tags = [Tag(id=1, user_id=1), Tag(id=2, user_id=1)]
        self.user = User(id=1, username="test_user", password="qwerty", confirmed=True)
        self.session = MagicMock(spec=Session)

    async def test_get_tags(self):
        limit = 10
        offset = 0
        self.session.query().filter().offset().limit().all.return_value = self.tags
        result = await get_tags(offset, limit, self.user, self.session)
        self.assertEqual(result, self.tags)

    async def test_get_tag(self):
        tag = Tag(id=1, name="test_1")
        self.session.query().filter().first.return_value = tag
        result = await get_tag(1, self.user, self.session)
        self.assertEqual(result, tag)
        self.assertIsInstance(result, Tag)
        self.assertTrue(hasattr(result, "id"))

    async def test_create_tag(self):
        body = TagModel(name="test_new_tag")
        self.session.commit.return_value = None
        result = await create_tag(body=body, user=self.user, db=self.session)
        self.assertIsInstance(result, Tag)

    async def test_update_tag(self):
        body = TagModel(name="test_updated_new")
        tag = Tag()
        self.session.query().filter().first.return_value = tag
        result = await update_tag(tag_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, tag)
        self.assertEqual(result.name, body.name)
        self.assertTrue(hasattr(result, "id"))
        self.session.commit.assert_called_once()

    async def test_remove_tags(self):
        tag = Tag(id=1, name="test_tag")
        self.session.query().filter().first.return_value = tag
        result = await remove_tag(tag_id=1, user=self.user, db=self.session)
        self.assertEqual(result, tag)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Tag)
