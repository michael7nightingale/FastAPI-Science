import json

from fastapi import status

from .conftest import get_science_router


class TestScience:

    async def test_science_all(self, client):
        response = await client.get(get_science_router('sciences_all'))
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        physics, mathem = data if data[0]['slug'] == 'physics' else data[::-1]
        assert physics['title'] == "Физика"
        assert physics['slug'] == "physics"
        assert mathem['title'] == "Математика"
        assert mathem['slug'] == "mathem"

    async def test_science_detail(self, client):
        response = await client.get(get_science_router("science_get", science_slug="physics"))
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "categories" in data and "science" in data
        assert len(data['categories'])
        assert any(1 for i in data['categories'] if i['title'] == "Динамика")

    async def test_science_detail_not_found(self, client_user2):
        response = await client_user2.get(get_science_router("science_get", science_slug="bio"))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Science is not found."}


class TestCategory:

    async def test_category_detail(self, client):
        response = await client.get(get_science_router("category_get", category_slug="dinamika"))
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "category" in data and "formulas" in data
        assert data['category']['title'] == "Динамика"

    async def test_category_not_found(self, client):
        response = await client.get(get_science_router("category_get", category_slug="python_and_js"))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Category is not found."}


class TestFormula:

    async def test_formula_detail_get(self, client):
        response = await client.get(get_science_router("formula_get", formula_slug="newton2"))
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "category" in data and "formula" in data and "info" in data
        assert data['category']['title'] == "Динамика"
        assert data['formula']['title'] == "Второй закон Ньютона"
        info = data['info']
        assert info == {
            "formula": "F = m * a",
            "args": ["F", "m", "a"],
            'literals': {
                'F': {
                    'ed': 'N',
                    'is_constant': False,
                    'is_function': False,
                    'literal': 'F',
                    'name': 'Force',
                    'si': {
                        'N': 1,
                        'kN': 1000,
                        'mN': 0.001
                    },
                    'value': None
                },
                'a': {
                    'ed': 'm/s^2',
                    'is_constant': False,
                    'is_function': False,
                    'literal': 'a',
                    'name': 'Acceleration',
                    'si': {
                        'km/s^2': 1000,
                        'm/s^2': 1
                    },
                    'value': None
                },
                'm': {
                    'ed': 'kg',
                    'is_constant': False,
                    'is_function': False,
                    'literal': 'm',
                    'name': 'Mass',
                    'si': {
                        'g': 0.001,
                        'kg': 1
                    },
                    'value': None}
            },
        }

    async def test_formula_detail_not_found(self, client):
        response = await client.get(get_science_router("formula_get", formula_slug="oop"))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Formula is not found."}

    async def test_formula_count_unauthorized(self, client):
        data = {
            "data": {
                "F": {}
            },
            "nums_comma": '2',
            "find_mark": "F"
        }
        response = await client.post(
            get_science_router("formula_post", formula_slug="newton2"),
            json=data
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_formula_count_success_default(self, client_user1):
        data = {
            "data": {
                "m": '123',
                "msi": "kg",
                "a": '100',
                "asi": "m/s^2"
            },
            "nums_comma": 2,
            "find_mark": "F"
        }
        response = await client_user1.post(
            get_science_router("formula_post", formula_slug="newton2"),
            json=data
        )
        assert response.status_code == status.HTTP_200_OK
        assert "result" in response.json()
        assert response.json()['result'] == 12300

    async def test_formula_count_success_find_mark_non_default(self, client_user1):
        data = {
            "data": {
                "F": '123',
                "Fsi": "H",
                "a": '100',
                "asi": "m/s^2"
            },
            "nums_comma": 2,
            "find_mark": "m"
        }
        response = await client_user1.post(
            get_science_router("formula_post", formula_slug="newton2"),
            json=data
        )
        assert response.status_code == status.HTTP_200_OK
        assert "result" in response.json()
        assert response.json()['result'] == 1.23
