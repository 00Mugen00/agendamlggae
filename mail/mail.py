# -*- coding: utf-8 -*-

from google.appengine.api import mail

#documentación: https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.api.mail#google.appengine.api.mail.EmailMessage
def send_mail(to,subject,msg):
    if to:
        try:
            message = mail.EmailMessage()
            # Este método de momento no va a funcionar porque sender tiene que ser el usuario que sube el proyecto
            # Consulte la siguiente página para más info: https://cloud.google.com/appengine/docs/standard/python/mail/
            message.sender = 'xagendamlg@gmail.com'
            message.to = to
            message.subject = subject
            message.body = msg
            # chech_initialized asegura que los destinatarios han sido especificados
            message.check_initialized()
            message.send()
        except mail.MissingRecipientError:
            print 'Los destinatarios no han sido especificados'