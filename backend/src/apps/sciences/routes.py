from fastapi import APIRouter, Path, Request, Body, Depends
from fastapi_authtools import login_required
from fastapi.responses import FileResponse, JSONResponse
from starlette.exceptions import HTTPException
import os

from .models import Science, Category, Formula
from ...services.formulas import contextBuilder, mathem_extra_counter
from src.services.formulas.plots import Plot
from .schemas import RequestSchema, RequestData, DownloadPlot, PlotData, EquationsData
from src.services.formulas.metadata import Formula as FormulaObject
from .dependencies import get_formula_mongo_repository


science_router = APIRouter(
    prefix='/sciences'
)
PLOTS_DIR = "files/plots/"


# ================================= PLOTS ================================ #

@science_router.get('/special-category/plots')
async def plots_view(request: Request):
    """Plot get endpoint."""
    category = await Category.get_or_none(slug="plots")
    response = {
        "science": category.science,
        "category": category
    }
    if request.user is not None:
        plot_path = PLOTS_DIR + f'/{request.user.id}.png'
        full_plot_path = request.app.state.STATIC_DIR + plot_path
        if os.path.exists(full_plot_path):
            response.update(plotPath=plot_path)
    return response


@science_router.post('/special-category/plots')
@login_required
async def plots_view_post(request: Request, data: PlotData = Body()):
    """Plot file view"""
    if data.functions:
        try:
            plot = Plot(data.functions, data.x_lim, data.y_lim)
            plot_path = PLOTS_DIR + f'{request.user.id}.png'
            full_plot_path = request.app.state.STATIC_DIR + plot_path
            print(full_plot_path)
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

@science_router.get('/special-category/equations')
async def equations_view(request: Request):
    """Equations get endpoint."""
    category = await Category.get_or_none(slug="equations")
    response = {
        "science": category.science,
        "category": category
    }
    return response


@science_router.post('/special-category/equations')
@login_required
async def equations_view_post(request: Request, data: EquationsData = Body()):
    message = result = ""
    if len(data.equations) > 0:
        result = mathem_extra_counter.equation_system(data.equations)
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
        formula_slug: str = Path(),
        formula_repository=Depends(get_formula_mongo_repository)
):
    """Science GET view."""
    formula = await Formula.get_or_none(slug=formula_slug)
    if formula is None:
        raise HTTPException(
            status_code=404,
            detail="Formula is not found."
        )
    formula_data = await formula_repository.get(slug=formula_slug)
    formula_obj = FormulaObject.from_dict(formula_data)
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
        formula_repository=Depends(get_formula_mongo_repository)
):
    """Request form to calculate."""
    formula = await Formula.get_or_none(slug=formula_slug)
    if formula is None:
        raise HTTPException(
            status_code=404,
            detail="Formula is not found."
        )
    formula_data = await formula_repository.get(slug=formula_slug)
    formula_obj = FormulaObject.from_dict(formula_data)
    request_schema = RequestSchema(
        formula_id=str(formula.id),
        url=request.url.path,
        method=request.method,
        user_id=request.user.id,
        **request_data.model_dump()
    )
    result = await contextBuilder.count_result(
        request=request_schema,
        formula_obj=formula_obj,
    )
    return {"result": result}
