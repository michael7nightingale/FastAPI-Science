from fastapi import FastAPI
from starlette.middleware import authentication
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection

from src.apps.users.models import User
from src.services.jwt import decode_jwt_token


RequestUser = User | authentication.UnauthenticatedUser


class AuthenticationBackend(authentication.AuthenticationBackend):
    """
    Auth backend class is used in AuthenticationMiddleware.
    Manages token header and `Request.user`.
    """

    @staticmethod
    async def verify_token(token: str | None) -> tuple[list, RequestUser]:
        """Get user from token."""
        scopes = []
        if token is None:
            return scopes, authentication.UnauthenticatedUser()
        token_data = decode_jwt_token(token)
        if token_data is None:
            return scopes, authentication.UnauthenticatedUser()
        user = await User.get_or_none(id=token_data.user_id)
        if user is None:
            raise authentication.AuthenticationError({"detail": "Invalid credentials."})
        return scopes, user

    @staticmethod
    def get_token_ws(conn: HTTPConnection) -> str:
        """Get token from current http connection."""
        query_token = conn.query_params.get("authorization")
        if query_token is None:
            return
        return query_token.split()[-1].strip()

    @staticmethod
    def get_token_http(conn: HTTPConnection) -> str | None:
        """Get token from current http connection."""
        header_token = conn.headers.get("authorization")
        if header_token is None:
            return
        return header_token.split()[-1].strip()

    async def authenticate(
            self, conn: HTTPConnection
    ) -> tuple[authentication.AuthCredentials, RequestUser]:   # type: ignore
        """Called form super().__call__()"""
        match conn.scope["type"]:
            case "websocket":
                token = self.get_token_ws(conn) or self.get_token_http(conn)
            case _:
                token = self.get_token_http(conn)
        response = await self.verify_token(token)
        scopes, user = response
        return authentication.AuthCredentials(scopes=scopes), user


def use_authentication_middleware(app: FastAPI) -> None:
    app.add_middleware(AuthenticationMiddleware, backend=AuthenticationBackend())
