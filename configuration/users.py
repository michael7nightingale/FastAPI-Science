# import datetime
#
# from fastapi_login import LoginManager
#
# from app.package.exceptions import NotAuthenticatedException
#
# loginManager = LoginManager(
#     'secret',
#     token_url='/login',
#     use_cookie=True,
#     custom_exception=NotAuthenticatedException,
#     default_expiry=datetime.timedelta(hours=12),
#
# )
# # loginManager.useRequest(app)