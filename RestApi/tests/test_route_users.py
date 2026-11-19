from io import BytesIO
from unittest.mock import MagicMock

from src.services.auth import auth_service
from src.routes.users import repository_users
from main import app


def test_read_users_me(client, user):
    async def mock_get_current_user():
        return user

    app.dependency_overrides[auth_service.get_current_user] = mock_get_current_user
    response = client.get("/api/users/me/")
    assert response.status_code == 200
    app.dependency_overrides.clear()


def test_update_avatar_user(client, user, monkeypatch):
    async def mock_get_current_user():
        return user

    async def mock_update_avatar(email, avatar_url, db):
        return user

    app.dependency_overrides[auth_service.get_current_user] = mock_get_current_user
    monkeypatch.setattr(
        "src.routes.users.repository_users.update_avatar",
        mock_update_avatar
    )

    monkeypatch.setattr(
        "src.routes.users.cloudinary.uploader.upload",
        MagicMock(return_value={"version": "123"})
    )
    mock_image = MagicMock()
    mock_image.build_url.return_value = "https://example.com/avatar.jpg"
    monkeypatch.setattr(
        "src.routes.users.cloudinary.CloudinaryImage",
        MagicMock(return_value=mock_image)
    )
    response = client.patch(
        "/api/users/avatar",
        files={
            "file": (
                "avatar.jpg",
                BytesIO(b"test image"),
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 200

