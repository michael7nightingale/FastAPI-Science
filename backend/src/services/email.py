import datetime
from smtplib import SMTP_SSL
from src.services.token import generate_activation_code


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


def create_server(host: str, port: int, user: str, password: str) -> SMTPServer:
    server_ = SMTPServer(
        port=port,
        host=host,
        from_addr=user,
    )
    # server_.ehlo()
    # server_.login(
    #     user=user,
    #     password=password
    # )
    return server_


class EmailService:

    def __init__(self, smtp_server: SMTPServer):
        self._smtp_server = smtp_server

    def send_activation_email(self, name, email):
        code = generate_activation_code(length=6)
        cache_data = {  # noqa: F841
            "email": email,
            "code": code,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=30)
        }
        message = "%s, вот ваш код для завершения регистрации: %s" % (name, code)
        self._smtp_server.send_message(
            subject="Registration",
            to_addrs=[email],
            body=message
        )
