#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler
from google.appengine.ext import ndb
from util.json import to_json
from tokens import get_user_from_token
from models import Categoria
from facades import categoria as cat

class CategoriaHandler(BaseHandler):
    def get(self,categoria_key):
        categoria = ndb.Key(urlsafe=categoria_key).get()
        categoria_mostrada = {'id': categoria.key.urlsafe(), 'nombre': categoria.nombre}
        self.response.write(to_json(categoria_mostrada))


class CategoriasHandler(BaseHandler):
    def get(self):
        categorias = []
        for categoria in Categoria.query().fetch():
            categoria_nueva = {'id':categoria.key.urlsafe(),'nombre':categoria.nombre}
            categorias.append(categoria_nueva)
        self.response.write(to_json(categorias))


class PreferenciasHandler(BaseHandler):
    def get(self):
        _, usuario_sesion = get_user_from_token(self.request.headers.get('bearer'))
        categorias = []
        for categoria in cat.buscar_preferencias_usuario(usuario_sesion):
            categoria_nueva = {'id':categoria.key.urlsafe(),'nombre':categoria.nombre}
            categorias.append(categoria_nueva)
        self.response.write(to_json(categorias))