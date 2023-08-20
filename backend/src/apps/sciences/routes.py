from fastapi import APIRouter, Path, Request, Body
from fastapi_authtools import login_required
from fastapi.responses import FileResponse, JSONResponse
from starlette.exceptions import HTTPException
import os

from .models import Science, Category, Formula
from ...services.formulas import contextBuilder, mathem_extra_counter
from src.services.formulas.plots import Plot
from .schemas import RequestSchema, RequestData, DownloadPlot
from src.services.formulas.metadata import get_formula


science_router = APIRouter(
    prefix='/sciences'
)
PLOTS_DIR = "/files/plots/"


# ================================= PLOTS ================================ #

@science_router.get('/special-category/plots')
async def plots_view(request: Request):
    """Plot get endpoint."""
    category = await Category.get_or_none(slug="plots")
    response = {
        "science": category.science,
        "category": category
    }
    plot_path = PLOTS_DIR + f'/{request.user.id}.png'
    full_plot_path = request.app.state.STATIC_DIR + plot_path
    if request.user is not None:
        if os.path.exists(full_plot_path):
            response.update(plotPath=plot_path)
    return response


@science_router.post('/special-category/plots')
@login_required
async def plots_view_post(request: Request, data: dict = Body()):
    """Plot file view"""
    functions_list = [data.get(f"function{i}") for i in range(1, 5) if data.get(f"function{i}") is not None]
    x_lim = data['xMin'], data['xMax']
    if all(x_lim) and functions_list:
        y_lim = data['yMin'], data['yMax']
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
            return {"plotPath": plot_path}
    else:
        message = "Неполные данные."
    return {"detail": message}


@science_router.post('/special-category/plots/download')
@login_required
async def plots_view_post(request: Request, filedata: DownloadPlot = Body()):
    """Plot file download view"""
    plot_path = PLOTS_DIR + f'/{request.user.id}.png'
    full_plot_path = request.app.state.STATIC_DIR + plot_path
    if os.path.exists(full_plot_path):
        return FileResponse(path=full_plot_path, filename=filedata.filename + ".png")
    else:
        return JSONResponse(
            {"detail": "Missing any plots."},
            status_code=404
        )


# ======================================= EQUATIONS ===================================== #

@science_router.post('/special-category/equations')
async def equations_view(request: Request):
    category = await Category.get_or_none(slug="equations")
    return {
        "request": request,
        "sciences": category.science,
        "category": category
    }


@science_router.post('/special-category/equations')
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


@science_router.get('/')
async def sciences_all():
    """All sciences list endpoint."""
    sciences = await Science.all()
    return sciences


@science_router.get('/science/{science_slug}')
async def science_get(
        science_slug: str = Path()
):
    """Science detail endpoint."""
    science = await Science.get_or_none(slug=science_slug)
    if science is None:
        raise HTTPException(
            status_code=404,
            detail="Science is not found."
        )
    return {
        "science": science.as_dict(),
        "categories": [i.as_dict() for i in science.categories]
    }


@science_router.get('/category/{category_slug}')
async def category_get(
        request: Request,
        category_slug: str = Path(),
):
    """Category GET view."""
    category = await Category.get_or_none(slug=category_slug)
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category is not found."
        )
    return {
        "category": category.as_dict(),
        "science": category.science.as_dict(),
        "formulas": [f.as_dict() for f in category.formulas]
    }


@science_router.get('/formula/{formula_slug}')
async def formula_get(
        formula_slug: str = Path()
):
    """Science GET view."""
    formula = await Formula.get_or_none(slug=formula_slug)
    if formula is None:
        raise HTTPException(
            status_code=404,
            detail="Formula is not found."
        )
    formula_obj = get_formula(formula_slug)
    if formula_obj is not None:
        return {
            "formula": formula.as_dict(),
            "category": formula.category.as_dict(),
            "info": formula_obj.as_dict()
        }


@science_router.post('/formula/{formula_slug}')
@login_required
async def formula_post(
        request: Request,
        formula_slug: str = Path(),
        request_data: RequestData = Body(),
):
    """Request form to calculate."""
    formula = await Formula.get_or_none(slug=formula_slug)
    if formula is None:
        raise HTTPException(
            status_code=404,
            detail="Formula is not found."
        )
    request_schema = RequestSchema(
        formula_id=str(formula.id),
        url=request.url.path,
        method=request.method,
        user_id=request.user.id,
        **request_data.model_dump()
    )
    result = await contextBuilder.count_result(
        request=request_schema,
        formula_slug=formula_slug,
    )
    return {"result": result}
