from fastapi import status
from httpx import AsyncClient

from src.services.token import generate_token
from tests_api.conftest import get_auth_url


class TestMain:
    async def test_token_bad_request(self, client: AsyncClient):
        user_nonexisted_data = {
            "password": "user1['password']",
            "username": "user1['username']"
        }
        response = await client.post(
            get_auth_url("get_token"),
            json=user_nonexisted_data
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Invalid credentials provided."}

    async def test_token_success(self, client: AsyncClient, users_test_data, user1):
        user_existed_data = {
            ""
            "password": user1['password'],
            "username": user1['username']
        }
        response = await client.post(
            get_auth_url("get_token"),
            json=user_existed_data
        )
        assert response.status_code == status.HTTP_200_OK

    # async def test_register_success(self, client: AsyncClient, user1: dict):
    #     response = await client.post(
    #         get_auth_url("register"),
    #         json=user1
    #     )
    #     assert response.status_code == status.HTTP_200_OK
    #     data = response.json()
    #     assert data['username'] == user1['username']
    #     assert data['email'] == user1['email']

    async def test_register_failed(self, client: AsyncClient):
        user_data = {
            "username": "asdoaisjfkljans",
            "password": "a0sdjkabkhf1",
        }
        response = await client.post(
            get_auth_url("register"),
            json=user_data
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_register_not_active(self, client: AsyncClient):
        user = {
            "username": "username",
            "email": "email@gmail.com",
            "password": "password"
        }
        response = await client.post(
            get_auth_url("register"),
            json=user
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "detail": f"Activation link is sent on email {user['email']}. Please follow the instructions."
        }
        user_existed_data = {
            "password": user['password'],
            "username": user['username']
        }
        response = await client.post(
            get_auth_url("get_token"),
            json=user_existed_data
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Invalid credentials provided."}

    async def test_me_success(self, client_user2: AsyncClient, user2: dict):
        response = await client_user2.get(get_auth_url("me"))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == user2['username']
        assert response.json()["email"] == user2['email']
        assert response.json()["is_active"]
        assert response.json()["is_authenticated"]
        assert "id" in response.json()

    async def test_activation_success(self, client: AsyncClient, not_active_user, user_not_activated: dict):
        assert not not_active_user.is_active
        activation_link = get_auth_url(
            "activate_user",
            uuid=not_active_user.id,
            token=generate_token(not_active_user.email)
        )
        response = await client.get(activation_link)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"detail": "User is activated successfully."}
        response = await client.post(
            get_auth_url("get_token"),
            json={
                "username": user_not_activated['username'],
                "password": user_not_activated["password"]
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()

    async def test_activation_failed(self, client: AsyncClient, not_active_user, user_not_activated: dict):
        assert not not_active_user.is_active
        activation_link = get_auth_url(
            "activate_user",
            uuid="0000-0000-0000-0000",
            token=generate_token(not_active_user.email)
        )
        response = await client.get(activation_link)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Activation link is invalid."}
