import requests


class GithubOAuthProvider:
    __slots__ = ("client_id", "client_secret", "code", "token_headers")

    def __init__(self, client_id: str, client_secret: str, code: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code

    def set_access_headers(self) -> str | None:
        url = "https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}".format(
            client_secret=self.client_secret,
            client_id=self.client_id,
            code=self.code
        )
        response = requests.post(url)
        if not response:
            return
        access_token = response.text.split('=')[1].split("&")[0]
        self.token_headers = {"Authorization": f"Bearer {access_token}"}
        return access_token

    def get_user_data(self) -> dict | None:
        response = requests.get("https://api.github.com/user", headers=self.token_headers)
        if not response:
            return
        return response.json()

    def get_user_email(self) -> str | None:
        response = requests.get("https://api.github.com/user/emails", headers=self.token_headers)
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
            if email is None and email_data:
                email = email_data[0]['email']
        return email

    def __call__(self) -> dict | None:
        access_token = self.set_access_headers()
        if access_token is None:
            return
        user_data = self.get_user_data()
        user_data['username'] = user_data.pop('login')
        if user_data is None:
            return
        email = self.get_user_email()
        if email is None:
            return
        user_data['email'] = email
        return user_data
