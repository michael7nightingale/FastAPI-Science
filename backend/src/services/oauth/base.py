from abc import ABC, abstractmethod


class BaseProvider(ABC):
    __slots__ = ("client_id", "client_secret", "code", "redirect_url", )
    name: str = None

    def __init__(self, client_id: str, client_secret: str, code: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        if self.name is None:
            self.name = self.__class__.__name__.lower().replace("oauth", "").replace("provider", "")

    @abstractmethod
    def provide(self) -> dict | None:
        pass
