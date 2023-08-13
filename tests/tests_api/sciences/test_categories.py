from fastapi import status

from tests_api.conftest import get_science_url


class TestCategory:

    async def test_category_detail(self, client):
        response = await client.get(get_science_url("category_get", category_slug="dinamika"))
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "category" in data and "formulas" in data
        assert data['category']['title'] == "Динамика"

    async def test_category_not_found(self, client):
        response = await client.get(get_science_url("category_get", category_slug="python_and_js"))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Category is not found."}
