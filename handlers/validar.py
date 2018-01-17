#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util.json
from base import BaseHandler
from facades.evento import validar_evento, evento_corto_clave, clave_evento_o_fallo
from models import Usuario, agenda_key
from tokens import get_user_from_token
from google.appengine.ext import ndb
from facades.excepcion import AgendamlgException, AgendamlgNotFoundException

class ValidacionHandler(BaseHandler):


    def put(self):
        """
        Se necesita autenticacion y es por ello que se lanza la excepcion si no hay usuario autenticado
        :param self:
        :return:
        """
        _, usuario = get_user_from_token(self.request.headers.get('bearer'), raise_for_unauthenticated=True)
        # Solo un usuario tipo 3 puede puede validar eventos
        if usuario.tipo != 3:
            raise AgendamlgException.sin_permisos(usuario)

        # Se espera recibir un json de la forma {"id":"idEvento"}
        contenido_json = self.json_body()

        if contenido_json.get('id', None) is None:
            raise AgendamlgNotFoundException.evento_no_existe(None)

        # Si tiene id y demas se procede a su validacion
        validar_evento(contenido_json['id'])

        self.response.write(util.json.to_json(evento_corto_clave(clave_evento_o_fallo(contenido_json['id']))))