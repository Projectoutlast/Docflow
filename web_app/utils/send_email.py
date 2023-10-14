import html

from flask_mail import Message
from web_app import mail

from config import Config


def send_email(to: str, subject: str, template: html):
    msg = Message(subject, recipients=[to], html=template, sender=Config.MAIL_USERNAME)
    mail.send(msg)
