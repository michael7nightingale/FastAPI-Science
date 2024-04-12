from email.message import EmailMessage

from src.core.worker import app
from ...core.config import get_app_settings
from ...services.email import EmailServer


@app.task
def send_email_task(subject: str, to_addrs: list[str], body: str) -> int:
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = get_app_settings().EMAIL_USER
    msg['To'] = ','.join(to_addrs)
    msg.set_content(body, subtype="html")
    with EmailServer() as email_server:
        return email_server.send_email(
            to_addrs=to_addrs,
            msg=msg
        )
