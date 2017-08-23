import tornado.web

from app.handlers import mail


url = tornado.web.URLSpec

urls = (
    url(r'/mail', mail.MailHandler, name='mail'),
)