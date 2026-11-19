
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieve a user by their email address.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user associated with the specified email address.
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


async def get_user_by_username(username: str, db: Session) -> User:
    """
    Retrieve a user by their username.

    :param username: The username of the user to retrieve.
    :type username: str
    :param db: The database session.
    :type db: Session
    :return: The user associated with the specified username.
    :rtype: User
    """
    return db.query(User).filter(User.username == username).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Create a new user in the database.

    :param body: The data used to create the user.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: User
    """
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Update the refresh token of a specific user.

    :param user: The user whose refresh token should be updated.
    :type user: User
    :param token: The new refresh token, or None to clear the existing token.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    :return: None.
    :rtype: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirm a user's email address.

    :param email: The email address of the user whose email should be confirmed.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: None.
    :rtype: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Update the avatar URL of a specific user.

    :param email: The email address of the user whose avatar should be updated.
    :type email: str
    :param url: The new avatar URL.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The user with the updated avatar URL.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
