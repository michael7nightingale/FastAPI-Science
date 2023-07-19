from fastapi import APIRouter, Depends, Form, Path, Request, Body
from fastapi.responses import FileResponse
from fastapi_authtools import login_required
from starlette.exceptions import HTTPException
import os

from app.formulas import contextBuilder, mathem_extra_counter
from app.formulas.plots import Plot
from app.models.schemas import RequestSchema
from app.formulas.metadata import get_formula
from app.db.repositories import (
    ScienceRepository,
    CategoryRepository,
    FormulaRepository,
    HistoryRepository,

)
from app.app.dependencies import (
    get_science_repository,
    get_category_repository,
    get_formula_repository,
    get_history_repository,

)


science_router = APIRouter(
    prefix='/science'
)
PLOTS_DIR = "/files/plots/"


# ================================= PLOTS ================================ #

async def plots_view(
        request: Request,
        category_slug: str,
        category_repo: CategoryRepository
):
    """Plot get endpoint."""
    category, science = await category_repo.get_with_science(category_slug)
    response = {
        "science": science,
        "category": category
    }
    plot_path = PLOTS_DIR + f'/{request.user.id}.png'
    full_plot_path = request.app.state.STATIC_DIR + plot_path
    if request.user is not None:
        if os.path.exists(full_plot_path):
            response.update(image_url=plot_path)
    return response


@login_required
async def plots_view_post(request: Request):
    """Plot file view"""
    data = await request.form()
    message = ""
    functions_list = [data[f"function{i}"] for i in range(1, 5) if data[f"function{i}"]]
    x_lim = data['xmin'], data['xmax']
    if all(x_lim) and functions_list:
        y_lim = data['ymin'], data['ymax']
        y_lim = y_lim if all(y_lim) else None
        try:
            plot = Plot(functions_list, x_lim, y_lim)
            plot_path = PLOTS_DIR + f'/{request.user.id}.png'
            full_plot_path = request.app.state.STATIC_DIR + plot_path
            plot.save_plot(full_plot_path)
        except (SyntaxError, NameError):
            message = "Невалидные данные."
        except TypeError:
            message = "Ожидаются рациональные числа."
        except ZeroDivisionError:
            message = "На ноль делить нет смысла."
        except ArithmeticError:
            message = "Вычислительно невозможное выражение"
        except ValueError as e:     # raises from Plot class
            message = str(e)
    else:
        message = "Неполные данные."
    if not message:
        return FileResponse(filename=f"{request.user.id}.png", path=full_plot_path)
    else:
        return {"detail": message}


# ======================================= EQUATIONS ===================================== #

async def equations_view(
        request: Request,
        category_slug: str,
        category_repo: CategoryRepository
):
    category, science = await category_repo.get_with_science(category_slug)
    return {
        "request": request,
        "science": science,
        "category": category
    }


async def equations_view_post(request: Request):
    form_data = await request.form()
    message = ""
    result = ""
    equations = list(filter(bool, form_data.values()))
    if len(equations) > 0:
        result = mathem_extra_counter.equation_system(equations)
    else:
        message = "Данные не предоставлены."
    if not message:
        return {"result": result}
    return {"detail": message}


SPECIAL_CATEGORIES_GET = {
    "plots": plots_view,
    "equations": equations_view
}

SPECIAL_CATEGORIES_POST = {
    "plots": plots_view_post,
    "equations": equations_view_post
}


@science_router.get('/science')
async def sciences_get(
        science_repo: ScienceRepository = Depends(get_science_repository),
):
    """All sciences list endpoint."""
    sciences = await science_repo.all()
    return sciences


@science_router.get('/science/{science_slug}')
async def science_get(
        science_repo: ScienceRepository = Depends(get_science_repository),
        science_slug: str = Path()
):
    """Science detail endpoint."""
    science, categories = await science_repo.get_with_categories(science_slug)
    return {
        "science": science,
        "categories": categories
    }


@science_router.get('/category/{category_slug}/')
async def category_get(
        request: Request,
        category_repo: CategoryRepository = Depends(get_category_repository),
        category_slug: str = Path(),
):
    """Category GET view."""
    if category_slug in SPECIAL_CATEGORIES_GET:
        return await SPECIAL_CATEGORIES_GET[category_slug](
            request,
            category_slug=category_slug,
            category_repo=category_repo
        )
    else:
        category, science, formulas = await category_repo.get_with_formulas_and_science(category_slug)
        return {
            "category": category,
            "science": science,
            "formulas": formulas
        }


@science_router.post('/category/{category_slug}/')
async def category_post(
        request: Request,
        category_slug: str = Path(),
        category_repo: CategoryRepository = Depends(get_category_repository)
):
    """Category POST view."""
    if category_slug in SPECIAL_CATEGORIES_POST:
        return await SPECIAL_CATEGORIES_GET[category_slug](
            request,
            category_slug=category_slug,
            category_repo=category_repo
        )
    else:
        raise HTTPException(status_code=404)


@science_router.get('/formula/{formula_slug}/')
async def formula_get(
        formula_repo: FormulaRepository = Depends(get_formula_repository),
        formula_slug: str = Path()
):
    """Science GET view."""
    formula, category = await formula_repo.get_with_category(formula_slug)
    formula_obj = get_formula(formula_slug)
    if formula_obj is not None:
        return {
            "formula": formula.as_dict(),
            "category": category.as_dict(),
            "info": formula_obj.as_dict()
        }


@science_router.post('/formula/{formula_slug}/')
@login_required
async def formula_post(
        request: Request,
        formula_slug: str = Path(),
        data: dict = Body(),
        nums_comma: int = Form(),
        formula_repo: FormulaRepository = Depends(get_formula_repository),
        history_repo: HistoryRepository = Depends(get_history_repository),
        find_mark: str = Form()
):
    """Request form to calculate."""
    formula, category = await formula_repo.get_with_category(formula_slug)
    request_schema = RequestSchema(
        formula_id=formula.id,
        url=request.url.path,
        method=request.method,
        find_mark=find_mark,
        user_id=request.user.id,
        data=data,
        nums_comma=nums_comma
    )
    result = await contextBuilder.count_result(
        request=request_schema,
        formula_slug=formula_slug,
        history_repo=history_repo
    )
    return result
