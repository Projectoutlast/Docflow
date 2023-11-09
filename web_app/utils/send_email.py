import html

from flask import render_template, url_for
from flask_mail import Message
from web_app import mail

from config import Config
from web_app.utils.token import generate_token


def send_email(to: str, subject: str, template: html):
    msg = Message(subject, recipients=[to], html=template, sender=Config.MAIL_USERNAME)
    mail.send(msg)


def generate_and_send_confirmation_token(email: str) -> None:
    token = generate_token(email)
    confirm_url = url_for("registration.confirm_email", token=token, _external=True)
    render_html = render_template("confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(email, subject, render_html)
    return
