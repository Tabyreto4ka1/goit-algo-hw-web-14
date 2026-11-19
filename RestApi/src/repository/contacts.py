from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
import datetime

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate, ContactSearch


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieve contacts belonging to a specific user.

    :param skip: The number of contacts to skip.
    :param limit: The maximum number of contacts to retrieve.    :type skip: int

    :type limit: int
    :param user: The user whose contacts are to be retrieved.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts belonging to the user.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(id: int, user: User, db: Session) -> Contact:
    """
    Retrieve a contact belonging to a specific user by its ID.

    :param id: The ID of the contact to retrieve.
    :type id: int
    :param user: The user who owns the contact.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The requested contact.
    :rtype: Contact
    """
    return db.query(Contact).filter(Contact.id == id).filter(Contact.user_id == user.id).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Create a new contact associated with a specific user.

    :param body: The data used to create the contact.
    :type body: ContactModel
    :param user: The user who creates the contact.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(
        name=body.name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        additional=body.additional,
        user=user
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    """
    Update a specific contact belonging to a user.

    :param id: The ID of the contact to update.
    :type id: int
    :param body: The data used to update the contact.
    :type body: ContactUpdate
    :param user: The user who owns the contact.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if the contact is not found.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(Contact.id == id).filter(Contact.user_id == user.id).first()
    if contact:
        contact.name = body.name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional = body.additional
        db.commit()
    return contact


async def remove_contact(id: int, user: User, db: Session) -> Contact | None:
    """
    Delete a contact belonging to a specific user.

    :param id: The ID of the contact to delete.
    :type id: int
    :param user: The user who owns the contact.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The deleted contact, or None if the contact is not found.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(Contact.id == id).filter(Contact.user_id == user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def birthday_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieve contacts whose birthdays fall within the next seven days.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to retrieve.
    :type limit: int
    :param user: The user whose contacts are to be retrieved.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts whose birthdays fall within the next seven days.
    :rtype: List[Contact]
    """
    contacts = []
    today = datetime.datetime.now(datetime.timezone.utc).date()
    for i in range(0, 8):
        date = today + datetime.timedelta(days=i)
        date_str = date.strftime("%m-%d")
        contacts.extend(
            db.query(Contact)
            .filter(func.to_char(Contact.birthday, "MM-DD") == date_str)
            .filter(Contact.user_id == user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    return contacts


async def search_contact(body: ContactSearch, user: User, db: Session) -> List[Contact]:
    """
    Retrieve contacts matching the specified search criteria.

    :param body: The criteria used to search for contacts.
    :type body: ContactSearch
    :param user: The user who owns the contacts.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts matching the search criteria.
    :rtype: List[Contact]
    """
    query = db.query(Contact)
    query = query.filter(Contact.user_id == user.id)
    if body.name:
        query = query.filter(Contact.name == body.name)
    if body.last_name:
        query = query.filter(Contact.last_name == body.last_name)
    if body.email:
        query = query.filter(Contact.email == body.email)
    return query.all()
