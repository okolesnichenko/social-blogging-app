from flask_mail import Message
from threading import Thread
from flask import render_template
from flask import current_app
from manage import app
from app import mail
'''
Это расширение обеспечивает возможность соединения с SMTP-
сервером (Simple Mail Transfer Protocol – простой протокол переда-
чи электронной почты) и передачи ему электронных писем для рас-
сылки. По умолчанию Flask-Mail пытается соединиться с портом 25
сервера localhost и отправить почту без аутентификации. В табл. 6.1
приводится список ключей параметров настройки соединения
с SMTP-сервером.
'''


# Отправка ассинхорнного сообщения
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# Отправка ассинхорнного сообщения
def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr