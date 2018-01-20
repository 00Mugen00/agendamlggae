#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util.json
from base import BaseHandler
from facades.evento import buscar_evento_categorias
from models import agenda_key
from tokens import get_user_from_token
from google.appengine.ext import ndb
from salida_eventos_json import eventos_json


class FiltradoHandler(BaseHandler):

    def get(self):
        filtrado = self.request.GET
        # Lista de claves de categorias en URLSafe
        categorias = self.request.get_all('categoriasSeleccionadas')

        # Si el usuario no esta autenticado no se lanza excepcion, de ahi el False
        # La barra baja indica que no se interesa asignar esa parte de la tupla
        _, usuario = get_user_from_token(self.request.headers.get('bearer'), raise_for_unauthenticated=False)

        if usuario and self.request.get('mostrarDeMiPreferencia', '') == 'true':
            # La lista de categorias se rellena en base a las preferencias del usuario
            filtrado['categorias'] = usuario.preferencias

        else:
            # El metodo de la fachada espera recibir una lista de claves de categoria, por la URL
            # se va a pasar la clave de categoria como urlSafe
            filtrado['categorias'] = [ndb.Key(urlsafe=categoria_clave) for categoria_clave in
                                      categorias]

        # Se procede a obtener la lista de resultados

        eventos = buscar_evento_categorias(usuario, **filtrado)

        self.response.write(eventos_json(eventos))
