from fastapi import status

from tests_api.conftest import get_main_url


class TestMain:
    async def test_main_url(self, client):
        response = await client.get(get_main_url("homepage"))
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"detail": "Application is started."}
