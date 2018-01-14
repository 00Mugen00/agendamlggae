#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util.json
from base import BaseHandler
from facades.evento import buscar_evento_categorias
from models import Usuario

class FiltradoHandler(BaseHandler):

    def get(self):
        self.response.write('Handler filtrado evento')

    def post(self):

        filtrado = self.request.GET

        recibido = self.request.body
        # json = util.json.from_json(recibido)

        # Obtener usuario de antonio
        query = Usuario.query(Usuario.idGoogle == '101525104652157188456')
        usuario = query.fetch()

        eventos = buscar_evento_categorias(usuario[0],**filtrado)

        retorno = [ {'descripcion': evento.descripcion,
                     'direccion': evento.direccion,
                     'fecha': evento.fecha.isoformat(),
                     'latitud': evento.coordenadas.lat if evento.coordenadas else None,
                     'longitud': evento.coordenadas.lon if evento.coordenadas else None,
                     'nombre': evento.nombre,
                     'precio': evento.precio,
                     'id': evento.key.id()} for evento in eventos]

        self.response.write(util.json.to_json(retorno))

