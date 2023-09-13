from fastapi import status
from httpx import AsyncClient

from src.apps.problems.models import Problem
from tests_api.conftest import get_problem_url


class TestProblems:

    async def test_problems_list_success(self, client_user1: AsyncClient, problems_test_data):
        problem1, *_ = problems_test_data
        resp = await client_user1.get(get_problem_url("problems_all"))
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 1
        problem = data[0]
        assert problem == {
            "id": problem1.id,
            "science_id": problem1.science_id,
            "user_id": problem1.user_id,
            "title": problem1.title,
            "time_opened": str(problem1.time_opened).replace(" ", "T"),
            "time_solved": str(problem1.time_opened).replace(" ", "T") if problem1.time_solved is not None else None,
            "text": problem1.text,
            'is_solved': problem1.is_solved,
        }

    async def test_problems_list_success_filter(self, client_user1: AsyncClient, problems_test_data):
        problem1, *_ = problems_test_data
        resp = await client_user1.get(get_problem_url("problems_all") + "?physics=on")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 1

    async def test_problems_list_success_filter_null(self, client_user1: AsyncClient, problems_test_data):
        problem1, *_ = problems_test_data
        resp = await client_user1.get(get_problem_url("problems_all") + "?mathem=on")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 0

    # async def test_problems_create(self, client_user1: AsyncClient, problem_create1_data):
    #     len_problems_before = await Problem.all().count()
    #     resp = await client_user1.post(
    #         get_problem_url("problem"),
    #         json=problem_create1_data,
    #     )
    #     assert resp.status_code == status.HTTP_201_CREATED
    #     data = resp.json()
    #     assert 'title' in data
    #     problems_after = await Problem.all()
    #     assert len(problems_after) - len_problems_before == 1

    async def test_problem_delete_success(self, client_user1, problem1_user1):
        len_problems_before = await Problem.all().count()
        resp = await client_user1.delete(get_problem_url("problem", problem_id=problem1_user1.id))
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert data == {"detail": "Problem deleted successfully."}
        problems_after = await Problem.all()
        assert len(problems_after) - len_problems_before == -1

    async def test_problem_delete_fail_unauthorized(self, client_user2, problem1_user1):
        len_problems_before = await Problem.all().count()
        resp = await client_user2.delete(get_problem_url("problem", problem_id=problem1_user1.id))
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        data = resp.json()
        assert data == {"detail": "You don`t have permissions."}
        problems_after = await Problem.all()
        assert len(problems_after) == len_problems_before

    async def test_problem_delete_fail_not_found(self, client_user2, problem1_user1):
        len_problems_before = await Problem.all().count()
        resp = await client_user2.delete(get_problem_url("problem", problem_id="90s91db7-18f6-44b1-9ca6-356cf825af83"))
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        data = resp.json()
        assert data == {"detail": "Problem is not found."}
        problems_after = await Problem.all()
        assert len(problems_after) == len_problems_before

    async def test_problem_update_success(self, client_user1, problem1_user1):
        update_data = {
            "title": "Problem of mathematics 1"
        }
        resp = await client_user1.patch(
            get_problem_url("problem", problem_id=problem1_user1.id),
            json=update_data
        )
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert data == {"detail": "Problem updated successfully."}
        await problem1_user1.refresh_from_db()
        assert problem1_user1.title == update_data['title']

    async def test_problem_update_fail_unauthorized(self, client_user2, problem1_user1):
        update_data = {
            "title": "Problem of mathematics 1"
        }
        len_problems_before = await Problem.all().count()
        resp = await client_user2.patch(
            get_problem_url("problem", problem_id=problem1_user1.id),
            json=update_data
        )
        data = resp.json()
        assert data == {"detail": "You don`t have permissions."}
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        problems_after = await Problem.all()
        assert len(problems_after) == len_problems_before

    async def test_problem_update_fail_not_found(self, client_user2, problem1_user1):
        update_data = {
            "title": "Problem of mathematics 1"
        }
        len_problems_before = await Problem.all().count()

        resp = await client_user2.patch(
            get_problem_url("problem", problem_id="90s91db7-18f6-44b1-9ca6-356cf825af83"),
            data=update_data
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        data = resp.json()
        assert data == {"detail": "Problem is not found."}
        problems_after = await Problem.all()
        assert len(problems_after) == len_problems_before
