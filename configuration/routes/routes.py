from dataclasses import dataclass
from fastapi import FastAPI

__all__ = ['Routes']


@dataclass(frozen=True)
class Routes:
    routes: tuple

    def register_rotes(self, app: FastAPI):
        for router in self.routes:
            app.include_router(router)
