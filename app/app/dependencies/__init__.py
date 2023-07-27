from fastapi_authtools.exceptions import raise_permissions_error

from .database import get_repository, get_socket_repository
from .auth import get_user_register_data
from .sciences import get_all_sciences
from .cabinets import get_table_filepath
from .problems import (
    get_problem,
    get_solution,
    get_problem_data,
    get_solution_data,
    get_solution_media,
    get_problem_media,

)
from .services import (
    get_history_service,
    get_user_service,
    get_science_service,
    get_formula_service,
    get_category_service,
    get_problem_service,
    get_solution_service,
    get_problem_media_service,
    get_solution_media_service,

)


def check_object_permissions(obj, user, field_name):
    if getattr(obj, field_name) != user.id:
        raise_permissions_error()
