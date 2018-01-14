#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler
import util.json
from google.appengine.ext import ndb
from facades import buscar_evento_categorias

from models import Usuario


class FiltradoHandler(BaseHandler):

    def get(self):
        self.response.write('Handler filtrado evento')

    def post(self):
        recibido = self.request.body
        json = util.json.from_json(recibido)

        # Obtener usuario de antonio
        query = Usuario.query(Usuario.idGoogle == '101525104652157188456')
        usuario = query.fetch()

        eventos = buscar_evento_categorias(usuario[0], **json)

        self.response.write(util.json.to_json(eventos))



