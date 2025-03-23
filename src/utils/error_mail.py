import os
import smtplib

# 文字コードを調整
from email import policy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils import environment


# リクエストエラーが発生した際にメールを送る
def request_error_mail(error_point: str, status_code: int) -> None:
    message = f"スクレイピングプログラムの {error_point} において、リクエスト時にエラーが発生した可能性があります。HTTPステータスコードは{status_code}です。"
    send_mail(message)


def send_mail(mess: str) -> None:
    # SMTPサーバーに接続
    smtp_server = "smtp.gmail.com"
    port = 587
    server = smtplib.SMTP(smtp_server, port)

    # 暗号化
    server.starttls()

    if environment == "local":
        import main_local

        login_address = main_local.mail_address
        login_password = main_local.gmail_password
    else:
        login_address = os.environ.get("MailAddress")
        login_password = os.environ.get("MailPass")
    server.login(login_address, login_password)

    message = MIMEMultipart(policy=policy.default)
    message["Subject"] = "ラノベスクレイピングでのエラーの可能性"
    message["From"] = "スクレイピング"
    message["To"] = login_address
    text = MIMEText(mess)

    message.attach(text)
    server.send_message(message)

    server.quit()
