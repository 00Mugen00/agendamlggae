#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler
from models import Usuario
from tokens import get_user_from_token
from util.json import to_json


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
