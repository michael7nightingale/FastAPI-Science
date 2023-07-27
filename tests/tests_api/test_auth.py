from fastapi import status
from httpx import AsyncClient

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

    async def test_register_success(self, client: AsyncClient, user1: dict):
        response = await client.post(
            get_auth_url("register"),
            json=user1
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['username'] == user1['username']
        assert data['email'] == user1['email']

    async def test_register_filed(self, client: AsyncClient):
        user_data = {
            "username": "asdoaisjfkljans",
            "password": "a0sdjkabkhf1",
        }
        response = await client.post(
            get_auth_url("register"),
            json=user_data
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # async def test_register_not_active(self, client: AsyncClient, user1):
    #     response = await client.post(
    #         get_auth_url("register"),
    #         json=user1
    #     )
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.json() == f"Activation link is send on email {user1['email']}"
    #     user_existed_data = {
    #         "password": user1['password'],
    #         "username": user1['username']
    #     }
    #     response = await client.post(
    #         get_auth_url("get_token"),
    #         json=user_existed_data
    #     )
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert response.json() == {"detail": "Invalid credentials provided."}

    async def test_me_success(self, client_user2: AsyncClient, user2: dict):
        response = await client_user2.get(get_auth_url("me"))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == user2['username']
        assert response.json()["email"] == user2['email']
        assert response.json()["is_active"]
        assert response.json()["is_authenticated"]
        assert "id" in response.json()
