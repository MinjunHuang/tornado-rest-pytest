import json
import tornado.auth
import tornado.gen
import tornado.httpclient

from app.handlers.base import RequestHandler
from app.storage.db import EmailEmail, ArchiveEmail


class MailHandler(RequestHandler):
    @staticmethod
    def noise_remove(body):
        stop_words = ('a', 'then', 'an', 'and', 'so', 'then')
        words = body.split()
        result = (' ').join([word for word in words if word.lower() not in stop_words])
        return result

    @staticmethod
    def compare_mail_body(body_one, body_two):
        if body_one.split()[:10] == body_two.split()[:10]:
            return True
        else:
            return False

    @staticmethod
    def compare_mail_subject(subject_one, subject_two):
        if subject_one.split()[:3] == subject_two.split()[:3]:
            return True
        else:
            return False

    def post(self):
        try:
            id_one = int(self.get_argument('email_id_one'))
            id_two = int(self.get_argument('email_id_two'))        
            if any(x == None for x in (id_one, id_two)):
                self.set_status(400)
                error_message = "Missing one or more parameters."
                self.finish(error_message)
            cursor = self.db()
            mails = []
            # get emails from EmailEmail
            for id in (id_one, id_two):
                mail = cursor.query(EmailEmail).filter(EmailEmail.id == id).first()
                mails.append(mail)
             
            cln_bd_one = self.noise_remove(mails[0].body)
            cln_bd_two = self.noise_remove(mails[1].body)
            sbj_one = mails[0].subject
            sbj_two = mails[1].subject

            if self.compare_mail_body(cln_bd_one, cln_bd_two) and self.compare_mail_subject(sbj_one, sbj_two):
                archive = ArchiveEmail(email_id=id_one, bury_email_id=id_two)
                cursor.add(archive)
                cursor.commit()
                self.set_status(201)
                message = "Emails were archived"
                self.finish(message)
            else:
                self.set_status(201)
                message = "Emails are not related"
                self.finish(message)
        except:
            self.set_status(400)
            message = "Something goes wrong"
            self.finish(message)
