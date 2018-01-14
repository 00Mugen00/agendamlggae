#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler
from facades import AgendamlgException, AgendamlgNotFoundException
from models import Usuario
from tokens import get_user_from_token
from util.json import to_json, from_json


def usuario_a_json(tup):
    # type: ((dict, Usuario)) -> unicode
    info, user = tup
    return to_json({
        u'id': info[u'id'],
        u'tipo': user.tipo,
        u'nombre': info[u'name'][u'givenName'],
        u'apellidos': info[u'name'][u'familyName'],
        u'email': info[u'emails'][0][u'value'],
        u'image': info[u'image'][u'url'][0:-6]  # Eliminar ?sz=50
    })


class UsuarioHandler(BaseHandler):

    def get(self):
        self.response.write(usuario_a_json(get_user_from_token(self.request.headers.get('bearer'))))


class UsuarioEspecificoHandler(BaseHandler):
    def get(self, uid):
        usuario = Usuario.query(Usuario.idGoogle == uid).fetch()
        if not usuario:
            raise AgendamlgNotFoundException.usuario_no_existe(uid)
        else:
            self.response.write(usuario_a_json((from_json(usuario[0].extra), usuario[0])))

    def delete(self, uid):
        _, usuario_sesion = get_user_from_token(self.request.headers.get('bearer'))
        usuario = Usuario.query(Usuario.idGoogle == uid).fetch()
        if not usuario:
            raise AgendamlgNotFoundException.usuario_no_existe(uid)
        if usuario_sesion.tipo != 3 or usuario_sesion.key == usuario.key:
            raise AgendamlgException.sin_permisos(usuario_sesion.idGoogle)
        usuario[0].key.remove()
        self.response.write(u'{"status": "ok"}')

    def put(self, uid):
        _, usuario_sesion = get_user_from_token(self.request.headers.get('bearer'))
        usuario = Usuario.query(Usuario.idGoogle == uid).fetch()
        if not usuario:
            raise AgendamlgNotFoundException.usuario_no_existe(uid)
        else:
            usuario = usuario[0]
        if usuario_sesion.tipo != 3 or usuario_sesion.key == usuario.key:
            raise AgendamlgException.sin_permisos(usuario_sesion.idGoogle)

        nueva_info = self.json_body()
        nuevo_tipo = int(nueva_info.get(u'tipo', usuario.tipo))
        if nuevo_tipo == 0 or nuevo_tipo > 3:
            raise AgendamlgException.evento_campos_invalidos()

        usuario.tipo = nuevo_tipo
        usuario.put()
        self.response.write(usuario_a_json((from_json(usuario.extra), usuario)))
