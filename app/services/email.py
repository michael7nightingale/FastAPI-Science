from smtplib import SMTP_SSL
from app.core.config import get_app_settings
from app.services.token import generate_token


def create_server() -> SMTP_SSL:
    settings = get_app_settings()
    server_ = SMTP_SSL(
        port=settings.EMAIL_PORT,
        host=settings.EMAIL_HOST
    )
    server_.ehlo()
    server_.login(
        user=settings.EMAIL_USER,
        password=settings.EMAIL_PASSWORD
    )
    return server_


smtp_server = create_server()


def send_message(subject: str, to_addrs: list, body: str) -> None:
    email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (get_app_settings().EMAIL_USER, ", ".join(to_addrs), subject, body)
    smtp_server.sendmail(
        from_addr="suslanchikmopl@gmail.com",
        to_addrs=to_addrs,
        msg=email_text
    )
