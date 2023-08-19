from fastapi import status

from tests_api.conftest import get_science_url


class TestScience:

    async def test_science_all(self, client):
        response = await client.get(get_science_url('sciences_all'))
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        physics, mathem = data if data[0]['slug'] == 'physics' else data[::-1]
        assert physics['title'] == "Физика"
        assert physics['slug'] == "physics"
        assert mathem['title'] == "Математика"
        assert mathem['slug'] == "mathem"

    async def test_science_detail(self, client, physics):
        response = await client.get(get_science_url("science_get", science_slug="physics"))
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'science' in data
        science_data = data['science']
        assert science_data['title'] == physics.title
        assert science_data['slug'] == physics.slug
        assert science_data['content'] == physics.content
        assert science_data['image_path'] == physics.image_path
        assert "categories" in data and "id" in science_data
        assert len(data['categories'])
        assert any(1 for i in data['categories'] if i['title'] == "Динамика")

    async def test_science_detail_not_found(self, client_user2):
        response = await client_user2.get(get_science_url("science_get", science_slug="bio"))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Science is not found."}
