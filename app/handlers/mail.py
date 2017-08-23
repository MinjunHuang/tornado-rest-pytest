import json
import tornado.auth
import tornado.gen
import tornado.httpclient

from app.handlers.base import RequestHandler
from app.storage import db


class MailHandler(RequestHandler):
    @property
    def noise_remove(self, body):
        stop_words = ('a', 'then', 'an', 'and', 'so', 'then')
        words = body.split()
        result = (' ').join([word for word in words if word.lower() not in stop_words])
        return result

    @property
    def compare_mail_body(self, body_one, body_two):
        if body_one.split()[:10] == body_two.split()[:10]:
            return True
        else:
            return False

    def post(self):
        print("entramos al metodo post")
        import pdb; pdb.set_trace()
        id_one = self.get_argument('email_id_one')
        id_two = self.get_argument('email_id_two')        
        if any(x == None for x in (id_one, id_two)):
            self.set_status(400)
            error_message = "Missing one or more parameters."
            self.finish(error_message)
        cursor = self.db()
        mails = []
        for id in (id_one, id_two):
            mail = cursor.query(EmailEmail).filter(EmailEmail.pk == id).first()
            mails.append(mail)
        if len(mails) < 2:
            self.set_status(500)
            error_message = "Email(s) doesn't exist"
            self.finish(error_message)
        
        cln_bd_one = self.noise_remove(mails[0].body)
        cln_by_two = self.noise_remove(mails[1].body)
        if self.compare_mail_body(cln_bd_one, cln_by_two):
            result = [{'response': 'Emails are equal'}]
        else:
            result = [{'response': 'Emails are different'}]

        self.write(json_encode(result))     
   