#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib2
import webapp2
from webapp2_extras import routes
from apiclient.discovery import build
from google.appengine.api import memcache

import handlers
import tokens

API_BASE_URL = '/agendamlg-api'

API_ENTITIES_ROUTES = {'Categoria': '/categoria',
                       'Usuario': '/usuario',
                       'Evento': '/evento'
                       }

OAuthLogin, OAuthTest = handlers.based_on(tokens.google_oauth_decorator,
                                          build("plus", "v1", http=httplib2.Http(memcache)))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(u"""Henlo friend. I see u come h3re and here is the base api handler,
        have a nice day :)
        """)


app = webapp2.WSGIApplication([
    routes.PathPrefixRoute(API_BASE_URL, [
        webapp2.Route(r'/', MainHandler),
        routes.PathPrefixRoute(API_ENTITIES_ROUTES['Categoria'], [
            webapp2.Route(r'/', handlers.CategoriaHandler)
        ]),
        routes.PathPrefixRoute(API_ENTITIES_ROUTES['Usuario'], [
            webapp2.Route(r'/', handlers.UsuarioHandler)
        ]),
        routes.PathPrefixRoute(API_ENTITIES_ROUTES['Evento'], [
            webapp2.Route(r'/', handlers.EventoHandler),
            webapp2.Route(r'/filtrar', handlers.FiltradoHandler)
        ]),
        routes.PathPrefixRoute(r'/seed', [
            webapp2.Route(r'/', handlers.SeedHandler)
        ]),
        routes.PathPrefixRoute(r'/oauth', [
            webapp2.Route(r'/', OAuthTest),
            webapp2.Route(r'/login', OAuthLogin)
        ])
    ]),
    webapp2.Route(tokens.google_oauth_decorator.callback_path, tokens.google_oauth_decorator.callback_handler())
], debug=True)
