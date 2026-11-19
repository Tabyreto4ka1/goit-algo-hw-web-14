import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact,User
from src.schemas import ContactModel, ContactUpdate, ContactSearch
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    birthday_contacts,
    search_contact
)


class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact=Contact(id=1)

    async def test_get_contacts(self):
        contacts=[Contact(),Contact(),Contact()]
        self.session.query().filter().offset().limit().all.return_value=contacts
        result= await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact=Contact()
        self.session.query().filter().filter().first.return_value = contact
        result=await get_contact(id=self.contact.id, user=self.user, db= self.session)
        self.assertEqual(result, contact)


    async def test_get_note_not_found(self):
        self.session.query().filter().filter().first.return_value = None
        result=await get_contact(id=self.contact.id, user=self.user, db= self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body=ContactModel(name="test",last_name="test",email="test@gmail.com",
                        phone_number="+3800000000",birthday="2026-11-19T10:37:13.932Z",additional="test")
        result=await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.additional, body.additional)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact=Contact()
        self.session.query().filter().filter().first.return_value=contact
        result= await remove_contact(id=self.contact.id, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().filter().first.return_value=None
        result= await remove_contact(id=self.contact.id, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body=ContactUpdate(name="test",last_name="test",email="test@gmail.com",
                                phone_number="+3800000000",birthday="2026-11-19T10:37:13.932Z",additional="test")
        contact=Contact()
        self.session.query().filter().filter().first.return_value=contact
        self.session.commit.return_value=None
        result=await update_contact(id=self.contact.id,body=body, user=self.user, db=self.session )
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body=ContactUpdate(name="test",last_name="test",email="test@gmail.com",
                                phone_number="+3800000000",birthday="2026-11-19T10:37:13.932Z",additional="test")
        self.session.query().filter().filter().first.return_value=None
        self.session.commit.return_value=None

    async def test_birthday_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().offset().limit().all.side_effect = [
            contacts, [], [], [], [], [], [], []
        ]
        self.session.reset_mock()
        result = await birthday_contacts(skip=0,limit=10,user=self.user,db=self.session)
        self.assertEqual(result, contacts)
        self.assertEqual(self.session.query.call_count, 8)

    async def test_search_contact_found(self):
        body = ContactSearch(
            name="test",
            last_name="test",
            email="test@gmail.com"
        )

        contact = Contact()
        expected = [contact]

        query = self.session.query.return_value
        query.filter.return_value = query
        query.all.return_value = expected

        result = await search_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

