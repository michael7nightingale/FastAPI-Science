# from typing import Callable
# from functools import lru_cache, wraps
# from fastapi.exceptions import RequestValidationError, StarletteHTTPException
# from fastapi.responses import RedirectResponse, FileResponse
# from fastapi import FastAPI, Path, Form, Depends, Request, File, UploadFile
# from fastapi import HTTPException
# from fastapi_login import LoginManager
# from fastapi.templating import Jinja2Templates
# from starlette.staticfiles import StaticFiles
# import datetime
# import sys
# import os
# sys.path.append(os.getcwd() + '/app/package/')
#
# from app.formulas import contextBuilder
# from app.package.exceptions import NotAuthenticatedException
# from app.package import database
# from app.formulas import plots
# from app.package import schema
#
# # ============================ CONFIGURATIONS ============================ #
#
# app = FastAPI()
# BASE_DIR = ""
# print(os.getcwd())
# STATIC_DIR = BASE_DIR.replace(os.getcwd(), '').replace('\\', '/') + "/public/static/"       # appends to BASE_DIR
# PLOTS_DIR = "/plots/"                                                                       # appends to STATIC_DIR
# TEMPLATES_DIR = BASE_DIR + '/public/templates/'                                             # appends to STATIC_DIR
# TEMPLATES_DIRS = ['main/', 'users/', 'science/', 'error/', 'search/']
# templates = Jinja2Templates(directory=TEMPLATES_DIR)
# app.mount(STATIC_DIR, StaticFiles(directory=STATIC_DIR.lstrip("/")), name="static")
#
#
# loginManager = LoginManager(
#     'secret',
#     token_url='/login',
#     use_cookie=True,
#     custom_exception=NotAuthenticatedException,
#     default_expiry=datetime.timedelta(hours=12),
#
# )
# loginManager.useRequest(app)
#
#
# session = database.session()
# UsersDb = database.UsersDb(session)
# FormulasDb = database.FormulasDb(session)
# HistoryDb = database.HistoryDb(session)
# CategoriesDb = database.CategoriesDb(session)
# ScienceDb = database.ScienceDb(session)
#
#
# # ============================ ERRORHANDLERS ============================ #
#
# @app.exception_handler(RequestValidationError)
# async def validation_exc_handler(request: Request, exc):
#     print(exc)
#     return templates.TemplateResponse("error/500.html", context={'request': request})
#
#
# @app.exception_handler(StarletteHTTPException)
# async def http_exc_handler(request: Request, exc):
#     print(exc)
#     if exc.status_code == 402:
#         return RedirectResponse(url='/login', status_code=303)
#     elif exc.status_code == 404:
#         return templates.TemplateResponse('error/404.html', context={'request': request})
#     elif exc.status_code == 403:
#         return templates.TemplateResponse('error/403.html', context={'request': request})
#     elif exc.status_code == 500:
#         return templates.TemplateResponse("error/500.html", context={'request': request})
#
#
# # ============================ SERVICE ============================ #
#
# @app.on_event('startup')
# async def create_formulas():
#     check_directories()
#     await FormulasDb.update_data()
#
#
# def check_directories():
#     """Checking if all important directories are existing. Otherwise, the app won`t be started."""
#     assert os.path.exists(os.getcwd() + STATIC_DIR), f"Static directory does not exists: {STATIC_DIR}"
#     assert os.path.exists(TEMPLATES_DIR), f"Template directory does not exists: {TEMPLATES_DIR}"
#     for temp in TEMPLATES_DIRS:
#         assert os.path.exists(TEMPLATES_DIR + temp), f"Template subdirectory does not exists: {temp}"
#     FULL_PLOT_PATH = os.getcwd() + STATIC_DIR + PLOTS_DIR
#     if not os.path.exists(FULL_PLOT_PATH):  # plots dir may be created empty
#         os.mkdir(FULL_PLOT_PATH)
#
#
# @loginManager.user_loader()
# async def get_user_from_db(username: str):
#     return await UsersDb.get_user(username)
#
#
# async def get_current_user(request: Request) -> None | database.Users:
#     token = request.cookies.get('access-token')
#     if token is not None:
#         try:
#             user_dict = loginManager._get_payload(token)
#             user = await get_user_from_db(username=user_dict['username'])
#             # user = await UsersDb.get_user(user_dict['username'])
#             return user
#         except NotAuthenticatedException:
#             user = None
#         except:
#             raise HTTPException(status_code=403, detail="You are not registered")
#         return user
#
#
# async def is_superuser(request: Request) -> database.Users | None:
#     user = await get_current_user(request)
#     if user:
#         return user if user.is_superuser else None
#
#
# async def is_stuff(request: Request) -> database.Users | None:
#     user = await get_current_user(request)
#     if user:
#         return user if user.is_stuff else None
#
#
# @lru_cache(maxsize=64)
# def permission(permissions: tuple):
#     __permissions = ('superuser', 'stuff')
#     def decorator(func: Callable):
#         @wraps(func)
#         async def inner(request: Request, user, *args, **kwargs):
#             nonlocal __permissions
#             if not all(perm in __permissions for perm in permissions):
#                 raise HTTPException(status_code=403, detail='Permission denied')
#             for i in set(permissions):
#                 if user is None:
#                     if i == 'stuff':
#                         user = await is_stuff(request)
#                     elif i == 'superuser':
#                         user = await is_superuser(request)
#             if user is None:
#                 if permissions:
#                     raise HTTPException(status_code=403, detail='Permission denied')
#                 else:
#                     user = await get_current_user(request)
#                     if user is None:
#                         return RedirectResponse(url=app.url_path_for('login'), status_code=303)
#             res = await func(request, user, *args, **kwargs)
#             return res
#         return inner
#     return decorator
#
#
# # ============================ DEPENDENCIES ============================ #
#
# async def science_basic(request: Request,
#                         science_slug: schema.ScienceEnum = Path()) -> dict[object, str]:
#     return {'request': request, "science_slug": science_slug.value}
#
#
# async def formula_basic(
#         request: Request,
#         science_slug: schema.ScienceEnum = Path(),
#         formula_slug: str = Path()
# ):
#     formula = await FormulasDb.get_formula(formula_slug)
#     category = await CategoriesDb.get_category(formula.category_id)
#     if category.super_category == science_slug:
#         return {
#             "current_science": science_slug.value,
#             "request": request,
#             "category": category,
#             "formula": formula,
#                 }
#
#     raise HTTPException(status_code=404,
#                         detail="Not matching data!")
#
#
# # =================================== URLS ============================ #
#
#
# @app.get("/")
# async def homepage(request: Request):
#     return templates.TemplateResponse("main/main.html", context={"request": request})
#
# # =================================== USERS ============================ #
#
# @app.get("/login")
# async def login(request: Request):
#     return templates.TemplateResponse('users/login.html', context={"request": request,})
#
#
# @app.post('/login')
# async def login_post(request: Request,
#                      user_data: dict = Depends(user_parameters)):
#     user: database.Users = await UsersDb.login_user(user_data["username"],
#                                     user_data['password'])
#     user_access_token = loginManager.create_access_token(data=schema.UserInSchema(**user.as_dict()).dict(),
#                                                          expires=datetime.timedelta(hours=12))
#     response = RedirectResponse(app.url_path_for('homepage'), status_code=303)
#     loginManager.set_cookie(response, user_access_token)
#     request.state.user = user
#     request.cookies['access-token'] = user_access_token
#     return response
#
#
# @app.get("/register")
# async def register(request: Request,
#                    user = None):
#     return templates.TemplateResponse('users/register.html', context={"request": request,})
#
#
# @app.post("/register")
# async def register_post(request: Request,
#                         user_data: dict = Depends(user_parameters_extra)):
#     user = await UsersDb.create_user(**user_data)
#     return RedirectResponse(app.url_path_for('login'), status_code=303)
#
#
# @app.get('/logout')
# async def logout(request: Request):
#     response =  RedirectResponse(url=app.url_path_for('homepage'), status_code=303)
#     response.delete_cookie(key='access-token')
#     return response
#
#
# @app.get('/history/{user_id}/')
# @permission(permissions=())
# async def get_history(request: Request,
#                       user=None,
#                       user_id: int = Path()):
#     if user.id != user_id:
#         raise HTTPException(status_code=403)
#     history_list = await HistoryDb.get_history(user_id)
#     context = {"title": "История вычислений",
#                "history": history_list,
#                'request': request}
#     return templates.TemplateResponse("users/history.html", context=context)
#
#
# # =============================== PLOTS ============================ #
#
# async def plotsView(request, science_slug, **_):
#     context = dict(request=request, current_science=science_slug)
#     return templates.TemplateResponse(f"science/plots.html", context=context)
#
#
# # @permission(permissions=())
# async def plotsViewPost(request, science_slug, **_):
#     data = await request.form()
#     context = dict(request=request, current_science=science_slug)
#     message = ""
#     user = await get_current_user(request)
#     if user is not None:
#         functions_list = [data[f"function{i}"] for i in range(1, 5) if data[f"function{i}"]]
#         x_lim = data['xmin'], data['xmax']
#         if all(x_lim) and functions_list:
#             y_lim = data['ymin'], data['ymax']
#             y_lim = y_lim if all(y_lim) else None
#             plot = plots.Plot(functions_list, x_lim, y_lim)
#             plot_path = os.getcwd() + STATIC_DIR + PLOTS_DIR + f"{user.id}.png"
#             plot.save_plot(plot_path)
#             context.update(image_url=plot_path.replace(os.getcwd(), ''))
#         else:
#             message = "Неполные данные."
#     else:
#         message = "Авторизуйтесь, чтобы увидеть график"
#     context.update(message=message)
#     return templates.TemplateResponse(f"science/plots.html", context=context)
#
#
# @app.post('/download_plot')
# async def download_plot(request: Request):
#     data = await request.form()
#     filename, filesurname = data['filename'], data['filesurname']
#     return FileResponse(path=os.getcwd() + filename, filename=filesurname + '.png')
#
#
# SPECIAL_CATEGORIES_GET = {
#     "plots": plotsView,
#     "equations": 'equations.html'
# }
#
# SPECIAL_CATEGORIES_POST = {
#     "plots": plotsViewPost,
#     "equations": 'equations.html'
# }
#
#
# # ============================== SCIENCE ============================ #
#
# @app.get('/{science_slug}')
# async def science_main(params: dict = Depends(science_basic)):
#     science = await ScienceDb.get_science(params['science_slug'])
#     categories = await CategoriesDb.get_all_categories(science=params['science_slug'])
#     return templates.TemplateResponse("science/main.html", context={"request": params['request'],
#                                                                     "current_science": science,
#                                                                     "categories": categories})
#
#
# @app.get('/{science_slug}/category/{cat_slug}/')
# async def science_category(params: dict = Depends(science_basic),
#                            cat_slug: str = Path()):
#     """
#     Category page. For all sciences. Available for everyone.
#     SQL: - category; formulas on category;
#     """
#     context = {"request": params['request'],
#                "current_science": params['science_slug']}
#     if cat_slug in SPECIAL_CATEGORIES_GET:
#         return await SPECIAL_CATEGORIES_GET[cat_slug](**params)
#     else:
#         formulas_objects = await FormulasDb.get_formulas_by_cat(cat_slug)
#         category = await CategoriesDb.get_category(cat_slug)
#         formulas = [i.as_dict() for i in formulas_objects]
#         context.update({'formulas': formulas, "title": category.category_name})
#         return templates.TemplateResponse("science/category.html", context=context)
#
#
# @app.post('/{science_slug}/category/{cat_slug}/')
# async def science_category(params: dict = Depends(science_basic),
#                            cat_slug: str = Path()):
#     context = {"request": params['request'],
#                "current_science": params['science_slug']}
#     if cat_slug in SPECIAL_CATEGORIES_POST:
#         return await SPECIAL_CATEGORIES_POST[cat_slug](**params, )
#     else:
#        raise HTTPException(status_code=404)
#
#
# @app.get('/{science_slug}/formula/{formula_slug}/')
# async def science_formula(
#         request: Request,
#         context: dict = Depends(formula_basic)):
#     requestSchema = schema.RequestSchema(
#         url=context["request"].url.path,
#         method=context["request"].method,
#     )
#     built_context = await contextBuilder.build_template(
#         request_schema=requestSchema,
#         user_id=None,
#         formula_name=context['formula'].slug,
#         science_name=context['current_science']
#     )
#     context.update(built_context)
#     return templates.TemplateResponse("science/template_formula.html", context=context)
#
#
# @app.post('/{science_slug}/formula/{formula_slug}/')
# async def science_formula_post(
#         request: Request,
#         context: dict = Depends(formula_basic),
#         nums_comma: int = Form(),
#         find_mark: str = Form()):
#     data = await context["request"].form()
#     requestSchema = schema.RequestSchema(url=context["request"].url.path,
#                                          method=context["request"].method,
#                                          find_mark=find_mark,
#                                          data=data,
#                                          nums_comma=nums_comma)
#     user = await get_current_user(request)
#     built_context = await contextBuilder.build_template(
#         request_schema=requestSchema,
#         user_id=user.id if user else None,
#         formula_name=context['formula'].slug,
#         science_name=context['current_science']
#     )
#     context.update(built_context)
#     return templates.TemplateResponse("science/template_formula.html", context=context)
#
#
#
