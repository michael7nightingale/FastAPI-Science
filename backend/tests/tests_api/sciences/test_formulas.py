from fastapi import status

from tests_api.conftest import get_science_url


class TestFormula:

    async def test_formula_detail_get(self, client):
        response = await client.get(get_science_url("formula_get", formula_slug="newton2"))
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "category" in data and "formula" in data and "info" in data
        assert data['category']['title'] == "Динамика"
        assert data['formula']['title'] == "Второй закон Ньютона"
        info = data['info']
        assert info == {
            "formula": "F = m * a",
            "args": ["F", "m", "a"],
            'literals': [
                {
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
                {
                    'ed': 'kg',
                    'is_constant': False,
                    'is_function': False,
                    'literal': 'm',
                    'name': 'Mass',
                    'si': {
                        'g': 0.001,
                        'kg': 1
                    },
                    'value': None
                },
                {
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
            ]
        }

    async def test_formula_detail_not_found(self, client):
        response = await client.get(get_science_url("formula_get", formula_slug="oop"))
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
            get_science_url("formula_post", formula_slug="newton2"),
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
            "numsComma": 2,
            "findMark": "F"
        }
        response = await client_user1.post(
            get_science_url("formula_post", formula_slug="newton2"),
            json=data
        )
        print(123123, response.json())
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
            "numsComma": 2,
            "findMark": "m"
        }
        response = await client_user1.post(
            get_science_url("formula_post", formula_slug="newton2"),
            json=data
        )
        assert response.status_code == status.HTTP_200_OK
        assert "result" in response.json()
        assert response.json()['result'] == 1.23
