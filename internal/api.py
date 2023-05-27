from fastapi import FastAPI, Path, Query, Body, Form, Depends, Request, APIRouter
from fastapi import HTTPException, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from formulas import contextBuilder
from fastapi.templating import Jinja2Templates
from package import database
from package import schema

# from package.schema import Tags


api_router = APIRouter(
    prefix="/api/v1"
)
templates = Jinja2Templates(directory="public/templates/")

session = database.session()
UsersDb = database.UsersDb(session)
FormulasDb = database.FormulasDb(session)
HistoryDb = database.HistoryDb(session)


# ========================= ROTES ========================= #

@api_router.get('/', status_code=status.HTTP_200_OK)
async def get_home(request: Request):
    return JSONResponse({
        "site": str(request.url_for("redirect_to_site")),
        "sciences": str(request.url_for("get_sciences")),
        "register": str(request.url_for("register")),
        "login": str(request.url_for("login"))
    })


@api_router.get('/site/')
async def redirect_to_site(teleport: bool = Query(default=False)):
    if teleport:
        return RedirectResponse(url='http://127.0.0.1:8001')
    return {'url': 'http://127.0.0.1:8001'}


@api_router.get("/sciences/")
async def get_sciences(request: Request):
    return JSONResponse({
        # i: str(request.url_for("get_science", science_name=i)) for i in database.categories_models
    })


@api_router.get('/sciences/{science_name}/')
async def get_science(science_name: schema.ScienceEnum, request: Request):
    return JSONResponse({
        "science_name": science_name,
        "categories": {i: {
            "url": str(request.url_for("get_category", science_name=science_name.value, category_name=i))
                           }
                       for i in FormulasDb.CATEGORIES[science_name]}
    })


@api_router.get('/sciences/{science_name}/{category_name}/')
async def get_category(science_name: schema.ScienceEnum,
                       category_name):
    # if await validators.check_category(science_name, category_name):
    return await FormulasDb.get_formulas_by_cat(category_name)
    # else:
        # raise HTTPException(status_code=403, detail='Science and category don`t match~!')


# @api_router.post('/api/create-formula/',
#           # response_model=schema.FormulaSchema,
#           status_code=status.HTTP_201_CREATED,
#           tags=[Tags.formula])
# async def create_formula(formula: schema.FormulaSchema = Body(embed=True)):
#     try:
#         await FormulasDb.create_formula()
#         return JSONResponse(formula)
#     except Exception as e:
#         raise HTTPException(status_code=402, detail="Incorrect formula data for creation!")


@api_router.get('/sciences/{science_name}/{category_name}/{formula_name}/')
async def get_formula(science_name: schema.ScienceEnum,
                       category_name,
                       formula_name: str = Path(title="Name of the formula", min_length=5, max_length=35)):
    # print(FormulasDb.FORMULAS[science_name][category_name])
    # if await validators.check_formula(science_name, category_name, formula_name):
    formula = await FormulasDb.get_formula(formula_name)
    return formula


# dependency
async def user_parameters(username: str = Form(),
                          password: str = Form()):
    return {"username": username, "password": password}


async def user_parameters_extra(parameters: dict = Depends(user_parameters),
                                email: str = Form()):
    parameters.update({"email": email})
    return JSONResponse(parameters)


# ================================ USERS =============================== #

@api_router.post('/sciences/{science_name}/{category_name}/{formula_name}/',)
async def count_formula(
        request: Request,
        science_name: schema.ScienceEnum = Path(),
        category_name: str = Path(),
        formula_name: str = Path(title="Name of the formula", min_length=5, max_length=35),
        nums_comma: int = Body(ge=0, le=10),
        find_mark: str = Body(max_length=1),
        data = Body()):
    # print(data, nums_comma, find_mark)
    # if await validators.check_formula(science_name, category_name, formula_name):
    request_schema = schema.RequestSchema(find_mark=find_mark,
                                              nums_comma=nums_comma,
                                              data=data,
                                              method=request.method,
                                              user_id=4,
                                              url=request.url.path)
    return JSONResponse(await contextBuilder.build_template(request_schema, 4, formula_name))


@api_router.post('/register/')
async def register(user_data: dict = Depends(user_parameters_extra)):
    try:
       await UsersDb.register_user(**user_data)
       return await login(await user_parameters(user_data['username'], user_data["password"]))
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=402, detail="Register Failed")


@api_router.post('/api/login/', response_model=schema.UserInSchema)
async def login(user_data: dict = Depends(user_parameters)):
    user = await UsersDb.login_user(**user_data)
    return JSONResponse(jsonable_encoder(user))


@api_router.post('/api/logout/')
async def logout(user_data: dict = Depends(user_parameters)):
    return user_data


@api_router.get('/api/history/{user_id}/')
async def get_history(user_id):
    return JSONResponse(jsonable_encoder(await HistoryDb.get_history(user_id)))



