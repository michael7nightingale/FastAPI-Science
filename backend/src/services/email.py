from smtplib import SMTP_SSL, _fix_eols

from src.core.config import get_app_settings


class SMTPServer(SMTP_SSL):

    def __init__(self, host: str, port: int, from_addr: str, *args, **kwargs):
        super().__init__(host, port, *args, **kwargs)
        self._from_addr = from_addr

    def send_message(self, subject: str, to_addrs: list, body: str) -> None:
        email_text = f"""\
            From: {self._from_addr}
            To: {", ".join(to_addrs)}
            Subject: {subject}

            {body}
            """
        super().sendmail(
            from_addr="suslanchikmopl@gmail.com",
            to_addrs=to_addrs,
            msg=_fix_eols(email_text).encode('utf-8')
        )


def create_smtp_server(
        host: str = get_app_settings().EMAIL_HOST,
        port: int = get_app_settings().EMAIL_PORT,
        user: str = get_app_settings().EMAIL_USER,
        password: str = get_app_settings().EMAIL_PASSWORD
) -> SMTPServer:
    server_ = SMTPServer(
        port=port,
        host=host,
        from_addr=user,
    )
    server_.ehlo()
    server_.login(
        user=user,
        password=password
    )
    return server_
