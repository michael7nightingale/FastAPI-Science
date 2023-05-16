import os
from fastapi import APIRouter, Depends, Form, Path
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import FileResponse

from formulas import contextBuilder, plots
from internal.users import get_current_user, permission
from package.schema import RequestSchema, ScienceEnum
from package.database import FormulasDb as FDb, CategoriesDb as CDb, session, ScienceDb as SDb


science_router = APIRouter(
    prefix='/science'
)
STATIC_DIR = "/app/public/static/"       # appends to BASE_DIR
PLOTS_DIR = "/plots/"

session = session()
FormulasDb = FDb(session)
CategoriesDb = CDb(session)
ScienceDb = SDb(session)

templates = Jinja2Templates(directory=os.getcwd() + '/app/public/templates/science/')


@science_router.on_event("startup")
async def create_formulas():
    """Перед запуском сервера формируется кэш-словарь формул и категорий из БД."""
    await FormulasDb.update_data()


# ================================= PLOTS ================================ #

async def plotsView(request: Request,
                    science_slug: str,
                    *_, **__):
    context = {"request": request,
               "current_science": science_slug}
    user = await get_current_user(request)
    if user is not None:
        plot_path = STATIC_DIR + PLOTS_DIR + f'/{user.id}.png'
        if os.path.exists(os.getcwd() + plot_path):
            context.update(image_url=plot_path)
    return templates.TemplateResponse(f"plots.html", context=context)


# @permission(permissions=())
async def plotsViewPost(request, science_slug, **_):
    """
    Создание графика функции. Отображание только для авторизованных пользователей.
    SQL: _.
    """
    data = await request.form()
    context = dict(request=request, current_science=science_slug)
    message = ""
    user = await get_current_user(request)
    if user is not None:
        functions_list = [data[f"function{i}"] for i in range(1, 5) if data[f"function{i}"]]
        x_lim = data['xmin'], data['xmax']
        if all(x_lim) and functions_list:
            y_lim = data['ymin'], data['ymax']
            y_lim = y_lim if all(y_lim) else None
            plot = plots.Plot(functions_list, x_lim, y_lim)
            plot_path = os.getcwd() + STATIC_DIR + PLOTS_DIR + f"{user.id}.png"
            plot.save_plot(plot_path)
            context.update(image_url=plot_path.replace(os.getcwd(), ''))
        else:
            message = "Неполные данные."
    else:
        message = "Авторизуйтесь, чтобы увидеть график"
    context.update(message=message)
    return templates.TemplateResponse(f"plots.html", context=context)


@science_router.post('/download_plot')
@permission(permissions=())
async def download_plot(request: Request, user=None):
    """Скачать график (только для авторизованных пользователей)."""
    data = await request.form()
    filename, filesurname = data['filename'], data['filesurname']
    return FileResponse(path=os.getcwd() + filename, filename=filesurname + '.png')


SPECIAL_CATEGORIES_GET = {
    "plots": plotsView,
    "equations": 'equations.html'
}

SPECIAL_CATEGORIES_POST = {
    "plots": plotsViewPost,
    "equations": 'equations.html'
}


# =================================== DEPENDENCIES ================================== #

async def science_basic(request: Request,
                        science_slug: ScienceEnum = Path()) -> dict[object, str]:
    """Зависимость для науки."""
    return {'request': request, "science_slug": science_slug.value}


async def formula_basic(
        request: Request,
        science_slug: ScienceEnum = Path(),
        formula_slug: str = Path()
):
    """Зависимость для формулы."""
    formula = await FormulasDb.get_formula(formula_slug)
    category = await CategoriesDb.get_category(formula.category_id)
    if category.super_category == science_slug:
        return {
            "current_science": science_slug.value,
            "request": request,
            "category": category,
            "formula": formula,
                }
    raise HTTPException(status_code=404,
                        detail="Not matching data!")


# ============================== SCIENCE ============================ #

@science_router.get('/{science_slug}')
async def science_main(params: dict = Depends(science_basic)):
    """
    Главная страница науки. Для всех пользователей.
    SQL: science; categories on science.
    """
    science = await ScienceDb.get_science(params['science_slug'])
    categories = await CategoriesDb.get_all_categories(science=params['science_slug'])
    print(science, science.title, science.slug)
    return templates.TemplateResponse("main.html", context={"request": params['request'],
                                                            "current_science": science,
                                                            "categories": categories})


@science_router.get('/{science_slug}/category/{cat_slug}/')
async def science_category(params: dict = Depends(science_basic),
                           cat_slug: str = Path()):
    """
    Category page. For all sciences. Available for everyone.
    SQL: - category; formulas on category;
    """
    context = {"request": params['request'],
               "current_science": params['science_slug']}
    if cat_slug in SPECIAL_CATEGORIES_GET:
        return await SPECIAL_CATEGORIES_GET[cat_slug](**params)
    else:
        formulas_objects = await FormulasDb.get_formulas_by_cat(cat_slug)
        category = await CategoriesDb.get_category(cat_slug)
        formulas = [i.as_dict() for i in formulas_objects]
        context.update({'formulas': formulas, "title": category.category_name})
        return templates.TemplateResponse("category.html", context=context)


@science_router.post('/{science_slug}/category/{cat_slug}/')
async def science_category_post(params: dict = Depends(science_basic),
                                cat_slug: str = Path()):
    """
    Маршрут необходим только для одностраничных специальных категорий. Для всех пользователей.
    SQL: _.
    """
    context = {"request": params['request'],
               "current_science": params['science_slug']}
    if cat_slug in SPECIAL_CATEGORIES_POST:
        return await SPECIAL_CATEGORIES_POST[cat_slug](**params, )
    else:
       raise HTTPException(status_code=404)


@science_router.get('/{science_slug}/formula/{formula_slug}/')
async def science_formula(
        request: Request,
        context: dict = Depends(formula_basic)):
    """
     Форма c формулой при первом открытии или обновлении страницы. Для всех пользователей.
     SQL: category; formula on category.
     """
    requestSchema = RequestSchema(
        url=context["request"].url.path,
        method=context["request"].method,
    )
    built_context = await contextBuilder.build_template(
        request_schema=requestSchema,
        user_id=None,
        formula_name=context['formula'].slug,
        science_name=context['current_science']
    )
    context.update(built_context)
    return templates.TemplateResponse("template_formula.html", context=context)


@science_router.post('/{science_slug}/formula/{formula_slug}/')
async def science_formula_post(
        request: Request,
        context: dict = Depends(formula_basic),
        nums_comma: int = Form(),
        find_mark: str = Form()):
    """
      Форма в формулой после отправки формы впервые. Для всех пользователей.
      SQL: category; formula on category.
      """
    data = await context["request"].form()
    requestSchema = RequestSchema(url=context["request"].url.path,
                                         method=context["request"].method,
                                         find_mark=find_mark,
                                         data=data,
                                         nums_comma=nums_comma)
    user = await get_current_user(request)
    built_context = await contextBuilder.build_template(
        request_schema=requestSchema,
        user_id=user.id if user else None,
        formula_name=context['formula'].slug,
        science_name=context['current_science']
    )
    context.update(built_context)
    return templates.TemplateResponse("template_formula.html", context=context)

