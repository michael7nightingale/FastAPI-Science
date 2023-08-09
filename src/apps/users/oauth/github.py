import requests

from .base import BaseProvider


class GithubOAuthProvider(BaseProvider):
    __slots__ = ()
    name = "github"

    def get_access_token(self) -> str | None:
        url = "https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}".format(
            client_secret=self.client_secret,
            client_id=self.client_id,
            code=self.code
        )
        response = requests.post(url)
        if not response:
            return
        access_token = response.text.split('=')[1].split("&")[0]
        return access_token

    def get_user_data(self, access_token: str) -> dict | None:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://api.github.com/user", headers=headers)
        if not response:
            return
        return response.json()

    def get_user_email(self, access_token: str) -> str | None:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://api.github.com/user/emails", headers=headers)
        if not response:
            return
        user_email_data = response.json()
        email = None
        if isinstance(user_email_data, dict):
            email = user_email_data['email']
        else:
            for email_data in user_email_data:
                if email_data['primary']:
                    email = email_data['email']
                    break
            if email is None and user_email_data:
                email = email_data[0]['email']
        return email

    def provide(self) -> dict | None:
        access_token = self.get_access_token()
        if access_token is None:
            return
        user_data = self.get_user_data(access_token)
        if user_data is None:
            return
        user_data['username'] = user_data.pop('login')
        email = self.get_user_email(access_token)
        if email is None:
            return
        user_data['email'] = email
        return user_data
