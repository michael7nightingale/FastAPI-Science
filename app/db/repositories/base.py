from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """
    Base repository class to access object management.
    """
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def all(self, *args, **kwargs):
        pass

    @abstractmethod
    def filter(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass
