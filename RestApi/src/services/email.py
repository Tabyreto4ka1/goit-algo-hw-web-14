from pathlib import Path

from sqlalchemy.orm import Session

from fastapi import HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr
from  src.conf.config import settings
from src.services.auth import auth_service
from src.repository.users import get_user_by_email

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)



async def send_email(email: EmailStr, username: str, host: str, db: Session):
    """
    Send email to a specific user
    :param email: The email of the user whose need to received email
    :type email: EmailStr
    :param username: The username of user
    :type username: str
    :param host: The host used to generate the email link
    :type host: str
    :param db: The database session
    :type db: Session
    :return:None
    :rtype:None

    """
    user=await get_user_by_email(email,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email.html")
    except ConnectionErrors as err:
        print(err)

