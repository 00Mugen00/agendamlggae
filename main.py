#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib2
import webapp2
from webapp2_extras import routes
from apiclient.discovery import build
from google.appengine.api import memcache

import handlers
import tokens

OAuthLogin, OAuthTest = handlers.based_on(tokens.google_oauth_decorator,
                                          build("plus", "v1", http=httplib2.Http(memcache)))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(u"""Henlo friend. I see u come h3re and here is the base api handler,
        have a nice day :)
        """)


app = webapp2.WSGIApplication([
    routes.PathPrefixRoute('/agendamlg-api', [
        webapp2.Route(r'/', MainHandler),
        routes.PathPrefixRoute(r'/categoria', [
            webapp2.Route(r'/', handlers.CategoriaHandler)
        ]),
        routes.PathPrefixRoute(r'/usuario', [
            webapp2.Route(r'/', handlers.UsuarioHandler),
            webapp2.Route(r'/<uid:\d+>', handlers.UsuarioEspecificoHandler)
        ]),
        routes.PathPrefixRoute(r'/evento', [
            webapp2.Route(r'/', handlers.EventoHandler),
            webapp2.Route(r'/filtrar', handlers.FiltradoHandler)
        ]),
        routes.PathPrefixRoute(r'/seed', [
            webapp2.Route(r'/', handlers.SeedHandler)
        ]),
        routes.PathPrefixRoute(r'/session', [
            webapp2.Route(r'/test', OAuthTest),
            webapp2.Route(r'/', OAuthLogin)
        ])
    ]),
    webapp2.Route(tokens.google_oauth_decorator.callback_path, tokens.google_oauth_decorator.callback_handler())
], debug=True)
