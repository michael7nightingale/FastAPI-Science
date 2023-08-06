from fastapi import APIRouter, Form, Path, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi_authtools import login_required
from starlette.exceptions import HTTPException
import os

from .models import Science, Category, Formula
from src.services.formulas.plots import Plot
from .schemas import RequestSchema
from ...services.formulas import contextBuilder, mathem_extra_counter


science_router = APIRouter(
    prefix='/sciences'
)
PLOTS_DIR = "sciences/images/plots/"

templates = Jinja2Templates('src/apps/sciences/templates/')


# ================================= PLOTS ================================ #

@login_required
async def plots_view(
        request: Request,
        category_slug: str,
):
    """Plot category GET view."""
    category = await Category.get_or_none(slug=category_slug)

    context = {
        "request": request,
        "science": category.science,
        "category": category
    }
    plot_path = PLOTS_DIR + f'{request.user.id}.png'
    full_plot_path = request.app.state.STATIC_DIR + plot_path
    if request.user is not None:
        if os.path.exists(full_plot_path):
            context.update(image_url=plot_path)
    return templates.TemplateResponse("plots.html", context=context)


async def plots_view_post(
        request: Request,
        category_slug: str,
):
    """Plot image creation. Watch for authorized only."""
    data = await request.form()
    category = await Category.get_or_none(slug=category_slug)
    context = {
        "request": request,
        "science": category.science,
        "category": category
    }
    message = ""
    if request.user is not None:
        functions_list = [data[f"function{i}"] for i in range(1, 5) if data[f"function{i}"]]
        x_lim = data['xmin'], data['xmax']
        if all(x_lim) and functions_list:
            y_lim = data['ymin'], data['ymax']
            y_lim = y_lim if all(y_lim) else None
            try:
                plot = Plot(functions_list, x_lim, y_lim)
                plot_path = PLOTS_DIR + f'{request.user.id}.png'
                full_plot_path = request.app.state.STATIC_DIR + plot_path
                plot.save_plot(full_plot_path)
                context.update(image_url=plot_path)
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
    else:
        message = "Авторизуйтесь, чтобы увидеть график"
    context.update(message=message)
    return templates.TemplateResponse("plots.html", context=context)


@science_router.post('/download_plot')
@login_required
async def download_plot(request: Request, filesurname: str = Form()):
    """Plot download view."""
    plot_path = PLOTS_DIR + f'{request.user.id}.png'
    full_plot_path = request.app.state.STATIC_DIR + plot_path
    if os.path.exists(full_plot_path):
        return FileResponse(path=full_plot_path, filename=filesurname + '.png')


# ======================================= EQUATIONS ===================================== #

async def equations_view(request: Request, category_slug: str):
    category = await Category.get_or_none(slug=category_slug)
    message = ""
    result = "Здесь появится решение."
    context = {
        "request": request,
        "sciences": category.science,
        "category": category,
        "result": result,
        "message": message,

    }
    return templates.TemplateResponse("equations.html", context=context)


async def equations_view_post(request: Request, category_slug: str):
    form_data = await request.form()
    message = ""
    result = "Здесь появится решение."
    equations = list(filter(bool, form_data.values()))
    if len(equations) > 0:
        result = mathem_extra_counter.equation_system(equations)
    else:
        message = "Данные не предоставлены."
    category = await Category.get_or_none(slug=category_slug)
    context = {
        "request": request,
        "sciences": category.science,
        "category": category,
        "result": result,
        "message": message,

    }
    return templates.TemplateResponse("equations.html", context=context)


SPECIAL_CATEGORIES_GET = {
    "plots": plots_view,
    "equations": equations_view
}

SPECIAL_CATEGORIES_POST = {
    "plots": plots_view_post,
    "equations": equations_view_post
}


@science_router.get('/all')
async def sciences_all(request: Request):
    """Science list view."""
    sciences = await Science.all()
    context = {
        "sciences": sciences,
        "request": request
    }
    return templates.TemplateResponse("main.html", context=context)


@science_router.get('/{science_slug}')
async def science_get(request: Request, science_slug: str = Path()):
    """Science detail view."""
    science = await Science.get_or_none(slug=science_slug)
    context = {
        "science": science,
        "categories": science.categories,
        "request": request
    }
    return templates.TemplateResponse("science.html", context=context)


@science_router.get('/category/{category_slug}/')
async def category_get(
        request: Request,
        category_slug: str = Path(),
):
    """Category GET view."""
    if category_slug in SPECIAL_CATEGORIES_GET:
        return await SPECIAL_CATEGORIES_GET[category_slug](
            request,
            category_slug=category_slug,
        )
    else:
        category = await Category.get_or_none(slug=category_slug)
        context = {
            'formulas': category.formulas,
            "title": category.title,
            "request": request,
            "category": category,
            "science_slug": category.science.slug
        }
        return templates.TemplateResponse("category.html", context=context)


@science_router.post('/category/{category_slug}/')
async def category_post(request: Request, category_slug: str = Path()):
    """Category POST view."""
    if category_slug in SPECIAL_CATEGORIES_POST:
        return await SPECIAL_CATEGORIES_POST[category_slug](
            request,
            category_slug=category_slug,
        )
    else:
        raise HTTPException(status_code=404)


@science_router.get('/formula/{formula_slug}/')
async def formula_get(request: Request, formula_slug: str = Path()):
    """Science GET view."""
    try:
        formula = await Formula.get_or_none(slug=formula_slug)
        request_schema = RequestSchema(
            formula_id=str(formula.id),
            url=request.url.path
        )
        context = await contextBuilder.build_template(
            request=request_schema,
            formula_slug=formula_slug
        )
        context.update(formula=formula, request=request, category=formula.category)
        return templates.TemplateResponse("template_formula.html", context=context)
    except KeyError:
        raise HTTPException(status_code=500)


@science_router.post('/formula/{formula_slug}/')
@login_required
async def formula_post(
        request: Request,
        formula_slug: str = Path(),
        nums_comma: int = Form(),
        find_mark: str = Form()
):
    """Request form to calculate."""
    data = await request.form()
    formula = await Formula.get_or_none(slug=formula_slug)
    request_schema = RequestSchema(
        formula_id=str(formula.id),
        url=request.url.path,
        method=request.method,
        find_mark=find_mark,
        user_id=request.user.id,
        data=data,
        nums_comma=nums_comma
    )
    context = await contextBuilder.build_template(
        request=request_schema,
        formula_slug=formula_slug,
    )
    context.update(formula=formula, request=request,  category=formula.category)
    return templates.TemplateResponse("template_formula.html", context=context)


# @science_router.get("/load-data")
# async def load_data(
#         request: Request,
#         science_repo: ScienceRepository = Depends(get_repository(ScienceRepository)),
#         category_repo: CategoryRepository = Depends(get_repository(CategoryRepository)),
#         formula_repo: FormulaRepository = Depends(get_repository(FormulaRepository)),
# ):
#     import csv
#     with open("fullstack/data/categories.csv") as file:
#         lines = list(csv.DictReader(file))
#
#     # for l in lines:
#     #     l["id"] = str(uuid4())
#     #     l["title"] = l['category_name']
#     #     l['science_id'] = (await science_repo.get(l["super_category"])).id
#     #     del l["super_category"]
#     #     del l["category_name"]
#     #     await category_repo.create(**l)
#
