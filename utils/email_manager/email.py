import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader

from core.config import settings


env = Environment(
    loader=FileSystemLoader("templates")
)

SMTP_SERVER = settings.EMAIL_HOST
SMTP_PORT = settings.EMAIL_PORT

SENDER_EMAIL = settings.EMAIL_FROM
SENDER_PASSWORD = settings.EMAIL_PASSWORD


def render_template(template_name: str, context: dict) -> str:
    template = env.get_template(template_name)
    return template.render(context)


def send_email(to_email: str, subject: str, template_name: str, context: dict):

    html_content = render_template(template_name, context)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()

        return True

    except Exception as e:
        print("Error sending email:", e)
        return False