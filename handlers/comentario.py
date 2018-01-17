# -*- coding: utf-8 -*-

from google.appengine.ext.ndb import Key
from facades import comentario, AgendamlgNotFoundException
from handlers.base import BaseHandler
from tokens import get_user_from_token
from util import to_json, from_json


class ComentarioHandler(BaseHandler):
    def get(self, eid):
        _, usuario_sesion = get_user_from_token(self.request.headers.get('bearer'), raise_for_unauthenticated=False)
        evento = ComentarioHandler.__evento_o_fallo(eid)
        comentarios = comentario.buscar_comentarios_evento(usuario_sesion, evento)
        self.response.write(ComentarioHandler.__comentarios_a_json(comentarios))

    def put(self, eid):
        _, usuario_sesion = get_user_from_token(self.request.headers.get('bearer'))
        nuevo_comentario = self.json_body()
        evento = ComentarioHandler.__evento_o_fallo(eid)
        comentarios = comentario.crear_comentario(usuario_sesion, evento, nuevo_comentario)
        self.response.write(ComentarioHandler.__comentarios_a_json([ comentarios ]))

    def delete(self, eid):
        _, usuario_sesion = get_user_from_token(self.request.headers.get('bearer'))
        evento = ComentarioHandler.__evento_o_fallo(eid)
        comentario.eliminar_comentario(usuario_sesion, evento)
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

    @staticmethod
    def __comentarios_a_json(comentarios):
        def creador(usuario_key):
            usuario = usuario_key.get()
            usuario_info = from_json(usuario.extra)
            return {
                u'id': usuario.idGoogle,
                u'nombre': usuario_info[u'displayName'],
                u'image': usuario_info[u'image'][u'url'][0:-6]
            }

        return to_json([ {u'texto': c.texto,
                          u'fecha': c.fecha.isoformat(),
                          u'creador': creador(c.creador),
                          u'id': c.key.urlsafe()}
                         for c in comentarios ])
