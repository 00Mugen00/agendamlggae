#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util.json
from base import BaseHandler
from facades.evento import evento_corto, buscar_eventos_usuario
from facades.excepcion import AgendamlgNotFoundException
from models import Usuario
from tokens import get_user_from_token
from salida_eventos_json import eventos_json


class EventosUsuario(BaseHandler):

    def get(self, idGoogle):
        # Obtener usuario para mostrar eventos validados o no
        _, usuario = get_user_from_token(self.request.headers.get('bearer'), raise_for_unauthenticated=False)

        # Usuario para la id de Google proporcionada
        # Si hay una excepsion es que no se ha encontrado el usuario

        otro_usuario = None

        try:
            otro_usuario = Usuario.query(Usuario.idGoogle == idGoogle).fetch()[0]
        except:
            raise AgendamlgNotFoundException.usuario_no_existe(idGoogle)

        mostrarTodos = False

        # Si quiero ver mis eventos o bien se es periodista, se muestran todos
        if usuario is not None and (usuario.tipo == 3 or usuario.idGoogle == otro_usuario.idGoogle):
            mostrarTodos = True

        eventosUsuario = buscar_eventos_usuario(otro_usuario, mostrarTodos)

        self.response.write(eventos_json(eventosUsuario))
