#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util.json
from base import BaseHandler
from facades.evento import buscar_evento_categorias
from models import Usuario, agenda_key
from tokens import get_user_from_token
from google.appengine.ext import ndb


class FiltradoHandler(BaseHandler):

    def get(self):
        filtrado = self.request.GET
        categorias = self.request.get_all('categorias')


        # Si el usuario no esta autenticado no se lanza excepcion, de ahi el False
        # La barra baja indica que no se interesa asignar esa parte de la tupla
        _, usuario = get_user_from_token(self.request.headers.get('bearer'), raise_for_unauthenticated=False)

        if usuario and self.request.get('mostrarDeMiPreferencia'):
            # La lista de categorias se rellena en base a las preferencias del usuario
            filtrado['categorias'] = usuario.preferencias

        else:
            # El metodo de la fachada espera recibir una lista de claves de categoria, por la URL
            # se va a pasar el id de categoria
            filtrado['categorias'] = [ndb.Key('Categoria', categoria_id, parent=agenda_key()) for categoria_id in categorias]

        # Se procede a obtener la lista de resultados

        eventos = buscar_evento_categorias(usuario, **filtrado)

        retorno = [{'descripcion': evento.descripcion,
                    'direccion': evento.direccion,
                    'fecha': evento.fecha.isoformat(),
                    'latitud': evento.coordenadas.lat if evento.coordenadas else None,
                    'longitud': evento.coordenadas.lon if evento.coordenadas else None,
                    'nombre': evento.nombre,
                    'precio': evento.precio,
                    'id': evento.key.id()} for evento in eventos]

        self.response.write(util.json.to_json(retorno))


