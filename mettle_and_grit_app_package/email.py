from flask_mail import Message
from mettle_and_grit_app_package import mg_app_object, mail
from threading import Thread
from flask import render_template

def send_async_email(app, msg):
    with mg_app_object.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(mg_app_object, msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Mettle and Grit] Password Reset',
               sender=mg_app_object.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(mg_app_object, msg)).start()
