#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler

import util.json


class Prueba:

    def __init__(self):
        self.saludo = 'holáááááá'
        self.despedida = 'adióóóóóó'


class UsuarioHandler(BaseHandler):

    def get(self):
        diccionario = {'clave1':'valorClave1', 'clave2':'ValorClave2'}
        prueba = Prueba()

        self.response.write(util.json.to_json(prueba))
