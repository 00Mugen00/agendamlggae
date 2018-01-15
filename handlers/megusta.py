# -*- coding: utf-8 -*-

from google.appengine.ext.ndb import Key
from facades import megusta, AgendamlgNotFoundException
from handlers.base import BaseHandler
from tokens import get_user_from_token


class MeGustaHandler(BaseHandler):
    def put(self, eid):
        _, usuario_sesion = get_user_from_token(self.request.headers.get('bearer'))
        evento = MeGustaHandler.__evento_o_fallo(eid)
        megusta.crear_me_gusta(usuario_sesion, evento)
        self.response.write(u'{"me_gusta": true}')

    def delete(self, eid):
        _, usuario_sesion = get_user_from_token(self.request.headers.get('bearer'))
        evento = MeGustaHandler.__evento_o_fallo(eid)
        megusta.eliminar_me_gusta(usuario_sesion, evento)
        self.response.write(u'{"deleted": true}')

    @staticmethod
    def __evento_o_fallo(eid):
        try:
            k = Key(urlsafe=(eid if '/' not in eid else eid[0:-1]))
            if not k.get():
                raise AgendamlgNotFoundException.evento_no_existe(eid)
            return k
        except Exception:
            raise AgendamlgNotFoundException.evento_no_existe(eid)
