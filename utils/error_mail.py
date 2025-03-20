import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText

#文字コードを調整
from email import policy
import main_local

# リクエストエラーが発生した際にメールを送る
def request_error_mail(error_point, status_code):
    message = (
        "スクレイピングプログラムの"
        + error_point
        + "でリクエスト時にエラーが発生した可能性があります。HTTPステータスコードは"
        + str(status_code)
        + "です。"
    )
    send_mail(message)

def send_mail(mess):
    #SMTPサーバーに接続
    smtp_server = "smtp.gmail.com"
    port = 587
    server = smtplib.SMTP(smtp_server, port)

    #暗号化
    server.starttls()

    login_address = main_local.mail_address
    login_password = main_local.gmail_password
    server.login(login_address, login_password)

    message = MIMEMultipart(policy=policy.default)
    message["Subject"] = "ラノベスクレイピングでのエラーの可能性"
    message["From"] = "スクレイピング"
    message["To"] = main_local.mail_address
    text = MIMEText(mess)

    message.attach(text)
    server.send_message(message)

    server.quit()
