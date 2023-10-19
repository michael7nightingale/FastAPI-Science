import requests

from .base import BaseProvider


class GoogleOAuthProvider(BaseProvider):
    __slots__ = ()
    name = "google"

    def get_access_token(self) -> str | None:
        params = {
            'code': self.code,
            'redirect_uri': "http://localhost:8000/auth/google/callback",
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code'
        }
        response = requests.post(
            url="https://accounts.google.com/o/oauth2/token",
            params=params,
            json=params
        )
        if not response:
            return
        access_token = response.json()['access_token']
        return access_token

    def get_user_data(self, access_token: str) -> dict | None:
        response = requests.get(
            url="https://www.googleapis.com/oauth2/v1/userinfo",
            params={"access_token": access_token}
        )
        if not response:
            return
        user_data = response.json()
        return user_data

    def provide(self):
        access_token = self.get_access_token()
        if access_token is None:
            return
        user_data = self.get_user_data(access_token)
        if not user_data:
            return
        user_data['username'] = user_data['email']
        user_data['first_name'] = user_data.get('given_name')
        user_data['last_name'] = user_data.get('family_name')
        return user_data
