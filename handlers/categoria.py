#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler
from google.appengine.ext import ndb
from util.json import to_json
from tokens import get_user_from_token
from models import Categoria
from facades import categoria as cat
from facades import AgendamlgNotFoundException

class CategoriaHandler(BaseHandler):
    def get(self, categoria_key):
        try:
            categoria = ndb.Key(urlsafe=categoria_key).get()
            if not categoria:
                raise AgendamlgNotFoundException.categoria_no_existe(categoria_key)
            categoria_mostrada = {'id': categoria.key.urlsafe(), 'nombre': categoria.nombre}
            self.response.write(to_json(categoria_mostrada))
        except Exception:
            raise AgendamlgNotFoundException.categoria_no_existe(categoria_key)


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

    def delete(self,categoria_key):
        _, usuario_sesion = get_user_from_token(self.request.headers.get('bearer'))
        try:
            k = ndb.Key(urlsafe=categoria_key)
            if not k.get():
                raise AgendamlgNotFoundException.categoria_no_existe(categoria_key)
            cat.eliminar_preferencia_usuario(usuario_sesion, k)
            self.response.write(u'{"deleted": true}')
        except Exception:
            raise AgendamlgNotFoundException.categoria_no_existe(categoria_key)

    def post(self):
        _, usuario_sesion = get_user_from_token(self.request.headers.get('bearer'))
        categoria_nueva = self.json_body()
        cat.agregar_preferencia_usuario(usuario_sesion, ndb.Key(urlsafe=categoria_nueva.get('id')))
        categorias = []
        for categoria in cat.buscar_preferencias_usuario(usuario_sesion):
            categoria_nueva = {'id':categoria.key.urlsafe(),'nombre':categoria.nombre}
            categorias.append(categoria_nueva)
        self.response.write(to_json(categorias))