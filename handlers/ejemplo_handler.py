#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Handler de ejemplo,
Es un modelo para hacer handlers necesarios en la aplicacion,
una vez hecho para exportarlo para su uso en main.py
simplemente añadir a __init__.py:
from ejemplo_handler import *
"""

from base_handler import BaseHandler

import util.json


# Ejemplo que serializa un bjeto y lo devuelve como JSON

class Prueba:

    def __init__(self):
        self.saludo = 'holáááááá'
        self.despedida = 'adióóóóóó'

class EjemploHandler(BaseHandler):

    def get(self):
        diccionario = {'clave1':'valorClave1', 'clave2':'ValorClave2'}
        prueba = Prueba()

        self.response.write(util.json.to_json(prueba))
