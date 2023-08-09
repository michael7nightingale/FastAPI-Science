from itsdangerous import URLSafeTimedSerializer

from src.core.config import get_app_settings


def generate_token(email, secret_key: str | None = None):
    if secret_key is None:
        secret_key = get_app_settings().SECRET_KEY
    serializer = URLSafeTimedSerializer(secret_key=secret_key)
    return serializer.dumps(email)


def confirm_token(token, expiration: int = 3600, secret_key: str | None = None):
    if secret_key is None:
        secret_key = get_app_settings().SECRET_KEY
    serializer = URLSafeTimedSerializer(secret_key=secret_key)
    try:
        email = serializer.loads(
            token, max_age=expiration
        )
        return email
    except Exception:
        return False


def generate_activation_link(request, user) -> str:
    token = generate_token(user.email)
    url = request.app.url_path_for("activate_user", uuid=user.id, token=token)
    # host = request.client.host
    host = "http://127.0.0.1:8000"
    return host + url
