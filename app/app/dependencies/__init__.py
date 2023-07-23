from fastapi_authtools.exceptions import raise_permissions_error

from .database import get_repository, get_socket_repository
from .auth import get_user_register_data
from .sciences import get_all_sciences
from .repository import (
    get_history_repository,
    get_user_repository,
    get_science_repository,
    get_formula_repository,
    get_category_repository,
    get_problem_repository,
    get_solution_repository,
    get_problem_media_repository,
    get_solution_media_repository,

)
from .cabinets import get_table_filepath
from .problems import (
    get_problem,
    get_solution,
    get_problem_data,
    get_solution_data,
    get_solution_media,
    get_problem_media,

)


def check_object_permissions(obj, user, field_name):
    if getattr(obj, field_name) != user.id:
        raise_permissions_error()
