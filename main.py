#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
from webapp2_extras import routes

from handlers import *

API_BASE_URL = '/agendamlg-api'

API_ENTITIES_ROUTES = {'Categoria': '/categoria',
                       'Usuario': '/usuario',
                       'Evento': '/evento'
                       }


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("""Henlo friend. I see u come h3re and here is the base api handler,
        have a nice day :)
        """)


app = webapp2.WSGIApplication([
    routes.PathPrefixRoute(API_BASE_URL, [
        webapp2.Route(r'/', MainHandler),
        routes.PathPrefixRoute(API_ENTITIES_ROUTES['Categoria'], [
            webapp2.Route(r'/', CategoriaHandler)
        ]),
        routes.PathPrefixRoute(API_ENTITIES_ROUTES['Usuario'], [
            webapp2.Route(r'/', UsuarioHandler)
        ]),
        routes.PathPrefixRoute(API_ENTITIES_ROUTES['Evento'], [
            webapp2.Route(r'/', EventoHandler)
        ]),
    ]),
], debug=True)
