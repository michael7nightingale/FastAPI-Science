from email.message import EmailMessage
from smtplib import SMTP_SSL

from src.core.config import get_app_settings


class EmailServer:

    def __init__(self):
        self.settings = get_app_settings()
        self.smtp_server = SMTP_SSL(port=self.settings.EMAIL_PORT, host=self.settings.EMAIL_HOST)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        self.smtp_server.ehlo()
        self.smtp_server.login(user=self.settings.EMAIL_USER, password=self.settings.EMAIL_PASSWORD)

    def disconnect(self):
        self.smtp_server.close()

    def send_email(self, to_addrs: list[str], msg: EmailMessage):
        self.smtp_server.sendmail(
            from_addr=self.settings.EMAIL_USER,
            to_addrs=to_addrs,
            msg=msg.as_string()
        )


def build_activation_email(activation_code: str) -> str:
    return f"<h1>Activation code: {activation_code}</h1>"
