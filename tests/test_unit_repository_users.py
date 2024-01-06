import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from src.database.models import Note, User, Tag
from src.repository.users import get_user_by_email, create_user, update_token, confirmed_email, update_avatar
from src.schemas import TagModel, UserModel


class TestTags(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User(id=1, email="person2024.ua", username="test_user", password="qwerty", confirmed=True)
        self.session = MagicMock(spec=Session)

    async def test_user_by_email(self):
        email="person2024.ua"
        self.session.query().filter().first.return_value = self.user
        result = await get_user_by_email(email, self.session)
        self.assertEqual(result, self.user)
        self.assertEqual(result.email, self.user.email)

    async def test_create_user(self):
        body = UserModel(username="Dmitro", email="example.com.ua", password="qwerty1234")
        result = await create_user(body, self.session)
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, User)
        self.assertTrue(hasattr(result, "id"))
        self.assertEqual(result.username,body.username)

    async def test_update_token(self):
        token = "secret_hash"
        result = await update_token(self.user, token, self.session)
        self.session.commit.assert_called_once()
        self.assertEqual(self.user.refresh_token, token)

    async def test_confirmed_email(self):
        email = "person2024.ua"
        with patch('src.repository.users.get_user_by_email') as mock:
            mock.return_value = self.user
            await confirmed_email(email, self.session)
            self.session.commit.assert_called_once()
            self.assertTrue(self.user.confirmed)
            self.assertEqual(self.user.email, email)

    async def test_update_avatar(self):
        url = "https://images.unsplash.com/photo-1575936123452-b67c3203c357?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aW1hZ2V8ZW58MHx8MHx8fDA%3D"
        with patch('src.repository.users.get_user_by_email') as mock:
            mock.return_value = self.user
            await update_avatar(self.user.email, url, self.session)
            self.session.commit.assert_called_once()
            self.assertEqual(self.user.avatar, url)


