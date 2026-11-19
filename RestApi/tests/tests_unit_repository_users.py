import unittest
from unittest.mock import AsyncMock, patch, MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact,User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    get_user_by_username,
    create_user,
    update_token,
    confirmed_email,
    update_avatar
)

class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_email_found(self):
        user=User()
        self.session.query().filter().first.return_value=user
        result= await get_user_by_email(email="test@gmail.com", db=self.session)
        self.assertEqual(result,user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value=None
        result= await get_user_by_email(email="test@gmail.com", db=self.session)
        self.assertIsNone(result)

    async def test_get_user_by_username_found(self):
        user=User()
        self.session.query().filter().first.return_value=user
        result= await get_user_by_username(username="test", db=self.session)
        self.assertEqual(result,user)

    async def test_get_user_by_username_not_found(self):
        self.session.query().filter().first.return_value=None
        result= await get_user_by_username(username="test", db=self.session)
        self.assertIsNone(result)

    async def test_creae_uesr(self):
        body=UserModel(username="test123",email="test@gmail.com", password="passs123")
        result = await create_user(body, self.session)
        user=User()
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        
    async def test_update_token(self):
        user=User()
        result = await update_token(user=user, token="new_token", db=self.session)
        self.assertIsNone(result)

    @patch("src.repository.users.get_user_by_email", new_callable=AsyncMock)
    async def test_confirmed_email(self, mock_get_user):
        user=User(confirmed=False)
        mock_get_user.return_value = user
        email = "test@example.com"
        result = await confirmed_email(email=email, db=self.session)
        self.assertTrue(user)
        self.assertIsNone(result)   

    @patch("src.repository.users.get_user_by_email", new_callable=AsyncMock)
    async def test_update_avatar(self, mock_get_user):
        user=User(avatar=None)
        mock_get_user.return_value = user
        email = "test@example.com"
        url="url"
        result = await update_avatar(email=email,url=url, db=self.session)
        self.assertEqual(result, user)
        self.assertEqual(url, user.avatar)


if __name__ == '__main__':
    unittest.main()
