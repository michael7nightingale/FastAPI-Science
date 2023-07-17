from fastapi import APIRouter, Depends, Form, Path, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi_authtools import login_required
from starlette.exceptions import HTTPException
import os

from app.models.schemas import RequestSchema
from app.formulas import contextBuilder, plots, mathem_extra_counter
from app.db.repositories import ScienceRepository, CategoryRepository, FormulaRepository, HistoryRepository
from app.api.dependencies import get_repository


science_router = APIRouter(
    prefix='/science'
)
STATIC_DIR = "app/public/static/"       # appends to BASE_DIR
PLOTS_DIR = "/plots/"

templates = Jinja2Templates('app/public/templates/science/')


# ================================= PLOTS ================================ #

async def plots_view(request: Request, science_slug: str):
    context = {"request": request,
               "current_science": science_slug}
    user = request.user
    if user is not None:
        plot_path = STATIC_DIR + PLOTS_DIR + f'/{user.id}.png'
        if os.path.exists(plot_path):
            context.update(image_url=plot_path)
    return templates.TemplateResponse(f"plots.html", context=context)


async def plots_view_post(request: Request, science_slug: str):
    """
    Создание графика функции. Отображание только для авторизованных пользователей.
    SQL: _.
    """
    data = await request.form()
    context = dict(request=request, current_science=science_slug)
    message = ""
    user = request.user
    if user is not None:
        functions_list = [data[f"function{i}"] for i in range(1, 5) if data[f"function{i}"]]
        x_lim = data['xmin'], data['xmax']
        if all(x_lim) and functions_list:
            y_lim = data['ymin'], data['ymax']
            y_lim = y_lim if all(y_lim) else None
            try:
                plot = plots.Plot(functions_list, x_lim, y_lim)
                plot_path = os.getcwd() + STATIC_DIR + PLOTS_DIR + f"{user.id}.png"
                plot.save_plot(plot_path)
                context.update(image_url=plot_path.replace(os.getcwd(), ''))
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
    return templates.TemplateResponse(f"plots.html", context=context)


@science_router.post('/download_plot')
async def download_plot(request: Request):
    """Скачать график (только для авторизованных пользователей)."""
    data = await request.form()
    filename, filesurname = data['filename'], data['filesurname']
    return FileResponse(path=os.getcwd() + filename, filename=filesurname + '.png')


# ======================================= EQUATIONS ===================================== #

async def equations_view(request: Request,
                         science_slug: str,
                         *_, **__):
    context = {
        "request": request,
        "science_slug": science_slug,
        "result": ""
    }
    return templates.TemplateResponse("equations.html", context=context)


async def equations_view_post(request: Request,
                              science_slug: str,
                              *_, **__):
    form_data = await request.form()
    message = ""
    result = "Здесь появится решение."
    equations = list(filter(bool, form_data.values()))
    if len(equations) > 0:
        result = mathem_extra_counter.equation_system(equations)
    else:
        message = "Данные не предоставлены."
    context = {
        "message": "",
        "request": request,
        "science_slug": science_slug,
        "result": result
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


@science_router.get('/science/{science_slug}')
async def science_main(
        request: Request,
        science_repo: ScienceRepository = Depends(get_repository(ScienceRepository)),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository)),
        science_slug: str = Path()
):
    """
    Главная страница науки. Для всех пользователей.
    SQL: science; categories on science.
    """
    science = await science_repo.get(science_slug)
    categories = await category_repo.filter(science_id=science.id)
    context = {
        "science": science,
        "categories": categories,
        "request": request
    }
    return templates.TemplateResponse("main.html", context=context)


@science_router.get('/category/{category_slug}/')
async def science_category(
        request: Request,
        science_repo: ScienceRepository = Depends(get_repository(ScienceRepository)),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository)),
        formula_repo: FormulaRepository = Depends(get_repository(FormulaRepository)),
        category_slug: str = Path(),
):
    """
    Category page. For all sciences. Available for everyone.
    SQL: - category; formulas on category;
    """
    if category_slug in SPECIAL_CATEGORIES_GET:
        return await SPECIAL_CATEGORIES_GET[category_slug](request, category_slug=category_slug)
    else:
        category = await category_repo.get(category_slug)
        science = await science_repo.get_by(id=category.science_id)
        formulas = await formula_repo.filter(category_id=category.id)
        # formulas = [i.as_dict() for i in formulas_objects]
        context = {
            'formulas': formulas,
            "title": category.title,
            "request": request,
            "category": category,
            "science_slug": science.slug
        }
        return templates.TemplateResponse("category.html", context=context)


@science_router.post('/category/{category_slug}/')
async def science_category_post(
        request: Request,
        category_slug: str = Path()
):
    """
    Маршрут необходим только для одностраничных специальных категорий. Для всех пользователей.
    SQL: _.
    """
    if category_slug in SPECIAL_CATEGORIES_POST:
        return await SPECIAL_CATEGORIES_POST[category_slug](request, category_slug=category_slug)
    else:
        raise HTTPException(status_code=404)


@science_router.get('/formula/{formula_slug}/')
async def science_formula(
        request: Request,
        formula_repo: FormulaRepository = Depends(get_repository(FormulaRepository)),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository)),
        formula_slug: str = Path()
):
    """
     Форма c формулой при первом открытии или обновлении страницы. Для всех пользователей.
     SQL: category; formula on category.
    """
    request_schema = RequestSchema(
        url=request.url.path,
    )
    try:
        formula = await formula_repo.get(formula_slug)
        category = await category_repo.get_by(id=formula.category_id)
        context = await contextBuilder.build_template(
            request=request_schema,
            formula_slug=formula_slug
        )
        context.update(formula=formula, request=request, category=category)
        return templates.TemplateResponse("template_formula.html", context=context)
    except KeyError:
        raise HTTPException(status_code=500)


@science_router.post('/formula/{formula_slug}/')
@login_required
async def science_formula_post(
        request: Request,
        formula_slug: str = Path(),
        nums_comma: int = Form(),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository)),
        formula_repo: FormulaRepository = Depends(get_repository(FormulaRepository)),
        history_repo: HistoryRepository = Depends(get_repository(HistoryRepository)),
        find_mark: str = Form()
):
    """
     Форма в формулой после отправки формы впервые. Для всех пользователей.
     SQL: category; formula on category.
     """
    data = await request.form()
    request_schema = RequestSchema(
        url=request.url.path,
        method=request.method,
        find_mark=find_mark,
        user_id=request.user.id,
        data=data,
        nums_comma=nums_comma
    )
    formula = await formula_repo.get(formula_slug)
    category = await category_repo.get_by(id=formula.category_id)
    context = await contextBuilder.build_template(
        request=request_schema,
        formula_slug=formula_slug
        )
    context.update(formula=formula, request=request,  category=category)
    return templates.TemplateResponse("template_formula.html", context=context)


# @science_router.get("/load-data")
# async def load_data(
#         request: Request,
#         science_repo: ScienceRepository = Depends(get_repository(ScienceRepository)),
#         category_repo: CategoryRepository = Depends(get_repository(CategoryRepository)),
#         formula_repo: FormulaRepository = Depends(get_repository(FormulaRepository)),
# ):
#     import csv
#     with open("app/data/categories.csv") as file:
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
