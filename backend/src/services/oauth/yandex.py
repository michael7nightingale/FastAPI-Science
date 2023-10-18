import requests

from .base import BaseProvider


class YandexOAuthProvider(BaseProvider):
    __slots__ = ()
    name = "yandex"

    def get_access_token(self) -> str | None:
        body_data = {
            "code": self.code,
            'grant_type': "authorization_code",
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post("https://oauth.yandex.ru/token", json=body_data)
        print(response.content)
        if not response:
            return
        access_token = response.json()['access_token']
        return access_token

    def get_user_data(self, access_token: str) -> dict | None:
        response = requests.get(
            f"https://login.yandex.ru/info",
            params={
                "access_token": access_token,
                "format": "json"
            }
        )
        if not response:
            return
        user_data = response.json()
        print(user_data)
        return user_data

    def provide(self):
        access_token = self.get_access_token()
        if access_token is None:
            return
        user_data = self.get_user_data(access_token)
        if not user_data:
            return
        print(user_data)
        return user_data
