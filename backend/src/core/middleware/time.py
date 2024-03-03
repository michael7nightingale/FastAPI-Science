from fastapi import Request, Response
import time


async def process_time_middleware(request: Request, call_next) -> Response:
    start_time = time.time()
    response = await call_next(request)
    finished_time = time.time()
    response.headers['X-Process-Time'] = str(finished_time - start_time)
    return response
