from smtplib import SMTP_SSL
from src.core.config import get_app_settings


class SMTPServer(SMTP_SSL):

    def __init__(self, host: str, port: int, from_addr: str, *args, **kwargs):
        super().__init__(host, port, *args, **kwargs)
        self._from_addr = from_addr

    def send_message(self, subject: str, to_addrs: list, body: str) -> None:
        email_text = """\
            From: %s
            To: %s
            Subject: %s

            %s
            """ % (self._from_addr, ", ".join(to_addrs), subject, body)
        super().sendmail(
            from_addr="suslanchikmopl@gmail.com",
            to_addrs=to_addrs,
            msg=email_text
        )


def create_server() -> SMTPServer:
    settings = get_app_settings()
    server_ = SMTPServer(
        port=settings.EMAIL_PORT,
        host=settings.EMAIL_HOST,
        from_addr=settings.EMAIL_USER,
    )
    server_.ehlo()
    server_.login(
        user=settings.EMAIL_USER,
        password=settings.EMAIL_PASSWORD
    )
    return server_


class EmailService:

    def __init__(self, smtp_server: SMTPServer):
        self._smtp_server = smtp_server

    def send_activation_email(self, name, email, link):
        message = "%s, please follow the link ro finish the registration: %s" % (name, link)
        self._smtp_server.send_message(
            subject="Registration",
            to_addrs=[email],
            body=message
        )
