from functools import wraps
from typing import Callable

from fastapi import Request, HTTPException, WebSocket


def login_required(view_func: Callable):
    """Decorator for api view to check token header."""

    @wraps(view_func)
    async def inner(request: Request, *args, **kwargs):
        if request.user is None:  # raise exception if user is not found
            raise HTTPException(403, "Authentication required.")
        return await view_func(request, *args, **kwargs)

    return inner


def ws_login_required(view_func: Callable):
    """Decorator for websocket view to check token header."""

    @wraps(view_func)
    async def inner(websocket: WebSocket, *args, **kwargs):
        if websocket.user is None:  # raise exception if user is not found
            raise HTTPException(403, "Authentication required.")
        return await view_func(websocket, *args, **kwargs)

    return inner
