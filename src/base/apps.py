from fastapi import APIRouter


class BaseConfig:
    static_directory: str
    static_path: str
    static_name: str
    router: APIRouter
    api_router: APIRouter

