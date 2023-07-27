from abc import ABC, abstractmethod
from typing import Type

from app.db.repositories import BaseRepository


class BaseService(ABC):
    """
    Base service class. Describes attributes and needed parts to define by
    inherits. Must implement logic to service with object on its type.
    """
    repository_class: Type[BaseRepository]

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def all(self, *args, **kwargs):
        pass

    @abstractmethod
    def filter(self, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass
