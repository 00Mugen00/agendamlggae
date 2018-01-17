#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler
from facades.evento import buscar_eventos_usuario
from salida_eventos_json import eventos_json
from tokens import get_user_from_token


class MisEventos(BaseHandler):

    def get(self):
        # Obtener usuario para mostrar eventos validados o no
        _, usuario = get_user_from_token(self.request.headers.get('bearer'), raise_for_unauthenticated=True)

        # Usuario para la id de Google proporcionada
        # Si hay una excepcion es que no se ha encontrado el usuario

        eventosUsuario = buscar_eventos_usuario(usuario, True)

        self.response.write(eventos_json(eventosUsuario, True))
