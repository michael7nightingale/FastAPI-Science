from fastapi import APIRouter, Request, Body, Depends
from fastapi.responses import FileResponse, JSONResponse
import os

from .models import Science, Category, Formula
from ..cabinets.models import History
from ..users.permissions import login_required
from ...services.formulas import counter, mathem_extra_counter
from src.services.formulas.plots import Plot
from .schemas import RequestSchema, RequestData, DownloadPlot, PlotData, EquationsData, \
    ScienceDetailSchema, CategoryDetailSchema, ScienceListSchema, FormulaDetailSchema
from src.services.formulas.metadata import Formula as FormulaObject
from .dependencies import get_formula_dependency, get_science_dependency, \
    get_category_dependency

router = APIRouter(prefix='/sciences', tags=['Sciences'])
PLOTS_DIR = "files/plots/"


# ================================= PLOTS ================================ #

@router.get('/special-category/plots')
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


@router.post('/special-category/plots')
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
        except ValueError as e:  # raises from Plot class
            message = str(e)
        else:
            return {"plotPath": plot_path}
    else:
        message = "Неполные данные."
    return {"detail": message}


@router.post('/special-category/plots/download')
@login_required
async def plots_view_download(request: Request, filedata: DownloadPlot = Body()):
    """Plot file download view"""
    plot_path = PLOTS_DIR + f'/{request.user.id}.png'
    full_plot_path = request.app.state.STATIC_DIR + plot_path
    if os.path.exists(full_plot_path):
        return FileResponse(path=full_plot_path, filename=filedata.filename + ".png")
    else:
        return JSONResponse({"detail": "Missing any plots."}, 404)


# ======================================= EQUATIONS ===================================== #

@router.get('/special-category/equations')
async def equations_view(request: Request):
    """Equations get endpoint."""
    category = await Category.get_or_none(slug="equations")
    response = {
        "science": category.science,
        "category": category
    }
    return response


@router.post('/special-category/equations')
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


@router.get('/', response_model=list[ScienceListSchema])
async def sciences_list_view():
    """All sciences list endpoint."""
    sciences = await Science.all()
    return sciences


@router.get('/science/{science_slug}', response_model=ScienceDetailSchema)
async def science_detail_view(science: Science = Depends(get_science_dependency)):
    """Science detail endpoint."""
    return {
        **science.as_dict(),
        "categories": (i.as_dict() for i in science.categories)
    }


@router.get('/category/{category_slug}', response_model=CategoryDetailSchema)
async def category_detail_view(
        request: Request,
        category: Category = Depends(get_category_dependency),
):
    """Category GET view."""
    return {
        **category.as_dict(),
        "science": category.science.as_dict(),
        "formulas": [f.as_dict() for f in category.formulas]
    }


@router.get('/formula/{formula_slug}', response_model=FormulaDetailSchema)
async def formula_detail_view(
        formula: Formula = Depends(get_formula_dependency),
        # formula_repository: FormulaRepository = Depends(get_formula_mongo_repository)
):
    """Science GET view."""
    # formula_data = await formula_repository.get(slug=formula.slug)
    formula_obj = FormulaObject.from_dict(formula.data)
    if formula_obj is None:
        return JSONResponse({"detail": "Cannot find formula metadata."}, status_code=404)
    return {
        **formula.as_dict(),
        "category": formula.category.as_dict(),
        "science": (await Science.get(id=formula.category.science_id)).as_dict(),
        "info": formula_obj.as_dict()
    }


@router.post('/formula/{formula_slug}')
@login_required
async def formula_calculate_view(
        request: Request,
        formula: Formula = Depends(get_formula_dependency),
        request_data: RequestData = Body(),
):
    """Request form to calculate."""
    formula_obj = FormulaObject.from_dict(formula.data)
    request_schema = RequestSchema(
        formula_id=str(formula.id),
        url=request.url.path,
        method=request.method,
        user_id=request.user.id,
        **request_data.model_dump()
    )
    result, is_success = counter.count_result(
        request=request_schema,
        formula_obj=formula_obj,
    )
    if is_success:
        await History.create(
            formula_id=formula.id,
            user_id=request.user.id,
            result=result
        )
        return JSONResponse({"result": result}, 200)
    return JSONResponse({"detail": result}, 400)
