from fastapi import Request, Response, FastAPI
import time


middleware_stack = {}


def middleware(middleware_type: str):
    def inner(func):
        global middleware_stack
        if middleware_type not in middleware_stack:
            middleware_stack[middleware_type] = []
        middleware_stack[middleware_type].append(func)
        return func
    return inner


@middleware("http")
async def process_time_middleware(request: Request, call_next) -> Response:
    start_time = time.time()
    response = await call_next(request)
    finished_time = time.time()
    response.headers['X-Process-Time'] = str(finished_time - start_time)
    return response


def register_middleware(app: FastAPI) -> None:
    for type_, functions in middleware_stack.items():
        for func in functions:
            app.middleware(type_)(func)
