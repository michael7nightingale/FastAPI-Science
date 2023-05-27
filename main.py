import sys
import os

sys.path.append(os.getcwd())

from fastapi import FastAPI
import uvicorn
from configuration.server import Server
from internal.users import loginManager


def create_app(_=None) -> FastAPI:
    app = FastAPI()
    return Server(app, loginManager).app


if __name__ == "__main__":
    uvicorn.run(
       app=create_app(), 
       port=8000, 
       host='localhost'
     )