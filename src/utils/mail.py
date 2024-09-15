import smtplib

from email.mime.text import MIMEText

from core.settings import settings


class Mail:

    def __init__(
        self,
        host: str = settings.email.HOST,
        host_user: str = settings.email.USER,
        port: int = settings.email.PORT,
        password: str = settings.email.PASSWORD,
    ):
        self.host = host
        self.host_user = host_user
        self.port = port
        self.password = password

    def send_email(self, email: str, message: str):
        """Функция для отправки письма"""
        new_message = MIMEText(message)  # type: ignore
        new_message["Subject"] = "Service itjob"
        new_message["From"] = self.host_user
        new_message["To"] = email
        with smtplib.SMTP_SSL(self.host, self.port) as server:
            server.login(self.host_user, self.password)
            server.sendmail(self.host_user, email, new_message.as_string())
